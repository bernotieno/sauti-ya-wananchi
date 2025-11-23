# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sauti ya Wananchi (Voice of the Citizens) is a civic-tech platform for Kenyan citizens to report corruption and service failures via voice, text, or image. AI processes complaints and displays them on a public accountability dashboard.

**Status:** MVP Phase - project specification only, no implementation yet.

## Technology Stack

- **Backend:** Django 4.2+ (Python 3.9+)
- **Database:** PostgreSQL
- **Frontend:** Django templates + Tailwind CSS
- **Charts:** Chart.js
- **AI Services:** OpenAI Whisper API (transcription), Claude API (categorization/summarization)
- **Deployment:** Railway/Render

## Commands

```bash
# Development
python manage.py runserver              # Start dev server
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Create admin user

# Testing
python manage.py test                   # Run all tests
python manage.py test complaints        # Test specific app
python manage.py test --keepdb          # Keep test database

# AI Processing
python manage.py process_complaints     # Manual AI processing batch

# Code Quality
black .                                 # Format code
flake8 .                               # Lint code
```

## Architecture

```
User Input (text/audio/image) → Django Backend → AI Processing Layer → PostgreSQL
                                                        ↓
                                              (Whisper + Claude APIs)
                                                        ↓
                                              Public Dashboard
```

**Django Apps:**
- `complaints/` - Core complaint submission, storage, and processing
- `dashboard/` - Public analytics feed and visualizations
- `api/` - REST endpoints for future scalability
- `ai_services/` - Whisper transcription, Claude categorization/summarization utilities
- `config/` - Django settings and URL routing

## Core Data Model

```python
Complaint:
    id: UUID
    raw_text: Text                    # Original text or transcript
    summary: Text                     # AI-generated 2-3 sentence summary
    category: Enum                    # corruption, delay, bribery, misconduct, lost_documents, infrastructure_damage, other
    county: String                    # Kenyan county (Nairobi, Kisumu, etc.)
    urgency: Enum                     # low, medium, high, critical
    sentiment: String
    audio_url: FileField
    image_url: FileField
    officer_name: String (optional)
    department_name: String (optional)
    created_at: DateTime
    ai_processed: Boolean
```

## Key Integration Points

### AI Processing Pipeline
1. Audio files → `ai_services/whisper_service.py` → transcribed text
2. Text → `ai_services/categorization.py` → category + urgency + county extraction
3. Text → `ai_services/summarization.py` → 2-3 sentence official summary

### URL Structure
- `/` - Dashboard with live feed and analytics
- `/submit/` - Complaint submission form
- `/complaints/<id>/` - Individual complaint detail + shareable card
- `/api/complaints/` - REST API endpoint
- `/admin/` - Django admin for complaint review

## Environment Variables

```
DEBUG=True/False
SECRET_KEY=<django-secret-key>
DATABASE_URL=<postgresql-connection-string>
OPENAI_API_KEY=<whisper-api-key>
ANTHROPIC_API_KEY=<claude-api-key>
ALLOWED_HOSTS=localhost,127.0.0.1
```

## MVP Constraints

- Synchronous AI processing (no Celery)
- English/Swahili only
- No video support
- Use Django admin (no custom admin panel)
- Session-based accountability points (no user profiles)

## Out of Scope (V2+)

USSD/SMS, blockchain, Neo4j graphs, PWA offline mode, video evidence, gamification leaderboards.
