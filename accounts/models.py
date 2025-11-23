from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with citizen/admin roles and profile info."""

    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('admin', 'Administrator'),
    ]

    # Kenyan counties for user location
    COUNTY_CHOICES = [
        ('Baringo', 'Baringo'),
        ('Bomet', 'Bomet'),
        ('Bungoma', 'Bungoma'),
        ('Busia', 'Busia'),
        ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
        ('Embu', 'Embu'),
        ('Garissa', 'Garissa'),
        ('Homa Bay', 'Homa Bay'),
        ('Isiolo', 'Isiolo'),
        ('Kajiado', 'Kajiado'),
        ('Kakamega', 'Kakamega'),
        ('Kericho', 'Kericho'),
        ('Kiambu', 'Kiambu'),
        ('Kilifi', 'Kilifi'),
        ('Kirinyaga', 'Kirinyaga'),
        ('Kisii', 'Kisii'),
        ('Kisumu', 'Kisumu'),
        ('Kitui', 'Kitui'),
        ('Kwale', 'Kwale'),
        ('Laikipia', 'Laikipia'),
        ('Lamu', 'Lamu'),
        ('Machakos', 'Machakos'),
        ('Makueni', 'Makueni'),
        ('Mandera', 'Mandera'),
        ('Marsabit', 'Marsabit'),
        ('Meru', 'Meru'),
        ('Migori', 'Migori'),
        ('Mombasa', 'Mombasa'),
        ('Murang\'a', 'Murang\'a'),
        ('Nairobi', 'Nairobi'),
        ('Nakuru', 'Nakuru'),
        ('Nandi', 'Nandi'),
        ('Narok', 'Narok'),
        ('Nyamira', 'Nyamira'),
        ('Nyandarua', 'Nyandarua'),
        ('Nyeri', 'Nyeri'),
        ('Samburu', 'Samburu'),
        ('Siaya', 'Siaya'),
        ('Taita-Taveta', 'Taita-Taveta'),
        ('Tana River', 'Tana River'),
        ('Tharaka-Nithi', 'Tharaka-Nithi'),
        ('Trans-Nzoia', 'Trans-Nzoia'),
        ('Turkana', 'Turkana'),
        ('Uasin Gishu', 'Uasin Gishu'),
        ('Vihiga', 'Vihiga'),
        ('Wajir', 'Wajir'),
        ('West Pokot', 'West Pokot'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citizen'
    )
    county = models.CharField(
        max_length=50,
        choices=COUNTY_CHOICES,
        blank=True,
        help_text="Your county of residence"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        help_text="Phone number for notifications"
    )
    accountability_points = models.IntegerField(
        default=0,
        help_text="Points earned from civic participation"
    )

    # Profile settings
    receive_notifications = models.BooleanField(
        default=True,
        help_text="Receive email notifications about your complaints"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin_user(self):
        return self.role == 'admin'

    @property
    def is_citizen(self):
        return self.role == 'citizen'
