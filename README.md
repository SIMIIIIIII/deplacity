# Deplacity

A Flask web application for analyzing traffic and mobility data in Belgian cities.

## Project Structure

```
deplacity/
├── __init__.py              # Flask app factory
├── wsgi.py                  # WSGI entry point for production
├── run.py                   # Development server runner
├── Schema.sql               # Database schema
├── Deplacity.csv            # Source data file
├── package.json             # Frontend dependencies (Chart.js)
├── .env                     # Environment variables (credentials)
├── .gitignore               # Git ignore file
│
├── instance/                # Instance folder (auto-created)
│   └── Deplacity.sqlite    # SQLite database (auto-created)
│
├── blueprints/              # Flask blueprints (routes/views)
│   ├── home.py             # Home page routes
│   ├── admin.py            # Admin panel routes
│   ├── citymap.py          # City map visualization routes
│   ├── requete.py          # Query/search routes
│   └── statistique.py      # Statistics page routes
│
├── models/                  # Database models and queries
│   ├── city.py             # City-related queries
│   ├── statistique.py      # Statistics queries
│   ├── requete.py          # Search queries
│   └── full_moon_ratio.py  # Moon phase analysis
│
├── utils/                   # Utility modules
│   ├── db.py               # Database connection utilities
│   ├── csv_file.py         # CSV data import utilities
│   └── moon_utils.py       # Moon phase calculations
│
├── static/                  # Static files (CSS, JS, images)
│   ├── *.css               # Stylesheets
│   ├── charFiles/          # Chart.js visualization scripts
│   ├── photos/             # Images
│   └── pts/                # Point data files
│
├── templates/               # Jinja2 HTML templates
│   └── *.html
│
└── tests/                   # Unit tests
    └── test_*.py
```

## Setup and Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd deplacity
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # OR
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # OR install minimal dependencies:
   pip install Flask python-dotenv
   ```

4. **Configure environment variables:**
   
   The `.env` file contains admin credentials and Flask configuration:
   ```bash
   # .env file (already created)
   ADMIN_USERNAME=Deplacity
   ADMIN_PASSWORD=G19DeplacityUcl
   SECRET_KEY=dev
   ```
   
   **⚠️ IMPORTANT**: Change these values in production!

5. **Optional: Install production server (Gunicorn):**
   ```bash
   pip install gunicorn
   ```

## Running the Application

### Development Mode

From the `deplacity` directory:

**Option 1: Using run.py (Recommended)**

```bash
cd deplacity
python3 run.py
```

The server will start at:

- <http://127.0.0.1:5000>
- <http://192.168.0.164:5000> (network accessible)

**Option 2: Using Flask CLI**

```bash
cd deplacity
export FLASK_APP="deplacity:create_app"
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### Production Mode

Using Gunicorn (recommended for production):

```bash
cd deplacity
gunicorn --workers 3 --bind 0.0.0.0:8000 "deplacity.wsgi:application"
```

## Features

- **Home Page**: Overview and introduction
- **Statistics**: View traffic statistics by city
- **Queries**: Search and analyze traffic data by city, street, and time period
- **City Map**: Interactive map showing traffic data across Belgian cities
- **Admin Panel**: Manage city data (requires authentication)
- **Team Page**: Information about the development team

## Database

The application uses SQLite with the following tables:
- `ville` - Cities data
- `rue` - Streets data
- `trafic` - Traffic observations
- `vitesse` - Speed measurements
- `v85` - 85th percentile speed data
- `proportion` - Traffic proportion by vehicle type

The database is automatically initialized on first run from `Deplacity.csv`.

## Development

- Debug mode is enabled by default in `run.py`
- Auto-reload is active when code changes are detected
- Access debugger at errors when running in debug mode

## Testing

Run tests from the deplacity directory:

```bash
cd deplacity
python3 -m pytest tests/
```

Or run individual test files:

```bash
python3 -m pytest tests/test_city.py
```

## Notes

- The `instance/` folder is created automatically for the SQLite database
- The database is initialized from `Schema.sql` on first run
- CSV data is imported automatically from `Deplacity.csv` on first request
- Frontend assets (Chart.js) are configured in `package.json`

## Troubleshooting

- If you encounter import errors, ensure you're running the application from the `deplacity` directory
- Make sure the virtual environment is activated before running the app
- The database file will be created at `instance/Deplacity.sqlite` on first run
- Check that port 5000 is not already in use by another application
