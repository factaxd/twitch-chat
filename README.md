# Twitch Chat Reader

Twitch Chat Reader is a Python application that allows you to connect to a Twitch channel, read chat messages, and display them in a graphical user interface (GUI). The app also fetches the Twitch user's profile picture and shows it alongside their username.

## Features

- **Twitch OAuth 2.0 Authentication**: Connects to Twitch using secure OAuth authentication.
- **Live Chat Display**: Receives and displays Twitch chat messages in real-time.
- **Profile Info Display**: Shows the Twitch user's profile picture and username in the GUI.
- **User Selection**: Allows the user to select chat users and filter messages based on selected users.
- **Easy Disconnect**: Provides an option to disconnect from Twitch and reset the interface.

## Requirements

Before starting, make sure you have the following:

- **Python 3.x** installed on your machine.
- A **Twitch Developer account** to create an app and get your `Client ID` and `Client Secret`.

### Python Libraries

You will need the following Python libraries:

- `tkinter` (standard with Python)
- `requests`
- `Pillow` (for handling images)
- `requests_oauthlib`

You can install the required libraries using:

```bash
pip install requests Pillow requests_oauthlib
```





## Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/twitch-chat-reader.git
cd twitch-chat-reader
```

### 2. Set Up Twitch Developer App

To authenticate with Twitch, you need to create a Twitch Developer App to get your Client ID and Client Secret.

- Go to the Twitch Developers Console and create a new app.
- Set the OAuth Redirect URL to http://localhost:3000.
- Copy the Client ID and Client Secret provided by Twitch.


### 3. Update config.py

Open the config.py file and replace the placeholders with your Client ID and Client Secret.

```bash
class Config:
    CLIENT_ID = "your_twitch_client_id"  # Add your Twitch Client ID here
    CLIENT_SECRET = "your_twitch_client_secret"  # Add your Twitch Client Secret here
    REDIRECT_URI = "http://localhost:3000"
    IRC_TOKEN = "oauth:your_oauth_token"  # This will be set dynamically after login
    USERNAME = "your_twitch_username"     # Leave this as-is; it's set dynamically
    CHANNEL = ""  # This is dynamically set to your username after login
    PORT = 3000   # Local server port for OAuth redirection
    SCOPE = ['user:read:email', 'chat:read']  # Required Twitch permission
```
