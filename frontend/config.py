# General Application Configurations
APP_NAME = "S.C.A.M."
APP_VERSION = "1.0.0"
APP_WIDTH = 800 # Windowed mode
APP_HEIGHT = 600

# Colors
PRIMARY_COLOR = "#222B36"
SECONDARY_COLOR = "#2ecc71"
BACKGROUND_COLOR = "#141A1F"
TEXT_COLOR = "#2c3e50"

# Fonts
FONT_FAMILY = "Arial"
FONT_SIZE_LARGE = 14
FONT_SIZE_MEDIUM = 12
FONT_SIZE_SMALL = 10

# Paths
ICON_PATH = "assets/images/icon.png"
LOGO_PATH = "assets/images/logo.png"
STYLESHEET_PATH = "assets/styles/stylesheet.css"

# API Endpoints
API_BASE_URL = "http://localhost:5000/"
LOGIN_ENDPOINT = f"{API_BASE_URL}/auth/login"
SIGNUP_ENDPOINT = f"{API_BASE_URL}/auth/signup"
NOTES_ENDPOINT = f"{API_BASE_URL}/notes"
EVENTS_ENDPOINT = f"{API_BASE_URL}/events"
TASKS_ENDPOINT = f"{API_BASE_URL}/tasks"
PROGRESS_ENDPOINT = f"{API_BASE_URL}/progress"
FLASHCARDS_ENDPOINT = f"{API_BASE_URL}/flashcards"
COLLABORATION_ENDPOINT = f"{API_BASE_URL}/collaboration"
USERS_ENDPOINT = f"{API_BASE_URL}/users"

# Other Settings
AUTO_SAVE_INTERVAL = 300000  # 5 minutes in milliseconds
MAX_RECENT_FILES = 10
