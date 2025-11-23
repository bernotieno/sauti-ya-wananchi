from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from complaints.models import Complaint


def landing_page(request):
    """Landing page with hero, stats, and overview."""
    # Get statistics for the landing page
    total_complaints = Complaint.objects.count()
    resolved_complaints = Complaint.objects.filter(is_verified=True).count()
    counties_covered = Complaint.objects.values('county').distinct().count()

    # Get recent complaints for preview (only verified ones)
    recent_complaints = Complaint.objects.filter(
        ai_processed=True
    ).order_by('-created_at')[:5]

    context = {
        'total_complaints': total_complaints,
        'resolved_complaints': resolved_complaints,
        'counties_covered': counties_covered,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'pages/landing.html', context)


def about_page(request):
    """About page with mission, vision, and how it works."""
    # Get some stats for the about page
    total_complaints = Complaint.objects.count()

    context = {
        'total_complaints': total_complaints,
    }
    return render(request, 'pages/about.html', context)


def contact_page(request):
    """Contact page with form."""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        if name and email and message:
            # In production, you would send an email here
            # send_mail(
            #     f'Contact Form: {subject}',
            #     f'From: {name} ({email})\n\n{message}',
            #     email,
            #     [settings.DEFAULT_FROM_EMAIL],
            # )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'pages/contact.html')
