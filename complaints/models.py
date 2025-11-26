import uuid
from django.db import models
from django.conf import settings


class Complaint(models.Model):
    """Core model for citizen complaints."""

    # Category choices
    CATEGORY_CHOICES = [
        ('corruption', 'Corruption'),
        ('delay', 'Delay in Service Delivery'),
        ('bribery', 'Bribery'),
        ('misconduct', 'Misconduct'),
        ('lost_documents', 'Lost Documents'),
        ('infrastructure_damage', 'Infrastructure Damage'),
        ('other', 'Other'),
    ]

    # Urgency choices
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='complaints',
        help_text="User who submitted (null if anonymous)"
    )
    is_anonymous = models.BooleanField(
        default=False,
        help_text="Whether this complaint was submitted anonymously"
    )
    raw_text = models.TextField(
        help_text="Original complaint text or audio transcript"
    )
    summary = models.TextField(
        blank=True,
        help_text="AI-generated 2-3 sentence summary"
    )

    # Classification fields
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    county = models.CharField(
        max_length=100,
        help_text="Kenyan county (e.g., Nairobi, Kisumu)"
    )
    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        default='medium'
    )
    sentiment = models.CharField(
        max_length=50,
        blank=True,
        help_text="Sentiment analysis result"
    )

    # Media attachments
    audio_file = models.FileField(
        upload_to='complaints/audio/',
        blank=True,
        null=True,
        help_text="Voice recording (max 60 seconds)"
    )
    image_file = models.ImageField(
        upload_to='complaints/images/',
        blank=True,
        null=True,
        help_text="Evidence image"
    )

    # Optional identification
    officer_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of officer involved (if mentioned)"
    )
    department_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Department involved (if mentioned)"
    )

    # Processing status
    ai_processed = models.BooleanField(
        default=False,
        help_text="Whether AI processing has been completed"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether complaint has been reviewed by admin"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    def __str__(self):
        return f"{self.category} - {self.county} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def short_summary(self):
        """Return truncated summary for display."""
        if self.summary:
            return self.summary[:150] + '...' if len(self.summary) > 150 else self.summary
        return self.raw_text[:150] + '...' if len(self.raw_text) > 150 else self.raw_text

    @property
    def has_media(self):
        """Check if complaint has any media attachments."""
        return bool(self.audio_file or self.image_file)
