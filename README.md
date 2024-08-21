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


## Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/twitch-chat-reader.git
cd twitch-chat-reader


### 2. Set Up Twitch Developer App

To authenticate with Twitch, you need to create a Twitch Developer App to get your Client ID and Client Secret.

