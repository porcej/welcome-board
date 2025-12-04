# Digital Signage Welcome Board

A Flask-based digital signage application for displaying schedules, weather information, and custom content on digital displays. The application supports schedule management with date-based activation, custom icons, weather integration, and extensive customization options.

## Features

- **Schedule Management**: Create and manage schedules with optional date-based activation
  - Schedules with dates automatically activate on that specific date
  - Schedules without dates can be manually activated
  - Export/import schedules to/from Excel
  - Duplicate schedules for easy reuse

- **Schedule Items**: Add detailed items to schedules with:
  - Start/end times and duration
  - Location, uniform, and lead information
  - Notes and custom icons
  - Automatic end time calculation

- **Custom Icons**: Upload custom icons or create character-based icons for schedule items

- **Weather Integration**: Display weather information based on location coordinates and timezone

- **Display Customization**: 
  - Custom logo and background images
  - Color customization (background, text, panels)
  - Opacity controls
  - Timezone configuration

- **User Management**: Admin and user roles with authentication

- **Public Display**: Public-facing display endpoint that doesn't require authentication

## Prerequisites

- Docker and Docker Compose
- (Optional) Domain name and SSL certificate for production deployment

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd welcome-board
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (optional, defaults are provided):

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://app:app@db:5432/app
TIMEZONE=America/New_York
WEATHER_TTL_MINUTES=60
GUNICORN_WORKERS=2
GUNICORN_TIMEOUT=120
POSTGRES_USER=app
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=app
```

### 3. Build and Start Services

```bash
docker compose up -d --build
```

This will:
- Build the Flask application container
- Start PostgreSQL database
- Make the application available at `http://localhost:8005`

### 4. Initialize Database

Run database migrations:

```bash
docker compose exec app flask --app wsgi db upgrade
```

### 5. Create Admin User

Create your first admin user:

```bash
docker compose exec app flask --app wsgi create-admin
```

Follow the prompts to enter an email and password.

### 6. Access the Application

- **Admin Interface**: `http://localhost:8005`
- **Public Display**: `http://localhost:8005/display`

## Usage

### Managing Schedules

1. **Create a Schedule**:
   - Navigate to Schedules → New
   - Enter schedule name
   - (Optional) Set a date - if provided, the schedule will automatically activate on that date
   - Check "Active" to manually activate schedules without dates
   - Click "Save"

2. **Add Schedule Items**:
   - After creating a schedule, click "Add Item"
   - Fill in start time, duration, location, and other details
   - Select an icon if desired
   - Save the item

3. **Export/Import**:
   - Export schedules to Excel for backup or editing
   - Import schedules from Excel files

### Schedule Date Behavior

- **With Date**: If a schedule has a date set, it will automatically be displayed on that specific date, regardless of the "Active" checkbox
- **Without Date**: Schedules without dates require the "Active" checkbox to be enabled to display

### Customizing the Display

1. Navigate to **Schedules → Settings**
2. Configure:
   - Logo and background images
   - Colors (background, text, panels)
   - Opacity settings
   - Location coordinates for weather
   - Timezone

### Managing Icons

1. Navigate to **Icons**
2. Create icons by:
   - Uploading image files
   - Creating character-based icons with custom fonts

## Docker Commands

### Start Services

```bash
docker compose up -d
```

### Stop Services

```bash
docker compose down
```

### View Logs

```bash
# All services
docker compose logs -f

# Application only
docker compose logs -f app

# Database only
docker compose logs -f db
```

### Database Operations

```bash
# Run migrations
docker compose exec app flask --app wsgi db upgrade

# Create migration
docker compose exec app flask --app wsgi db migrate -m "migration message"

# Rollback migration
docker compose exec app flask --app wsgi db downgrade

# Access database shell (PostgreSQL)
docker compose exec db psql -U app -d app
```

### Create Admin User

```bash
docker compose exec app flask --app wsgi create-admin
```

### Execute Commands in Container

```bash
docker compose exec app <command>
```

### Rebuild After Changes

```bash
docker compose up -d --build
```

## Project Structure

```
welcome-board/
├── app/
│   ├── auth/              # Authentication routes
│   ├── display/           # Public display routes
│   ├── icons/             # Icon management
│   ├── schedules/         # Schedule management
│   ├── users/             # User management
│   ├── forms/             # WTForms form definitions
│   ├── models.py          # Database models
│   ├── config.py          # Configuration
│   └── templates/         # Jinja2 templates
├── migrations/            # Database migrations
├── nginx/                 # Nginx reverse proxy setup
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Application container definition
├── requirements.txt       # Python dependencies
└── wsgi.py               # WSGI entry point
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Flask environment (development/production) |
| `SECRET_KEY` | `dev-secret` | Secret key for sessions and CSRF protection |
| `DATABASE_URL` | `sqlite:////app/instance/app.db` | Database connection string |
| `TIMEZONE` | `UTC` | Timezone for weather and display |
| `WEATHER_TTL_MINUTES` | `60` | Weather cache TTL in minutes |
| `GUNICORN_WORKERS` | `2` | Number of Gunicorn worker processes |
| `GUNICORN_TIMEOUT` | `120` | Gunicorn worker timeout |
| `POSTGRES_USER` | `app` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `app` | PostgreSQL password |
| `POSTGRES_DB` | `app` | PostgreSQL database name |

### Database Options

The application supports both SQLite (default) and PostgreSQL:

- **SQLite**: Default, no additional configuration needed
- **PostgreSQL**: Set `DATABASE_URL=postgresql://user:password@db:5432/dbname` in your `.env` file

## Production Deployment

### Using Nginx Reverse Proxy

The project includes nginx configuration for production deployment with SSL. See `nginx/README.md` for detailed setup instructions.

### Security Considerations

1. **Change Default Secrets**: Update `SECRET_KEY` and database passwords
2. **Use HTTPS**: Set up SSL certificates (see nginx setup)
3. **Environment Variables**: Store sensitive data in `.env` file (not committed to git)
4. **Database**: Use strong PostgreSQL passwords in production
5. **Firewall**: Restrict access to necessary ports only

## Development

### Running in Development Mode

```bash
# Set FLASK_ENV to development
export FLASK_ENV=development

# Start services
docker compose up -d

# Access development server
docker compose exec app flask --app wsgi run --host=0.0.0.0 --port=5000
```

### Running Tests

```bash
docker compose exec app pytest tests/
```

### Code Structure

- **Models**: SQLAlchemy models in `app/models.py`
- **Routes**: Blueprint-based routing in `app/*/routes.py`
- **Forms**: WTForms definitions in `app/forms/`
- **Templates**: Jinja2 templates in `app/templates/`

## Troubleshooting

### Database Connection Issues

```bash
# Check database is running
docker compose ps db

# Check database logs
docker compose logs db

# Test connection
docker compose exec app flask --app wsgi shell
# Then in Python: from app.extensions import db; db.engine.connect()
```

### Migration Issues

```bash
# Check current migration status
docker compose exec app flask --app wsgi db current

# View migration history
docker compose exec app flask --app wsgi db history

# If stuck, you may need to manually fix the database state
```

### Application Not Starting

```bash
# Check application logs
docker compose logs app

# Check if port is already in use
lsof -i :8005

# Rebuild containers
docker compose down
docker compose up -d --build
```

### File Upload Issues

- Ensure `app/static/uploads` directory exists and is writable
- Check volume mounts in `docker-compose.yml`
- Verify `UPLOAD_FOLDER` environment variable

## API Endpoints

- `/` - Home page (requires authentication)
- `/auth/login` - Login page
- `/schedules/` - Schedule management (requires authentication)
- `/display/` - Public display endpoint
- `/display/check-updates` - JSON endpoint for checking updates

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support information here]

