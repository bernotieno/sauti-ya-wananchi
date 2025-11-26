# Deployment Guide - Sauti ya Wananchi

This guide covers deploying the Sauti ya Wananchi platform to production using Railway, Docker, or other hosting providers.

## Table of Contents

1. [Railway Deployment (Recommended)](#railway-deployment-recommended)
2. [Docker Deployment](#docker-deployment)
3. [Database Seeding](#database-seeding)
4. [Environment Variables](#environment-variables)
5. [Post-Deployment Setup](#post-deployment-setup)
6. [Troubleshooting](#troubleshooting)

---

## Railway Deployment (Recommended)

Railway is the recommended hosting platform for Sauti ya Wananchi due to its excellent Django and PostgreSQL support.

### Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- OpenAI API key (for Whisper transcription)
- Anthropic API key (for Claude AI processing)

### Step 1: Prepare Your Repository

1. Ensure all changes are committed to git:
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your `sauti-ya-wananchi` repository
4. Railway will automatically detect it's a Django project

### Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables

Go to your Railway project settings and add these environment variables:

```bash
# Django Core (CRITICAL)
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>

# Security - Replace with your Railway domain
ALLOWED_HOSTS=your-app.railway.app,yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-app.railway.app,https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-app.railway.app,https://yourdomain.com

# AI Services (REQUIRED)
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Optional
PORT=8000
RAILWAY_ENVIRONMENT=production
```

**To generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy

1. Railway will automatically build and deploy your application
2. Monitor the deployment logs in the Railway dashboard
3. Once deployed, you'll receive a public URL (e.g., `https://your-app.railway.app`)

### Step 6: Run Initial Setup

After first deployment, access the Railway CLI or use the web terminal:

```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run migrations (if not done automatically)
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Seed database with sample data
railway run python manage.py seed_data

# Process existing complaints with AI (optional)
railway run python manage.py process_complaints
```

---

## Docker Deployment

Use Docker for local development or deployment to VPS/cloud providers.

### Local Development with Docker

1. **Start all services:**
```bash
docker-compose up -d
```

2. **Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

3. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

4. **Seed database:**
```bash
docker-compose exec web python manage.py seed_data
```

5. **Access the application:**
- Web: http://localhost:8000
- Admin: http://localhost:8000/admin

6. **View logs:**
```bash
docker-compose logs -f web
```

7. **Stop services:**
```bash
docker-compose down
```

### Production Docker Deployment

Build and run production container:

```bash
# Build production image
docker build --target production -t sauti-ya-wananchi:latest .

# Run with environment variables
docker run -d \
  --name sauti-web \
  -p 8000:8000 \
  --env-file .env.production \
  -v ./staticfiles:/app/staticfiles \
  -v ./media:/app/media \
  sauti-ya-wananchi:latest
```

### Docker on VPS (DigitalOcean, AWS, etc.)

1. **Install Docker on your VPS:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

2. **Clone repository:**
```bash
git clone https://github.com/yourusername/sauti-ya-wananchi.git
cd sauti-ya-wananchi
```

3. **Set up environment:**
```bash
cp .env.production .env
# Edit .env with your production values
nano .env
```

4. **Deploy with docker-compose:**
```bash
docker-compose -f docker-compose.yml up -d
```

---

## Database Seeding

The project includes a management command to populate the database with sample data for testing and demonstration.

### Seed Command Options

**Add sample data to existing database:**
```bash
python manage.py seed_data
```

**Clear existing data and reseed:**
```bash
python manage.py seed_data --clear
```

### What Gets Created

The `seed_data` command creates:

- **1 Admin User**
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@sauti.go.ke`

- **5 Citizen Users**
  - Usernames: `wanjiku`, `ochieng`, `akinyi`, `mutua`, `njeri`
  - Password (all): `password123`
  - Various counties across Kenya

- **12+ Sample Complaints**
  - Various categories (corruption, bribery, delays, etc.)
  - Different urgency levels
  - Realistic Kenyan scenarios
  - Mix of anonymous and authenticated complaints
  - Already AI-processed with summaries

### Running on Railway

```bash
railway run python manage.py seed_data
```

### Running with Docker

```bash
docker-compose exec web python manage.py seed_data
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Debug mode (False in production) | `False` |
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.com,www.yourdomain.com` |
| `OPENAI_API_KEY` | OpenAI API key for Whisper | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | `sk-ant-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application port | `8000` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `http://localhost:8000` |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins | `""` |
| `DB_NAME` | Database name (if not using DATABASE_URL) | `sauti_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `""` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

---

## Post-Deployment Setup

### 1. Create Admin User

If you didn't seed the database:

```bash
# Railway
railway run python manage.py createsuperuser

# Docker
docker-compose exec web python manage.py createsuperuser

# Local
python manage.py createsuperuser
```

### 2. Configure Domain (Optional)

**Railway:**
1. Go to project settings → Domains
2. Add custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` environment variables

### 3. Set Up Media Storage (Production)

For production, consider using cloud storage for media files:

- **AWS S3** - Use `django-storages` with S3 backend
- **Cloudinary** - Use `django-cloudinary-storage`
- **Railway Volumes** - Persistent storage on Railway

### 4. Monitor Application

**Railway:**
- Built-in metrics and logs in dashboard
- Set up health checks and alerts

**Docker:**
```bash
# View logs
docker-compose logs -f web

# Check container status
docker-compose ps

# Monitor resources
docker stats
```

### 5. Set Up Automated Backups

**Railway Database:**
1. Go to PostgreSQL service settings
2. Enable automated backups
3. Configure backup retention

**Docker:**
```bash
# Backup database
docker-compose exec db pg_dump -U postgres sauti_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres sauti_db < backup.sql
```

---

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

**Problem:** CSS/JS not loading after deployment

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Ensure WhiteNoise is in MIDDLEWARE (already configured)
```

#### 2. Database Connection Errors

**Problem:** Can't connect to PostgreSQL

**Solution Railway:**
- Verify `DATABASE_URL` is set in environment variables
- Check PostgreSQL service is running
- Ensure web service is linked to database

**Solution Docker:**
```bash
# Check database container
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### 3. Migration Errors

**Problem:** Migration fails on deployment

**Solution:**
```bash
# Reset migrations (CAUTION: loses data)
python manage.py migrate --fake

# Or manually run migrations
python manage.py migrate --run-syncdb
```

#### 4. AI Processing Fails

**Problem:** Complaint processing fails

**Solution:**
- Verify `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are correct
- Check API quotas and billing
- Review logs for specific API errors

#### 5. ALLOWED_HOSTS Error

**Problem:** "Invalid HTTP_HOST header" error

**Solution:**
- Add your domain to `ALLOWED_HOSTS` environment variable
- Include Railway domain: `your-app.railway.app`
- Format: comma-separated, no spaces

#### 6. CSRF Verification Failed

**Problem:** CSRF errors on form submissions

**Solution:**
- Add domain to `CSRF_TRUSTED_ORIGINS`
- Include protocol: `https://yourdomain.com`
- Clear browser cookies and try again

### Getting Help

- **Documentation:** `/home/sir0kumu/sauti-ya-wananchi/CLAUDE.md`
- **Railway Docs:** https://docs.railway.app
- **Django Docs:** https://docs.djangoproject.com
- **Docker Docs:** https://docs.docker.com

---

## Security Checklist

Before going to production:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Enable HTTPS (Railway does this automatically)
- [ ] Set up CSRF_TRUSTED_ORIGINS
- [ ] Secure database credentials
- [ ] Rotate API keys regularly
- [ ] Set up database backups
- [ ] Enable Railway/server monitoring
- [ ] Review Django security checklist: `python manage.py check --deploy`

---

## Useful Commands

```bash
# Check deployment configuration
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed database
python manage.py seed_data

# Process complaints with AI
python manage.py process_complaints

# Run tests
python manage.py test

# Shell access
python manage.py shell

# Database shell
python manage.py dbshell
```

---

## Next Steps

After successful deployment:

1. Test all functionality on production
2. Create your admin account
3. Seed database with sample data (for testing)
4. Configure custom domain (optional)
5. Set up monitoring and alerts
6. Document your specific deployment configuration
7. Plan regular backup schedule

---

**Need Help?** Review the main project documentation in `CLAUDE.md` or Railway's Django deployment guide.
