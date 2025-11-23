from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint


@login_required(login_url='accounts:login')
def dashboard_home(request):
    """Main dashboard view with live feed and analytics."""
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    county_filter = request.GET.get('county', '')
    urgency_filter = request.GET.get('urgency', '')

    # Base queryset
    complaints = Complaint.objects.all()

    # Apply filters
    if category_filter:
        complaints = complaints.filter(category=category_filter)
    if county_filter:
        complaints = complaints.filter(county=county_filter)
    if urgency_filter:
        complaints = complaints.filter(urgency=urgency_filter)

    # Get recent complaints for live feed
    recent_complaints = complaints[:20]

    # Analytics data
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Complaints today
    complaints_today = Complaint.objects.filter(
        created_at__date=today
    ).count()

    # Total complaints
    total_complaints = Complaint.objects.count()

    # Complaints by category
    category_data = list(
        Complaint.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Complaints by county (top 10)
    county_data = list(
        Complaint.objects.values('county')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Complaints trend (last 7 days)
    trend_data = list(
        Complaint.objects.filter(created_at__date__gte=week_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Urgency breakdown
    urgency_data = list(
        Complaint.objects.values('urgency')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Get unique counties and categories for filters
    counties = Complaint.objects.values_list('county', flat=True).distinct().order_by('county')
    categories = [choice[0] for choice in Complaint.CATEGORY_CHOICES]
    urgencies = [choice[0] for choice in Complaint.URGENCY_CHOICES]

    context = {
        'complaints': recent_complaints,
        'complaints_today': complaints_today,
        'total_complaints': total_complaints,
        'category_data': category_data,
        'county_data': county_data,
        'trend_data': trend_data,
        'urgency_data': urgency_data,
        'counties': counties,
        'categories': categories,
        'urgencies': urgencies,
        'current_filters': {
            'category': category_filter,
            'county': county_filter,
            'urgency': urgency_filter,
        }
    }

    return render(request, 'dashboard/home.html', context)


def analytics_api(request):
    """API endpoint for dashboard charts (JSON response)."""
    from django.http import JsonResponse

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Category data
    category_data = list(
        Complaint.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # County data
    county_data = list(
        Complaint.objects.values('county')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Trend data
    trend_data = list(
        Complaint.objects.filter(created_at__date__gte=week_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Convert dates to strings for JSON
    for item in trend_data:
        item['date'] = item['date'].strftime('%Y-%m-%d')

    return JsonResponse({
        'category_data': category_data,
        'county_data': county_data,
        'trend_data': trend_data,
        'total': Complaint.objects.count(),
        'today': Complaint.objects.filter(created_at__date=today).count(),
    })
