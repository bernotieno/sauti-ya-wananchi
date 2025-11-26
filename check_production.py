#!/usr/bin/env python
"""
Production Readiness Checker for Sauti ya Wananchi
Validates configuration before deployment
"""

import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings
from django.core.management import call_command


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(50)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text):
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def check_debug_mode():
    """Check if DEBUG is False in production"""
    if settings.DEBUG:
        print_error("DEBUG is set to True (should be False in production)")
        return False
    else:
        print_success("DEBUG is False")
        return True


def check_secret_key():
    """Check if SECRET_KEY is strong"""
    if settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        print_error("SECRET_KEY is using default insecure value")
        return False
    elif len(settings.SECRET_KEY) < 50:
        print_warning("SECRET_KEY seems short (should be 50+ characters)")
        return False
    else:
        print_success("SECRET_KEY is configured")
        return True


def check_allowed_hosts():
    """Check ALLOWED_HOSTS configuration"""
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
        print_error("ALLOWED_HOSTS is not properly configured")
        return False
    elif 'localhost' in settings.ALLOWED_HOSTS or '127.0.0.1' in settings.ALLOWED_HOSTS:
        print_warning("ALLOWED_HOSTS contains localhost/127.0.0.1 (may not be needed in production)")
        return True
    else:
        print_success(f"ALLOWED_HOSTS: {', '.join(settings.ALLOWED_HOSTS)}")
        return True


def check_database():
    """Check database configuration"""
    db = settings.DATABASES['default']
    if db['ENGINE'] == 'django.db.backends.sqlite3':
        print_error("Using SQLite (use PostgreSQL for production)")
        return False
    elif db['ENGINE'] == 'django.db.backends.postgresql':
        print_success("Using PostgreSQL")
        return True
    else:
        print_warning(f"Using {db['ENGINE']}")
        return True


def check_api_keys():
    """Check if AI API keys are configured"""
    results = []

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == 'your-openai-api-key':
        print_error("OPENAI_API_KEY not configured")
        results.append(False)
    else:
        print_success("OPENAI_API_KEY is configured")
        results.append(True)

    if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == 'your-anthropic-api-key':
        print_error("ANTHROPIC_API_KEY not configured")
        results.append(False)
    else:
        print_success("ANTHROPIC_API_KEY is configured")
        results.append(True)

    return all(results)


def check_static_files():
    """Check static files configuration"""
    if not settings.STATIC_ROOT:
        print_error("STATIC_ROOT not configured")
        return False

    static_root = Path(settings.STATIC_ROOT)
    if not static_root.exists():
        print_warning(f"STATIC_ROOT directory doesn't exist: {static_root}")
        print_warning("Run: python manage.py collectstatic")
        return False
    else:
        print_success(f"STATIC_ROOT configured: {static_root}")
        return True


def check_security_settings():
    """Check security middleware and settings"""
    results = []

    # Check WhiteNoise
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        print_success("WhiteNoise middleware enabled")
        results.append(True)
    else:
        print_warning("WhiteNoise middleware not found")
        results.append(False)

    # Check security middleware
    if 'django.middleware.security.SecurityMiddleware' in settings.MIDDLEWARE:
        print_success("Security middleware enabled")
        results.append(True)
    else:
        print_error("Security middleware not enabled")
        results.append(False)

    return all(results)


def check_csrf_settings():
    """Check CSRF configuration"""
    if hasattr(settings, 'CSRF_TRUSTED_ORIGINS') and settings.CSRF_TRUSTED_ORIGINS:
        print_success(f"CSRF_TRUSTED_ORIGINS configured")
        return True
    else:
        print_warning("CSRF_TRUSTED_ORIGINS not configured")
        return False


def run_django_checks():
    """Run Django's built-in deployment checks"""
    print("\nRunning Django deployment checks...")
    try:
        call_command('check', '--deploy', '--fail-level', 'WARNING')
        print_success("Django deployment checks passed")
        return True
    except Exception as e:
        print_error(f"Django deployment checks failed: {e}")
        return False


def main():
    print_header("Production Readiness Check")

    checks = [
        ("Debug Mode", check_debug_mode),
        ("Secret Key", check_secret_key),
        ("Allowed Hosts", check_allowed_hosts),
        ("Database", check_database),
        ("API Keys", check_api_keys),
        ("Static Files", check_static_files),
        ("Security Settings", check_security_settings),
        ("CSRF Settings", check_csrf_settings),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{Colors.BOLD}Checking {name}...{Colors.RESET}")
        results.append(check_func())

    # Run Django checks
    django_checks_passed = run_django_checks()
    results.append(django_checks_passed)

    # Summary
    print_header("Summary")
    passed = sum(results)
    total = len(results)

    if passed == total:
        print_success(f"All {total} checks passed! Ready for deployment.")
        return 0
    else:
        print_warning(f"{passed}/{total} checks passed.")
        print_error(f"{total - passed} checks failed or have warnings.")
        print("\nPlease fix the issues above before deploying to production.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
