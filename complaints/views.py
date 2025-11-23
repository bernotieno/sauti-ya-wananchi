from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .models import Complaint
from .forms import ComplaintForm


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    """View for submitting new complaints. Requires login."""
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/submit.html'
    success_url = reverse_lazy('complaints:success')
    login_url = 'accounts:login'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Store complaint ID in session for success page
        self.request.session['last_complaint_id'] = str(self.object.id)
        # Add accountability point to user's account
        user = self.request.user
        user.accountability_points += 1
        user.save()
        return response


class ComplaintDetailView(DetailView):
    """View for displaying individual complaint details."""
    model = Complaint
    template_name = 'complaints/detail.html'
    context_object_name = 'complaint'


@login_required(login_url='accounts:login')
def complaint_success(request):
    """Success page after complaint submission."""
    complaint_id = request.session.get('last_complaint_id')
    complaint = None
    if complaint_id:
        complaint = Complaint.objects.filter(id=complaint_id).first()

    return render(request, 'complaints/success.html', {
        'complaint': complaint,
        'points': request.user.accountability_points
    })


def complaint_card(request, pk):
    """Generate shareable complaint card."""
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaints/card.html', {
        'complaint': complaint
    })
