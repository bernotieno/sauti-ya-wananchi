from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from complaints.models import Complaint


@login_required
def my_complaints(request):
    """View all complaints by the current user."""
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'complaints': complaints,
        'total_count': complaints.count(),
    }
    return render(request, 'citizen/my_complaints.html', context)


@login_required
def citizen_dashboard(request):
    """Personal dashboard for logged-in citizens."""
    user = request.user

    # Get user's complaints (both anonymous and non-anonymous by this user)
    # For anonymous complaints, we can't show them in user dashboard since user=None
    # Only show complaints where user is explicitly set
    my_complaints = Complaint.objects.filter(user=user).order_by('-created_at')[:10]

    # Stats for the user's complaints only
    user_complaints = Complaint.objects.filter(user=user)
    total_complaints = user_complaints.count()
    pending_complaints = user_complaints.filter(ai_processed=False).count()
    verified_complaints = user_complaints.filter(is_verified=True).count()

    # Category breakdown for user's complaints
    category_stats = list(
        user_complaints.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    context = {
        'my_complaints': my_complaints,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'verified_complaints': verified_complaints,
        'category_stats': category_stats,
        'accountability_points': user.accountability_points,
    }

    return render(request, 'citizen/dashboard.html', context)
