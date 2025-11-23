from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from complaints.models import Complaint


@login_required
def citizen_dashboard(request):
    """Personal dashboard for logged-in citizens."""
    user = request.user

    # Get user's complaints (for now, we'll show all complaints since we don't have user FK yet)
    # In a full implementation, you'd filter by user: Complaint.objects.filter(user=user)
    my_complaints = Complaint.objects.all().order_by('-created_at')[:10]

    # Stats for the user
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(ai_processed=False).count()
    verified_complaints = Complaint.objects.filter(is_verified=True).count()

    # Category breakdown
    category_stats = list(
        Complaint.objects.values('category')
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
