#!/bin/bash

# Sauti ya Wananchi - Local Development Setup Script
# This script automates the setup process for local development

set -e  # Exit on error

echo "=========================================="
echo "Sauti ya Wananchi - Local Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
required_version="3.11"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "Error: Python $required_version or higher is required. You have Python $python_version"
    exit 1
fi
echo "✓ Python $python_version detected"
echo ""

# Check if PostgreSQL is installed
echo "Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL not found. Please install PostgreSQL 15+ before proceeding."
    echo "Visit: https://www.postgresql.org/download/"
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ PostgreSQL detected"
fi
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created from .env.example"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your configuration:"
    echo "   - Database credentials"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter when you've configured .env file..."
else
    echo "✓ .env file already exists"
fi
echo ""

# Database setup
echo "Setting up database..."
read -p "Do you want to create the database? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter database name (default: sauti_db): " db_name
    db_name=${db_name:-sauti_db}

    read -p "Enter PostgreSQL username (default: postgres): " db_user
    db_user=${db_user:-postgres}

    echo "Creating database..."
    createdb -U "$db_user" "$db_name" 2>/dev/null || echo "Database may already exist"
    echo "✓ Database setup complete"
fi
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py migrate
echo "✓ Migrations complete"
echo ""

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

# Create superuser
echo "Creating superuser..."
read -p "Do you want to create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
    echo "✓ Superuser created"
else
    echo "⚠️  You can create a superuser later with: python manage.py createsuperuser"
fi
echo ""

# Seed database
echo "Database seeding..."
read -p "Do you want to seed the database with sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py seed_data
    echo "✓ Database seeded with sample data"
    echo ""
    echo "Sample Credentials:"
    echo "  Admin: admin / admin123"
    echo "  Citizen: wanjiku / password123"
else
    echo "⚠️  You can seed the database later with: python manage.py seed_data"
fi
echo ""

# Setup complete
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run server: python manage.py runserver"
echo "  3. Visit: http://localhost:8000"
echo ""
echo "Admin panel: http://localhost:8000/admin"
echo "Dashboard: http://localhost:8000/dashboard"
echo ""
echo "Useful commands:"
echo "  python manage.py seed_data          # Add sample data"
echo "  python manage.py process_complaints # Process with AI"
echo "  python manage.py test               # Run tests"
echo ""
echo "Documentation:"
echo "  README.md       - Project overview"
echo "  DEPLOYMENT.md   - Deployment guide"
echo "  CLAUDE.md       - Development guide"
echo ""
echo "Happy coding! 🚀"
