"""Management command to process complaints with AI in batch."""
from django.core.management.base import BaseCommand
from complaints.models import Complaint
from ai_services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process unprocessed complaints with AI (transcription and analysis)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of complaints to process (default: 10)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Reprocess all complaints, even if already processed'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        force = options['force']

        # Get complaints to process
        if force:
            complaints = Complaint.objects.all()[:limit]
            self.stdout.write(f"Reprocessing {complaints.count()} complaints (forced)...")
        else:
            complaints = Complaint.objects.filter(ai_processed=False)[:limit]
            self.stdout.write(f"Processing {complaints.count()} unprocessed complaints...")

        if not complaints.exists():
            self.stdout.write(self.style.SUCCESS('No complaints to process.'))
            return

        # Initialize AI service
        try:
            ai_service = OpenAIService()
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Failed to initialize AI service: {str(e)}'))
            return

        # Process each complaint
        processed_count = 0
        failed_count = 0

        for complaint in complaints:
            try:
                self.stdout.write(f'Processing complaint {complaint.id}...')
                self._process_complaint(complaint, ai_service)
                processed_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Complaint {complaint.id} processed'))
            except Exception as e:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to process {complaint.id}: {str(e)}'))

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Successfully processed: {processed_count}'))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f'Failed: {failed_count}'))
        self.stdout.write('='*50)

    def _process_complaint(self, complaint, ai_service):
        """Process a single complaint with AI."""

        # Step 1: Transcribe audio if present and not already transcribed
        if complaint.audio_file and '[Audio Transcription]' not in complaint.raw_text:
            try:
                logger.info(f"Transcribing audio for complaint {complaint.id}")
                transcribed_text = ai_service.transcribe_from_file_field(complaint.audio_file)

                # Append transcription to raw_text or replace if empty
                if complaint.raw_text:
                    complaint.raw_text += f"\n\n[Audio Transcription]: {transcribed_text}"
                else:
                    complaint.raw_text = transcribed_text

                self.stdout.write(f'  - Audio transcribed')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  - Audio transcription failed: {str(e)}'))

        # Step 2: Analyze the complaint text
        if complaint.raw_text:
            try:
                logger.info(f"Analyzing complaint {complaint.id}")
                analysis = ai_service.analyze_complaint(complaint.raw_text)

                # Update complaint with AI analysis
                complaint.summary = analysis.get('summary', '')
                complaint.sentiment = analysis.get('sentiment', 'neutral')

                # Update category and urgency from AI if not specifically set
                if not complaint.category or complaint.category == 'other':
                    complaint.category = analysis.get('category', 'other')

                if not complaint.urgency or complaint.urgency == 'medium':
                    complaint.urgency = analysis.get('urgency', 'medium')

                # Update county if not set
                if not complaint.county or complaint.county == 'Unknown':
                    complaint.county = analysis.get('county', 'Unknown')

                complaint.ai_processed = True
                self.stdout.write(f'  - Analysis complete: {complaint.category} / {complaint.urgency}')

            except Exception as e:
                complaint.ai_processed = False
                raise Exception(f'Analysis failed: {str(e)}')

        # Save the updated complaint
        complaint.save()
