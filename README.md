# Sauti ya Wananchi (Voice of the Citizens)

A civic-tech platform empowering Kenyan citizens to report corruption, service failures, and misconduct through voice, text, or image submissions. AI-powered processing delivers real-time accountability insights on a public dashboard.

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Multi-Modal Submissions**: Text, voice recordings, and images
- **AI-Powered Processing**:
  - Whisper API for audio transcription
  - Claude API for categorization and summarization
- **Real-Time Dashboard**: Live feed of complaints with analytics
- **County-Based Tracking**: Organized by Kenya's 47 counties
- **Urgency Classification**: Low, Medium, High, Critical
- **Anonymous Reporting**: Optional anonymous submissions
- **Admin Verification**: Review and verification system
- **Accountability Points**: Civic engagement gamification

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: PostgreSQL 15+
- **AI Services**: OpenAI Whisper, Anthropic Claude
- **Frontend**: Django Templates, Tailwind CSS
- **Visualization**: Chart.js
- **Deployment**: Railway (recommended), Docker
- **Web Server**: Gunicorn with WhiteNoise

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- OpenAI API Key
- Anthropic API Key

### Local Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/sauti-ya-wananchi.git
cd sauti-ya-wananchi
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your values
```

5. **Set up database:**
```bash
# Create PostgreSQL database
createdb sauti_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed with sample data
python manage.py seed_data
```

6. **Run development server:**
```bash
python manage.py runserver
```

7. **Access the application:**
- Homepage: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- Dashboard: http://localhost:8000/dashboard

## Docker Setup

### Using Docker Compose (Recommended for Development)

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Seed database
docker-compose exec web python manage.py seed_data

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## Deployment

### Railway Deployment (Recommended)

1. **Push to GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy to Railway:**
   - Visit https://railway.app/new
   - Connect your GitHub repository
   - Add PostgreSQL database
   - Configure environment variables (see [DEPLOYMENT.md](DEPLOYMENT.md))

3. **Post-deployment:**
```bash
railway run python manage.py seed_data
```

**Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Project Structure

```
sauti-ya-wananchi/
├── accounts/              # User authentication and profiles
├── admin_panel/           # Admin dashboard views
├── ai_services/           # AI processing utilities (Whisper, Claude)
├── citizen/               # Citizen-facing views
├── complaints/            # Core complaint models and views
│   ├── management/
│   │   └── commands/
│   │       ├── process_complaints.py  # AI processing batch
│   │       └── seed_data.py           # Database seeding
│   ├── models.py          # Complaint data model
│   └── views.py
├── config/                # Django settings and URLs
│   ├── settings.py
│   └── urls.py
├── dashboard/             # Public analytics dashboard
├── pages/                 # Landing and static pages
├── static/                # CSS, JavaScript, images
├── templates/             # HTML templates
├── media/                 # User uploads (audio, images)
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Production Docker image
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── railway.toml           # Railway configuration
└── manage.py              # Django management script
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Django Core
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=sauti_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# AI API Keys
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```

## Available Commands

```bash
# Development
python manage.py runserver              # Start dev server
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Create admin user

# Data Management
python manage.py seed_data              # Populate with sample data
python manage.py seed_data --clear      # Clear and reseed database
python manage.py process_complaints     # Manually trigger AI processing

# Testing
python manage.py test                   # Run all tests
python manage.py test complaints        # Test specific app

# Production
python manage.py collectstatic          # Collect static files
python manage.py check --deploy         # Check production readiness
gunicorn config.wsgi:application        # Run production server
```

## Database Seeding

The project includes realistic sample data for testing:

```bash
python manage.py seed_data
```

**Creates:**
- 1 admin user (`admin`/`admin123`)
- 5 citizen users (password: `password123`)
- 12+ sample complaints across various categories
- Pre-processed AI summaries and categorizations

**Clear existing data and reseed:**
```bash
python manage.py seed_data --clear
```

## AI Processing

The platform uses AI to automatically process complaints:

### Whisper (OpenAI)
- Transcribes audio complaints to text
- Supports multiple languages (English, Swahili)

### Claude (Anthropic)
- Categorizes complaints (corruption, bribery, delay, etc.)
- Extracts urgency level (low, medium, high, critical)
- Identifies county and department
- Generates concise 2-3 sentence summaries
- Analyzes sentiment

**Manual processing:**
```bash
python manage.py process_complaints
```

## Data Model

### Complaint Model

```python
Complaint:
    id: UUID                     # Unique identifier
    user: ForeignKey             # Submitter (null if anonymous)
    is_anonymous: Boolean        # Anonymous flag
    raw_text: Text               # Original text or transcript
    summary: Text                # AI-generated summary
    category: Enum               # corruption, delay, bribery, etc.
    county: String               # Kenyan county
    urgency: Enum                # low, medium, high, critical
    sentiment: String            # Sentiment analysis
    audio_file: File             # Voice recording
    image_file: Image            # Evidence image
    officer_name: String         # Officer involved (optional)
    department_name: String      # Department name
    ai_processed: Boolean        # Processing status
    is_verified: Boolean         # Admin verification
    created_at: DateTime
    updated_at: DateTime
```

### Kenyan Counties Supported

All 47 counties including: Nairobi, Mombasa, Kisumu, Nakuru, Kiambu, Machakos, and more.

## API Endpoints

RESTful API available at `/api/`:

- `GET /api/complaints/` - List all complaints (paginated)
- `GET /api/complaints/<id>/` - Retrieve specific complaint
- `POST /api/complaints/` - Submit new complaint
- `GET /api/complaints/stats/` - Get statistics by county/category

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test complaints

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Security Features

- **HTTPS**: Enforced in production
- **CSRF Protection**: Built-in Django CSRF tokens
- **SQL Injection**: Protected by Django ORM
- **XSS Prevention**: Template auto-escaping
- **Secure Headers**: HSTS, X-Frame-Options, etc.
- **Password Validation**: Strong password requirements
- **Session Security**: Secure cookies in production

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking (if using mypy)
mypy .
```

## Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up `CSRF_TRUSTED_ORIGINS`
- [ ] Configure PostgreSQL database
- [ ] Add AI API keys
- [ ] Collect static files
- [ ] Run migrations
- [ ] Create superuser
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure monitoring
- [ ] Run security check: `python manage.py check --deploy`

## Troubleshooting

Common issues and solutions are documented in [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting).

## Roadmap

### Current (MVP)
- [x] Text, audio, and image submissions
- [x] AI-powered categorization and summarization
- [x] Public dashboard with analytics
- [x] Admin verification system
- [x] County-based organization
- [x] Docker deployment
- [x] Railway deployment support

### Future (V2+)
- [ ] USSD/SMS integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] Multi-language support (full Swahili)
- [ ] Video evidence support
- [ ] Blockchain verification
- [ ] Graph database for connections (Neo4j)
- [ ] PWA offline mode
- [ ] Gamification leaderboards

## Documentation

- [CLAUDE.md](CLAUDE.md) - Project overview and development guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Comprehensive deployment guide
- [Project.md](Project.md) - Original project specification

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for Whisper API
- Anthropic for Claude API
- Django community
- Railway for hosting infrastructure
- Kenyan civic tech community

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Email: support@sauti.go.ke (if applicable)

---

**Built with ❤️ for Kenya's accountability and transparency**
