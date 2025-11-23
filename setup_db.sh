#!/bin/bash

# Sauti ya Wananchi - Database Setup Script
# Run with: sudo bash setup_db.sh

set -e

echo "=========================================="
echo "Sauti ya Wananchi - Database Setup"
echo "=========================================="

# Configuration
DB_NAME="sauti_db"
DB_USER="sauti_user"
DB_PASSWORD="sauti_pass_2025"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo: sudo bash setup_db.sh"
    exit 1
fi

# Create database and user
echo ""
echo "[1/2] Creating database and user..."
sudo -u postgres psql <<EOF
-- Drop if exists (for fresh setup)
DROP DATABASE IF EXISTS ${DB_NAME};
DROP USER IF EXISTS ${DB_USER};

-- Create user and database
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
ALTER USER ${DB_USER} CREATEDB;

-- Grant schema permissions (PostgreSQL 15+)
\c ${DB_NAME}
GRANT ALL ON SCHEMA public TO ${DB_USER};
EOF

# Create .env file
echo ""
echo "[2/2] Creating .env file..."
cat > .env <<EOF
# Django settings
DEBUG=True
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=5432

# AI API Keys (add your keys here)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:8000
EOF

# Set proper ownership of .env
REAL_USER=${SUDO_USER:-$USER}
chown $REAL_USER:$REAL_USER .env

echo ""
echo "=========================================="
echo "Setup complete!"
echo ""
echo "Database Details:"
echo "  Name:     ${DB_NAME}"
echo "  User:     ${DB_USER}"
echo "  Password: ${DB_PASSWORD}"
echo "  Host:     localhost"
echo "  Port:     5432"
echo "=========================================="
