from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from complaints.models import Complaint
from accounts.models import CustomUser


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


@login_required
@user_passes_test(is_admin, login_url='accounts:login')
def complaints_list(request):
    """List all complaints with filtering and pagination."""
    complaints = Complaint.objects.all().order_by('-created_at')

    # Filtering
    category_filter = request.GET.get('category', '')
    urgency_filter = request.GET.get('urgency', '')
    verified_filter = request.GET.get('verified', '')
    search_query = request.GET.get('search', '')

    if category_filter:
        complaints = complaints.filter(category=category_filter)

    if urgency_filter:
        complaints = complaints.filter(urgency=urgency_filter)

    if verified_filter == 'yes':
        complaints = complaints.filter(is_verified=True)
    elif verified_filter == 'no':
        complaints = complaints.filter(is_verified=False)

    if search_query:
        complaints = complaints.filter(
            Q(raw_text__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(county__icontains=search_query) |
            Q(officer_name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(complaints, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'urgency_filter': urgency_filter,
        'verified_filter': verified_filter,
        'search_query': search_query,
        'total_count': complaints.count(),
    }

    return render(request, 'admin_panel/complaints_list.html', context)


@login_required
@user_passes_test(is_admin, login_url='accounts:login')
def complaint_detail(request, complaint_id):
    """View and manage a specific complaint."""
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'verify':
            complaint.is_verified = True
            complaint.save()
            messages.success(request, 'Complaint verified successfully.')
        elif action == 'unverify':
            complaint.is_verified = False
            complaint.save()
            messages.success(request, 'Complaint unverified.')
        elif action == 'delete':
            complaint.delete()
            messages.success(request, 'Complaint deleted successfully.')
            return redirect('admin_panel:complaints_list')

    context = {
        'complaint': complaint,
    }

    return render(request, 'admin_panel/complaint_detail.html', context)


@login_required
@user_passes_test(is_admin, login_url='accounts:login')
def users_list(request):
    """List all users with filtering."""
    users = CustomUser.objects.all().order_by('-date_joined')

    # Filtering
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('search', '')

    if role_filter:
        users = users.filter(role=role_filter)

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'role_filter': role_filter,
        'search_query': search_query,
        'total_count': users.count(),
    }

    return render(request, 'admin_panel/users_list.html', context)
