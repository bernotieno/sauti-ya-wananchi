# Quick Reference - Sauti ya Wananchi

Essential commands and configurations for quick access.

## Local Development

```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Seed database
python manage.py seed_data
python manage.py seed_data --clear  # Clear and reseed

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell

# Check production readiness
python check_production.py
```

## Docker

```bash
# Start all services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Execute command in container
docker-compose exec web python manage.py [command]

# Rebuild containers
docker-compose up -d --build

# Access shell
docker-compose exec web bash
```

## Railway CLI

```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run command
railway run python manage.py [command]

# Open project
railway open

# Set environment variable
railway variables set KEY=value
```

## Database

```bash
# PostgreSQL commands
createdb sauti_db                    # Create database
dropdb sauti_db                      # Drop database
psql sauti_db                        # Access database

# Django database commands
python manage.py dbshell             # Database shell
python manage.py migrate             # Run migrations
python manage.py showmigrations      # Show migration status
python manage.py sqlmigrate app 0001 # View SQL for migration
```

## Git Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# Create branch
git checkout -b feature/feature-name

# Switch branch
git checkout main
```

## Environment Variables (Production)

```bash
DEBUG=False
SECRET_KEY=<generate-strong-key>
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=yourdomain.com
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Default Credentials (After Seeding)

```
Admin:
  Username: admin
  Password: admin123
  Email: admin@sauti.go.ke

Citizens:
  wanjiku / password123
  ochieng / password123
  akinyi / password123
  mutua / password123
  njeri / password123
```

## URLs

```
Local:
  Homepage:   http://localhost:8000
  Admin:      http://localhost:8000/admin
  Dashboard:  http://localhost:8000/dashboard
  Submit:     http://localhost:8000/complaints/submit
  Health:     http://localhost:8000/health

Railway:
  Replace localhost:8000 with your-app.railway.app
```

## File Structure

```
Key Directories:
  complaints/     - Core complaint models and views
  accounts/       - User authentication
  dashboard/      - Public dashboard
  templates/      - HTML templates
  static/         - CSS, JS, images
  media/          - User uploads

Key Files:
  manage.py       - Django management
  requirements.txt - Python dependencies
  .env            - Environment variables (local)
  docker-compose.yml - Docker configuration
  railway.toml    - Railway configuration
```

## Troubleshooting

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reset migrations (CAUTION: loses data)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Rebuild database (CAUTION: loses data)
dropdb sauti_db && createdb sauti_db
python manage.py migrate
python manage.py seed_data

# Check for issues
python manage.py check
python manage.py check --deploy

# View Django version
python -m django --version

# Update dependencies
pip install -r requirements.txt --upgrade
```

## API Endpoints

```
GET  /api/complaints/          - List complaints
GET  /api/complaints/<id>/     - Get complaint
POST /api/complaints/          - Create complaint
GET  /api/complaints/stats/    - Get statistics
GET  /health/                  - Health check
```

## Code Quality

```bash
# Format code
black .

# Check formatting
black . --check

# Lint code
flake8 .

# Run specific tests
python manage.py test complaints
python manage.py test complaints.tests.TestComplaintModel
```

## Production Deployment

```bash
# Railway
1. Push to GitHub
2. Connect to Railway
3. Add PostgreSQL
4. Set environment variables
5. Deploy automatically

# Manual Deploy
1. git push origin main
2. Railway auto-deploys
3. railway run python manage.py seed_data

# Check deployment
curl https://your-app.railway.app/health/
```

## Useful Django Commands

```bash
# Show installed apps
python manage.py showmigrations

# Create empty migration
python manage.py makemigrations --empty app_name

# Reverse migration
python manage.py migrate app_name migration_name

# Load fixtures
python manage.py loaddata fixture.json

# Dump data
python manage.py dumpdata app_name > fixture.json

# Clear sessions
python manage.py clearsessions

# Change password
python manage.py changepassword username
```

## Security

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Check security
python manage.py check --deploy

# Production checklist
python check_production.py
```

## Monitoring

```bash
# Railway logs
railway logs

# Docker logs
docker-compose logs -f

# Filter logs
railway logs | grep ERROR

# Follow logs in real-time
railway logs --follow
```

## Backup & Restore

```bash
# Backup database
pg_dump -U postgres sauti_db > backup.sql

# Restore database
psql -U postgres sauti_db < backup.sql

# Docker backup
docker-compose exec db pg_dump -U postgres sauti_db > backup.sql

# Railway backup
railway run pg_dump > backup.sql
```

---

For detailed information, see:
- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [CLAUDE.md](CLAUDE.md) - Development guide
