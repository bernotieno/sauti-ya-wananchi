from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .models import Complaint
from .forms import ComplaintForm
from ai_services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)


class AnonymousComplaintCreateView(CreateView):
    """View for anonymous complaint submission. No login required."""
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/submit_anonymous.html'
    success_url = reverse_lazy('complaints:success')

    def form_valid(self, form):
        # Force anonymous submission
        complaint = form.save(commit=False)
        complaint.is_anonymous = True
        complaint.user = None
        complaint.save()
        self.object = complaint

        # Process complaint with AI
        self._process_complaint_with_ai(complaint)

        # Store complaint ID in session for success page
        self.request.session['last_complaint_id'] = str(complaint.id)

        return redirect(self.success_url)

    def _process_complaint_with_ai(self, complaint):
        """Process complaint using OpenAI services."""
        try:
            ai_service = OpenAIService()

            # Step 1: Transcribe audio if present
            if complaint.audio_file:
                try:
                    logger.info(f"Transcribing audio for complaint {complaint.id}")
                    transcribed_text = ai_service.transcribe_from_file_field(complaint.audio_file)

                    # Append transcription to raw_text or replace if empty
                    if complaint.raw_text:
                        complaint.raw_text += f"\n\n[Audio Transcription]: {transcribed_text}"
                    else:
                        complaint.raw_text = transcribed_text

                    logger.info(f"Audio transcribed successfully for complaint {complaint.id}")
                except Exception as e:
                    logger.error(f"Audio transcription failed for complaint {complaint.id}: {str(e)}")

            # Step 2: Analyze the complaint text
            text_to_analyze = complaint.raw_text
            if text_to_analyze:
                try:
                    logger.info(f"Analyzing complaint {complaint.id}")
                    analysis = ai_service.analyze_complaint(text_to_analyze)

                    # Update complaint with AI analysis
                    complaint.summary = analysis.get('summary', '')
                    complaint.sentiment = analysis.get('sentiment', 'neutral')

                    # Only update category and urgency if not already set by user
                    if not complaint.category or complaint.category == 'other':
                        complaint.category = analysis.get('category', 'other')

                    if not complaint.urgency or complaint.urgency == 'medium':
                        complaint.urgency = analysis.get('urgency', 'medium')

                    # Update county if not set
                    if not complaint.county or complaint.county == 'Unknown':
                        complaint.county = analysis.get('county', 'Unknown')

                    complaint.ai_processed = True
                    logger.info(f"Complaint {complaint.id} analyzed successfully")

                except Exception as e:
                    logger.error(f"AI analysis failed for complaint {complaint.id}: {str(e)}")
                    complaint.ai_processed = False

            # Save the updated complaint
            complaint.save()

        except Exception as e:
            logger.error(f"AI processing failed for complaint {complaint.id}: {str(e)}")
            # Don't fail the submission if AI processing fails
            complaint.ai_processed = False
            complaint.save()


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    """View for submitting new complaints. Requires login."""
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/submit.html'
    success_url = reverse_lazy('complaints:success')
    login_url = 'accounts:login'

    def form_valid(self, form):
        # Set user and anonymous flag before saving
        complaint = form.save(commit=False)
        
        # Handle anonymous submission
        if form.cleaned_data.get('is_anonymous', False):
            complaint.is_anonymous = True
            complaint.user = None  # Don't associate with user for anonymous submissions
        else:
            complaint.is_anonymous = False
            complaint.user = self.request.user
        
        complaint.save()
        self.object = complaint

        # Process complaint with AI
        self._process_complaint_with_ai(complaint)

        # Store complaint ID in session for success page
        self.request.session['last_complaint_id'] = str(complaint.id)

        # Add accountability point to user's account (only for non-anonymous)
        if not complaint.is_anonymous:
            user = self.request.user
            user.accountability_points += 1
            user.save()

        return redirect(self.success_url)

    def _process_complaint_with_ai(self, complaint):
        """Process complaint using OpenAI services."""
        try:
            ai_service = OpenAIService()

            # Step 1: Transcribe audio if present
            if complaint.audio_file:
                try:
                    logger.info(f"Transcribing audio for complaint {complaint.id}")
                    transcribed_text = ai_service.transcribe_from_file_field(complaint.audio_file)

                    # Append transcription to raw_text or replace if empty
                    if complaint.raw_text:
                        complaint.raw_text += f"\n\n[Audio Transcription]: {transcribed_text}"
                    else:
                        complaint.raw_text = transcribed_text

                    logger.info(f"Audio transcribed successfully for complaint {complaint.id}")
                except Exception as e:
                    logger.error(f"Audio transcription failed for complaint {complaint.id}: {str(e)}")

            # Step 2: Analyze the complaint text
            text_to_analyze = complaint.raw_text
            if text_to_analyze:
                try:
                    logger.info(f"Analyzing complaint {complaint.id}")
                    analysis = ai_service.analyze_complaint(text_to_analyze)

                    # Update complaint with AI analysis
                    complaint.summary = analysis.get('summary', '')
                    complaint.sentiment = analysis.get('sentiment', 'neutral')

                    # Only update category and urgency if not already set by user
                    if not complaint.category or complaint.category == 'other':
                        complaint.category = analysis.get('category', 'other')

                    if not complaint.urgency or complaint.urgency == 'medium':
                        complaint.urgency = analysis.get('urgency', 'medium')

                    # Update county if not set
                    if not complaint.county or complaint.county == 'Unknown':
                        complaint.county = analysis.get('county', 'Unknown')

                    complaint.ai_processed = True
                    logger.info(f"Complaint {complaint.id} analyzed successfully")

                except Exception as e:
                    logger.error(f"AI analysis failed for complaint {complaint.id}: {str(e)}")
                    complaint.ai_processed = False

            # Save the updated complaint
            complaint.save()

        except Exception as e:
            logger.error(f"AI processing failed for complaint {complaint.id}: {str(e)}")
            # Don't fail the submission if AI processing fails
            complaint.ai_processed = False
            complaint.save()


class ComplaintDetailView(DetailView):
    """View for displaying individual complaint details."""
    model = Complaint
    context_object_name = 'complaint'
    
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['complaints/detail_dashboard.html']
        return ['complaints/detail.html']


def complaint_success(request):
    """Success page after complaint submission."""
    complaint_id = request.session.get('last_complaint_id')
    complaint = None
    if complaint_id:
        complaint = Complaint.objects.filter(id=complaint_id).first()

    # Handle both logged-in and anonymous users
    context = {
        'complaint': complaint,
    }
    
    if request.user.is_authenticated:
        context['points'] = request.user.accountability_points
    
    template_name = 'complaints/success_dashboard.html' if request.user.is_authenticated else 'complaints/success.html'
    return render(request, template_name, context)


def complaint_card(request, pk):
    """Generate shareable complaint card."""
    complaint = get_object_or_404(Complaint, pk=pk)
    template_name = 'complaints/card_dashboard.html' if request.user.is_authenticated else 'complaints/card.html'
    return render(request, template_name, {
        'complaint': complaint
    })
