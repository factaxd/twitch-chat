import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk  # Pillow library for displaying profile images
from io import BytesIO
import requests
from twitch_api import TwitchAPI
from twitch_irc import TwitchIRC
from config import Config
import webbrowser

class TwitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitch Chat Reader")
        self.root.geometry("800x600")

        # Theme Colors
        self.bg_color = "#090300"
        self.fg_color = "#a5a2a2"
        self.button_color = "#3a3432"
        self.highlight_color = "#01a0e4"

        self.root.configure(bg=self.bg_color)

        self.selected_user = None
        self.irc = None
        self.api = TwitchAPI()

        # Frame for Profile Picture and User Info
        self.profile_frame = tk.Frame(root, bg=self.bg_color)
        self.profile_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        # Placeholder for Profile Picture
        self.profile_pic_label = tk.Label(self.profile_frame, bg=self.bg_color)
        self.profile_pic_label.pack(side=tk.LEFT, padx=10)

        # Placeholder for Username
        self.username_label = tk.Label(self.profile_frame, text="Not connected", bg=self.bg_color, fg=self.fg_color)
        self.username_label.pack(side=tk.LEFT, padx=10)

        # List of Users in the Chat
        self.user_listbox = tk.Listbox(root, bg=self.bg_color, fg=self.fg_color, highlightcolor=self.highlight_color, selectbackground=self.highlight_color)
        self.user_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

        # Button to Select a User
        self.select_user_button = tk.Button(root, text="Select User", command=self.on_user_select, bg=self.button_color, fg=self.fg_color)
        self.select_user_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Scrollable Textbox for Chat Messages
        self.chat_text = scrolledtext.ScrolledText(root, height=20, width=50, state=tk.DISABLED, bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.chat_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Connect to Twitch Button
        self.connect_button = tk.Button(root, text="Connect to Twitch", command=self.connect_to_twitch, width=30, bg=self.button_color, fg=self.fg_color)
        self.connect_button.grid(row=2, column=1, pady=10, sticky="e")

        # Disconnect from Twitch Button
        self.disconnect_button = tk.Button(root, text="Disconnect from Twitch", command=self.disconnect_from_twitch, width=30, bg=self.button_color, fg=self.fg_color, state=tk.DISABLED)
        self.disconnect_button.grid(row=3, column=1, pady=10, sticky="e")

        # Grid configuration: makes the elements responsive to window resizing
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def connect_to_twitch(self):
        try:
            auth_url = self.api.get_authorization_url()
            webbrowser.open(auth_url)
            messagebox.showinfo("Authorization", "Please authorize the app in the opened browser window.")
            auth_code = self.api.start_local_http_server()
            if not auth_code:
                messagebox.showerror("Error", "Failed to retrieve authorization code.")
                return

            self.api.get_token(auth_code)
            messagebox.showinfo("Success", "Successfully obtained access token.")

            user_info = self.api.get_user_info()
            username = user_info.get('login')
            display_name = user_info.get('display_name')
            user_id = user_info.get('id')
            profile_image_url = user_info.get('profile_image_url')  # Get the profile picture URL

            # Update the UI with the username and profile picture
            self.update_user_info(display_name, profile_image_url)

            # Set the channel name dynamically to the user's username
            channel = username
            print(f"Using channel: {channel}")
            self.username_label.config(text=f"Connected as: {display_name} (ID: {user_id})")

            # Connect to IRC and start receiving chat messages
            self.connect_to_twitch_chat(username, channel)

            # Enable the disconnect button after successful connection
            self.disconnect_button.config(state=tk.NORMAL)
            self.connect_button.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_user_info(self, display_name, profile_image_url):
        """Display the username and profile picture."""
        self.username_label.config(text=f"{display_name}")

        # Download and display the profile picture
        response = requests.get(profile_image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((50, 50))  # Resize the profile picture
        profile_img = ImageTk.PhotoImage(img)

        # Update the profile picture label
        self.profile_pic_label.config(image=profile_img)
        self.profile_pic_label.image = profile_img  # Keep a reference to avoid garbage collection

    def connect_to_twitch_chat(self, username, channel):
        try:
            self.irc = TwitchIRC(
                token=self.api.token['access_token'],
                username=username,
                channel=channel,
                on_message_callback=self.display_chat_message
            )
            self.irc.connect()
            messagebox.showinfo("Success", f"Connected to Twitch Chat on channel #{channel}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def disconnect_from_twitch(self):
        """Disconnect from Twitch and reset the UI."""
        if self.irc:
            self.irc.disconnect()  # Disconnect from IRC (you need to implement the disconnect method in IRC class)
            self.irc = None

        # Reset the UI components
        self.profile_pic_label.config(image='')
        self.username_label.config(text="Not connected")
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)
        self.user_listbox.delete(0, tk.END)

        # Disable disconnect button and enable connect button
        self.disconnect_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.NORMAL)

        messagebox.showinfo("Disconnected", "Disconnected from Twitch.")

    def display_chat_message(self, user_info, message):
        if self.selected_user and user_info != self.selected_user:
            return

        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{user_info}: {message}\n")
        if user_info not in self.user_listbox.get(0, tk.END):
            self.user_listbox.insert(tk.END, user_info)

        self.chat_text.yview(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def on_user_select(self):
        selection = self.user_listbox.curselection()
        if selection:
            self.selected_user = self.user_listbox.get(selection[0])
            messagebox.showinfo("User Selected", f"Now showing messages only from: {self.selected_user}")
        else:
            self.selected_user = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TwitchApp(root)
    root.mainloop()
