# SpotifyStats — Your Personal Discord Spotify Analytics Bot

SpotifyStats is a Discord bot that tracks your **Spotify listening activity** and visualizes it through beautiful charts and detailed statistics. 

You can view daily, weekly, monthly, and yearly insights - along with top artists, songs, genres, and more.

## Installation & Setup

Follow the steps below to clone the repo and configure the bot.

### 1. Clone the Repository 
```bash
git clone https://github.com/ftpng/SpotifyStats.git
cd SpotifyStats
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your `.env` File

Inside the project root, create a file named:
```
.env
```

Copy and paste the following template:
```
TOKEN = 

SPOTIFY_CLIENT_ID = 
SPOTIFY_CLIENT_SECRET = 
SPOTIFY_REFRESH_TOKEN = 

DBUSER = 
DBPASS = 
DBNAME = 
DBENDPOINT = 
```

### 4. Run the Bot
```bash
python main.py
```

## Commands
- `/daily` Shows your listening stats for today.
- `/weekly` Shows your weekly summary.
- `/monthly` Shows your monthly listening stats.
- `/overview` Your yearly Spotify overview.
- `/nowplaying` Displays what you're currently listening to on Spotify.
- `/topartists` Shows your top artists, ranked by total listening time.
- `/topsongs` Shows your top tracks for the year.
- `/topgenres` Shows your top Spotify genres based on your listening history.

Most commands include a chart or graph that helps visualize your listening patterns:
- `/daily` → hourly graph
- `/weekly` → weekday graph
- `/monthly` → daily graph
- `/overview` → monthly graph

# Support
If you run into any issues, bugs, or have other questions, feel free to DM me on Discord `@ventros.` thanks!