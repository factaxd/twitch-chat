class Config:
    CLIENT_ID = "your_twitch_client_id"  # Add your Twitch Client ID here
    CLIENT_SECRET = "your_twitch_client_secret"  # Add your Twitch Client Secret here
    REDIRECT_URI = "http://localhost:3000"
    IRC_TOKEN = "oauth:your_oauth_token"  # This will be set dynamically after login
    USERNAME = "your_twitch_username"     # Leave this as-is; it's set dynamically
    CHANNEL = ""  # This is dynamically set to your username after login
    PORT = 3000   # Local server port for OAuth redirection
    SCOPE = ['user:read:email', 'chat:read']  # Required Twitch permissions
