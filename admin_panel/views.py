from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint


def is_admin(user):
    """Check if user is an admin."""
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)


@login_required
@user_passes_test(is_admin, login_url='accounts:login')
def admin_dashboard(request):
    """Admin dashboard with overview and management tools."""

    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Overview stats
    total_complaints = Complaint.objects.count()
    complaints_today = Complaint.objects.filter(created_at__date=today).count()
    complaints_this_week = Complaint.objects.filter(created_at__date__gte=week_ago).count()
    pending_verification = Complaint.objects.filter(is_verified=False).count()
    unprocessed = Complaint.objects.filter(ai_processed=False).count()

    # Recent complaints needing attention
    pending_complaints = Complaint.objects.filter(
        is_verified=False
    ).order_by('-created_at')[:10]

    # Category breakdown
    category_data = list(
        Complaint.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # County breakdown (top 10)
    county_data = list(
        Complaint.objects.values('county')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Urgency breakdown
    urgency_data = list(
        Complaint.objects.values('urgency')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Critical and high urgency complaints
    critical_complaints = Complaint.objects.filter(
        urgency__in=['critical', 'high'],
        is_verified=False
    ).order_by('-created_at')[:5]

    context = {
        'total_complaints': total_complaints,
        'complaints_today': complaints_today,
        'complaints_this_week': complaints_this_week,
        'pending_verification': pending_verification,
        'unprocessed': unprocessed,
        'pending_complaints': pending_complaints,
        'category_data': category_data,
        'county_data': county_data,
        'urgency_data': urgency_data,
        'critical_complaints': critical_complaints,
    }

    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_admin, login_url='accounts:login')
def verify_complaint(request, complaint_id):
    """Mark a complaint as verified."""
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.is_verified = True
        complaint.save()
        messages.success(request, f'Complaint {complaint_id} has been verified.')
    except Complaint.DoesNotExist:
        messages.error(request, 'Complaint not found.')

    return redirect('admin_panel:dashboard')
