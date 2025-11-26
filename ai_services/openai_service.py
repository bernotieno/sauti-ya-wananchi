"""OpenAI API service for audio transcription and complaint analysis."""
import json
from openai import OpenAI
from django.conf import settings


class OpenAIService:
    """Service for processing complaints using OpenAI API."""

    # Kenyan counties for validation
    KENYAN_COUNTIES = [
        'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika',
        'Malindi', 'Kitale', 'Garissa', 'Kakamega', 'Machakos', 'Meru',
        'Nyeri', 'Kiambu', 'Kajiado', 'Narok', 'Murang\'a', 'Embu',
        'Kericho', 'Migori', 'Siaya', 'Kisii', 'Bungoma', 'Busia',
        'Vihiga', 'Bomet', 'Homa Bay', 'Turkana', 'West Pokot', 'Samburu',
        'Trans Nzoia', 'Uasin Gishu', 'Elgeyo Marakwet', 'Nandi', 'Baringo',
        'Laikipia', 'Nyandarua', 'Nyamira', 'Kirinyaga', 'Makueni',
        'Tharaka Nithi', 'Kitui', 'Marsabit', 'Isiolo', 'Wajir', 'Mandera',
        'Taita Taveta', 'Kwale', 'Kilifi', 'Lamu', 'Tana River'
    ]

    def __init__(self):
        """Initialize OpenAI client with API key from settings."""
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in settings")
        self.client = OpenAI(api_key=api_key)

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text using Whisper API.

        Args:
            audio_file_path: Path to audio file or file object

        Returns:
            str: Transcribed text

        Raises:
            Exception: If transcription fails
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Can be 'sw' for Swahili or auto-detect
                )
            return transcript.text
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")

    def transcribe_from_file_field(self, file_field):
        """
        Transcribe audio from Django FileField.

        Args:
            file_field: Django FileField object

        Returns:
            str: Transcribed text
        """
        if not file_field:
            raise ValueError("No audio file provided")

        # Get the actual file path
        file_path = file_field.path
        return self.transcribe_audio(file_path)

    def analyze_complaint(self, complaint_text):
        """
        Analyze complaint text and extract structured information using GPT.

        Args:
            complaint_text: The complaint text to analyze

        Returns:
            dict: Contains summary, category, urgency, county, sentiment
        """
        prompt = f"""Analyze this complaint from a Kenyan citizen and extract the following information:

Complaint text: {complaint_text}

Please provide your analysis in the following JSON format:
{{
    "summary": "A clear 2-3 sentence summary of the complaint",
    "category": "one of: corruption, delay, bribery, misconduct, lost_documents, infrastructure_damage, other",
    "urgency": "one of: low, medium, high, critical",
    "county": "The Kenyan county mentioned (or 'Unknown' if not specified)",
    "sentiment": "negative, neutral, or positive"
}}

Guidelines:
- Summary should be professional and concise
- Category should best match the nature of the complaint
- Urgency should reflect the severity and time-sensitivity
- County should be a valid Kenyan county name
- Sentiment should reflect the emotional tone

Respond ONLY with the JSON object, no additional text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that analyzes civic complaints from Kenyan citizens. You extract key information and provide structured analysis."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            # Extract and parse JSON response
            response_text = response.choices[0].message.content
            analysis = json.loads(response_text)

            # Validate and clean the response
            return self._validate_analysis(analysis)

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI analysis failed: {str(e)}")

    def _validate_analysis(self, analysis):
        """Validate and clean the analysis response."""
        valid_categories = [
            'corruption', 'delay', 'bribery', 'misconduct',
            'lost_documents', 'infrastructure_damage', 'other'
        ]
        valid_urgencies = ['low', 'medium', 'high', 'critical']
        valid_sentiments = ['negative', 'neutral', 'positive']

        # Ensure category is valid
        if analysis.get('category') not in valid_categories:
            analysis['category'] = 'other'

        # Ensure urgency is valid
        if analysis.get('urgency') not in valid_urgencies:
            analysis['urgency'] = 'medium'

        # Ensure sentiment is valid
        if analysis.get('sentiment') not in valid_sentiments:
            analysis['sentiment'] = 'neutral'

        # Validate county (case-insensitive match)
        county = analysis.get('county', 'Unknown')
        county_match = next(
            (c for c in self.KENYAN_COUNTIES if c.lower() == county.lower()),
            'Unknown'
        )
        analysis['county'] = county_match

        return analysis

    def summarize_text(self, text):
        """
        Generate a concise summary of the complaint text.

        Args:
            text: The text to summarize

        Returns:
            str: 2-3 sentence summary
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that summarizes civic complaints concisely and professionally."},
                    {"role": "user", "content": f"Summarize this complaint in 2-3 clear, professional sentences:\n\n{text}"}
                ],
                temperature=0.3,
                max_tokens=256
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI summarization failed: {str(e)}")
