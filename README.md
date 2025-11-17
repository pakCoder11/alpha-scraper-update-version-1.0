# Insta Data Scraper (Web)

A modern, Flask-based web application to extract and analyze Instagram data without using the official API. It provides a clean UI to:

- Post comments on posts
- Send direct messages
- Scrape posts and followers
- View live logs in real time (via WebSocket)
- Review and download generated data files (Excel/JSON)
- Run a local “AI” analysis (dummy/locally computed) and preview the report
- Toggle Light/Dark theme globally (with persistence)

Note: This project is intended for educational and personal use. Always comply with Instagram’s Terms of Service and applicable laws.

---

## Table of Contents
- Features
- Tech Stack
- Prerequisites
- Quick Start (Windows)
- Configuration (.env)
- Running the App
- Project Structure
- Key Pages & Routes
- Typical Workflows (Use Cases)
- Data & Reports
- Theming (Light/Dark)
- Troubleshooting
- Security & Compliance

---

## Features
- Web UI built with Bootstrap 5, Bootstrap Icons, and DataTables for a responsive, clean experience
- Real-time log streaming using Flask-SocketIO
- Data exploration page (Analyze) with preview, table/JSON modal viewers, created-time column, and direct file downloads
- Background file maintenance (temporary/output files can be cleaned on app startup)
- FAQ and helpful guide (Screenshot Guide page)
- Global Day/Night theme toggle with persistence across sessions and pages 
- Add Data Visualization section to display graphs related to the user data 
- Scraping Update: Add a new scraping function to extract REELS from any Instagram profile 

## Tech Stack
- Backend: Flask + Flask-SocketIO
- Frontend: Bootstrap 5, Bootstrap Icons, DataTables
- Data Processing: pandas, openpyxl, BeautifulSoup
- Automation & Scraping: selenium-driverless, pyautogui (legacy flows), custom scripts

## Prerequisites
- Python 3.10+ (tested with Python 3.13)
- Google Chrome/Chromium installed (selenium-driverless relies on a local browser)
- Windows PowerShell (examples below), but the app is cross-platform with equivalent commands on macOS/Linux

## Quick Start (Windows)
1) Clone or copy the project

2) Create and activate a virtual environment
- PowerShell
  - python -m venv .venv
  - .\.venv\Scripts\Activate.ps1

3) Upgrade pip
- pip install --upgrade pip

4) Install dependencies
- If you have a requirements.txt, run:
  - pip install -r requirements.txt
- Otherwise, install the core set directly:
  - pip install flask flask-socketio python-socketio python-engineio eventlet
  - pip install pandas numpy openpyxl beautifulsoup4
  - pip install selenium-driverless pyautogui
  - pip install python-dotenv

5) Create a .env file (see Configuration below)

6) Run the server
- python app.py
- Open http://127.0.0.1:5000 in your browser

## Configuration (.env)
Create a .env file in the project root with at least the following keys:

- INSTAGRAM_USERNAME=your_username
- INSTAGRAM_PASSWORD=your_password

Optional keys can be added later as features expand. Keep your .env private and never commit it.

## Running the App
- Development server: python app.py
  - Uses Flask’s debug mode and SocketIO dev server
  - Default URL: http://127.0.0.1:5000
- Stopping the app: Ctrl + C

## Project Structure
- app.py — Flask entry point, routes, and initialization
- templates/ — HTML templates (index, analyze, logs, screenshot guide)
- static/ — styles.css and media (e.g., bg.mp4)
- instagram_scraper.py — scraping/automation routines
- ai_function.py — local/dummy analysis function that generates an analysis report
- logs.txt — aggregated logs written by the system
- Screenshots/ — helper images used by the guide and/or documentation

## Key Pages & Routes
- / — Home: main features (comments, DMs, posts, followers), FAQ, and quick actions
- /logs — Live logs view with the ability to clear logs
- /analyze — File listing (Excel/JSON) with preview modals, download buttons, and AI analysis runner
- /screenshot-guide — Basic guidance on taking screenshots

## Typical Workflows (Use Cases)
1) Prepare environment
- Ensure .env is configured with your Instagram credentials
- Make sure Chrome/Chromium is installed

2) Choose a task from the Home page
- Write Comments on Posts: Provide the target profile/URLs and a list of comments (tooling may read from your provided files)
- Send Direct Messages: Provide usernames/URLs and message content
- Scrape Posts: Provide target profile, number of posts to scrape, and whether to capture comments
- Scrape Followers: Provide target profile and how far you want to scroll/load

3) Monitor progress in Logs
- Navigate to /logs to see real-time events

4) Review and download data in Analyze
- Go to /analyze to see detected .xlsx/.json files
- Preview as an HTML table or formatted JSON in modals
- Use the Download button to save files locally

5) (Optional) Run AI Analysis
- If eligible data exists (e.g., instagram_posts_comments.xlsx), trigger the local dummy analysis
- A markdown-like report is generated and displayed in the page

## Data & Reports
- Output data files: usually stored in the project root directory (Excel .xlsx and JSON .json)
- Analysis report: analysis_report.md (or sentiment_analysis_report.md in some flows) generated in the project root
- Automatic cleanup: Certain temporary/output files may be cleaned on the first request after the app starts. Download any files you want to keep.

## Theming (Light/Dark)
- Use the moon/sun icon in the navbar to toggle Light/Dark theme
- Selection persists across pages (stored in localStorage)
- The app also respects system preference on first load

## Troubleshooting
- Page doesn’t load / socket errors
  - Ensure the server is running (python app.py) and the terminal shows Running on http://127.0.0.1:5000
  - Some corporate networks or firewalls may block WebSocket connections
- Missing dependencies
  - Re-run the pip install commands above; verify your virtual environment is activated
- Chrome/Chromium not found
  - Install Chrome/Chromium; ensure it is in the default path for selenium-driverless
- Excel errors
  - Ensure openpyxl is installed; re-install pandas/openpyxl
- Permission errors on Windows
  - Try running PowerShell as Administrator for initial setup, or ensure the project directory is writable

## Security & Compliance
- Never share or commit your .env (credentials)
- Be mindful of Instagram’s Terms of Service and rate limits
- Use responsibly and ethically; this repository is provided “as is” for educational purposes

---

Happy scraping and analyzing!