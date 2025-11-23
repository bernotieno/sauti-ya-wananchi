from django import forms
from .models import Complaint


# Kenyan counties
KENYA_COUNTIES = [
    ('', 'Select County'),
    ('baringo', 'Baringo'),
    ('bomet', 'Bomet'),
    ('bungoma', 'Bungoma'),
    ('busia', 'Busia'),
    ('elgeyo_marakwet', 'Elgeyo Marakwet'),
    ('embu', 'Embu'),
    ('garissa', 'Garissa'),
    ('homa_bay', 'Homa Bay'),
    ('isiolo', 'Isiolo'),
    ('kajiado', 'Kajiado'),
    ('kakamega', 'Kakamega'),
    ('kericho', 'Kericho'),
    ('kiambu', 'Kiambu'),
    ('kilifi', 'Kilifi'),
    ('kirinyaga', 'Kirinyaga'),
    ('kisii', 'Kisii'),
    ('kisumu', 'Kisumu'),
    ('kitui', 'Kitui'),
    ('kwale', 'Kwale'),
    ('laikipia', 'Laikipia'),
    ('lamu', 'Lamu'),
    ('machakos', 'Machakos'),
    ('makueni', 'Makueni'),
    ('mandera', 'Mandera'),
    ('marsabit', 'Marsabit'),
    ('meru', 'Meru'),
    ('migori', 'Migori'),
    ('mombasa', 'Mombasa'),
    ('muranga', "Murang'a"),
    ('nairobi', 'Nairobi'),
    ('nakuru', 'Nakuru'),
    ('nandi', 'Nandi'),
    ('narok', 'Narok'),
    ('nyamira', 'Nyamira'),
    ('nyandarua', 'Nyandarua'),
    ('nyeri', 'Nyeri'),
    ('samburu', 'Samburu'),
    ('siaya', 'Siaya'),
    ('taita_taveta', 'Taita Taveta'),
    ('tana_river', 'Tana River'),
    ('tharaka_nithi', 'Tharaka Nithi'),
    ('trans_nzoia', 'Trans Nzoia'),
    ('turkana', 'Turkana'),
    ('uasin_gishu', 'Uasin Gishu'),
    ('vihiga', 'Vihiga'),
    ('wajir', 'Wajir'),
    ('west_pokot', 'West Pokot'),
]


class ComplaintForm(forms.ModelForm):
    """Form for submitting complaints."""

    county = forms.ChoiceField(
        choices=KENYA_COUNTIES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
        })
    )

    class Meta:
        model = Complaint
        fields = [
            'raw_text',
            'category',
            'county',
            'audio_file',
            'image_file',
            'officer_name',
            'department_name',
        ]
        widgets = {
            'raw_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 5,
                'placeholder': 'Describe your complaint in detail... (English or Swahili)'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'audio/*',
                'id': 'audio-upload'
            }),
            'image_file': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'id': 'image-upload'
            }),
            'officer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Officer name (optional)'
            }),
            'department_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Department name (optional)'
            }),
        }

    def clean_audio_file(self):
        audio = self.cleaned_data.get('audio_file')
        if audio:
            # Check file size (max 10MB)
            if audio.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Audio file must be less than 10MB.")
            # Check content type
            if audio.content_type not in ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/webm']:
                raise forms.ValidationError("Invalid audio format. Use MP3, WAV, OGG, or WebM.")
        return audio

    def clean_image_file(self):
        image = self.cleaned_data.get('image_file')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file must be less than 5MB.")
        return image
