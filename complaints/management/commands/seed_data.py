"""
Management command to seed the database with sample data.
Usage: python manage.py seed_data [--clear]
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from complaints.models import Complaint
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample complaints and users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing data before seeding',
        )

    def handle(self, *args, **options):
        import os
        
        # Check if seeding is enabled via environment variable
        if not os.getenv('SEED_DATA', '').lower() in ('true', '1', 'yes'):
            self.stdout.write(self.style.WARNING('Seeding skipped - SEED_DATA not enabled'))
            return
            
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Complaint.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))

        self.stdout.write('Seeding database...')

        # Create sample users
        users = self.create_users()

        # Create sample complaints
        self.create_complaints(users)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {Complaint.objects.count()} complaints'))

    def create_users(self):
        """Create sample users (citizens and admins)."""
        self.stdout.write('Creating users...')

        users = []

        # Create admin user if doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@sauti.go.ke',
                password='admin123',
                role='admin',
                county='Nairobi',
                first_name='Admin',
                last_name='User'
            )
            users.append(admin)
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))

        # Create sample citizen users
        citizen_data = [
            ('wanjiku', 'Wanjiku', 'Kamau', 'wanjiku@email.com', 'Nairobi', '+254712345678'),
            ('ochieng', 'Peter', 'Ochieng', 'ochieng@email.com', 'Kisumu', '+254723456789'),
            ('akinyi', 'Grace', 'Akinyi', 'akinyi@email.com', 'Mombasa', '+254734567890'),
            ('mutua', 'John', 'Mutua', 'mutua@email.com', 'Machakos', '+254745678901'),
            ('njeri', 'Mary', 'Njeri', 'njeri@email.com', 'Nakuru', '+254756789012'),
        ]

        for username, first_name, last_name, email, county, phone in citizen_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    role='citizen',
                    first_name=first_name,
                    last_name=last_name,
                    county=county,
                    phone_number=phone,
                    accountability_points=random.randint(0, 150)
                )
                users.append(user)

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
        return users

    def create_complaints(self, users):
        """Create sample complaints with realistic Kenyan scenarios."""
        self.stdout.write('Creating complaints...')

        sample_complaints = [
            {
                'raw_text': 'I went to the huduma center in Nairobi to get my ID processed. The officer asked for 500 shillings to "speed up" the process. This is wrong and should be free.',
                'summary': 'Citizen reports bribery at Nairobi Huduma Center where officer demanded KSh 500 to expedite ID processing. Service should be free of charge.',
                'category': 'bribery',
                'county': 'Nairobi',
                'urgency': 'high',
                'sentiment': 'angry',
                'department_name': 'Huduma Center',
                'ai_processed': True,
                'is_verified': True,
            },
            {
                'raw_text': 'The road from Kisumu to Bondo has huge potholes that have caused several accidents. It has been like this for 6 months despite complaints. People are getting hurt.',
                'summary': 'Kisumu-Bondo road has dangerous potholes for 6 months causing accidents. Multiple complaints ignored, public safety at risk.',
                'category': 'infrastructure_damage',
                'county': 'Kisumu',
                'urgency': 'critical',
                'sentiment': 'frustrated',
                'department_name': 'Kenya National Highways Authority',
                'ai_processed': True,
                'is_verified': True,
            },
            {
                'raw_text': 'I applied for a business permit at Mombasa County offices 3 months ago. Still waiting. When I call, they say "come tomorrow" every time. Very frustrating.',
                'summary': 'Business permit application pending for 3 months at Mombasa County with repeated delays and no clear timeline provided.',
                'category': 'delay',
                'county': 'Mombasa',
                'urgency': 'medium',
                'sentiment': 'frustrated',
                'department_name': 'Mombasa County Business Licensing',
                'ai_processed': True,
                'is_verified': False,
            },
            {
                'raw_text': 'Police officer at Machakos station was very rude and shouted at me when I came to report a theft. He refused to file my report saying I was wasting his time.',
                'summary': 'Police officer at Machakos station displayed misconduct by refusing to file theft report and showing hostile behavior towards citizen.',
                'category': 'misconduct',
                'county': 'Machakos',
                'urgency': 'high',
                'sentiment': 'upset',
                'department_name': 'Kenya Police Service - Machakos',
                'officer_name': 'Officer Kimani',
                'ai_processed': True,
                'is_verified': False,
            },
            {
                'raw_text': 'I submitted my land title documents to the lands office in Nakuru for processing. They have now lost my documents and are asking me to bring originals again. This is unacceptable.',
                'summary': 'Nakuru lands office lost submitted land title documents and requesting originals again, causing significant inconvenience.',
                'category': 'lost_documents',
                'county': 'Nakuru',
                'urgency': 'critical',
                'sentiment': 'angry',
                'department_name': 'Lands Office Nakuru',
                'ai_processed': True,
                'is_verified': True,
            },
            {
                'raw_text': 'Water supply in Kibera has been cut for 2 weeks. No communication from the water company. People are suffering and buying expensive water from vendors.',
                'summary': 'Two-week water supply disruption in Kibera without communication from provider, forcing residents to purchase expensive water.',
                'category': 'delay',
                'county': 'Nairobi',
                'urgency': 'critical',
                'sentiment': 'distressed',
                'department_name': 'Nairobi City Water and Sewerage Company',
                'ai_processed': True,
                'is_verified': True,
            },
            {
                'raw_text': 'The chief in our village is allocating land plots to people who pay him bribes. Many of us have been waiting years for our rightful allocations.',
                'summary': 'Village chief allegedly accepting bribes for land plot allocations, disadvantaging legitimate applicants waiting for years.',
                'category': 'corruption',
                'county': 'Kiambu',
                'urgency': 'high',
                'sentiment': 'angry',
                'department_name': 'Local Administration',
                'officer_name': 'Chief Mwangi',
                'ai_processed': True,
                'is_verified': False,
            },
            {
                'raw_text': 'Streetlights on Moi Avenue have not been working for months. The area is now very dark at night and there have been several mugging incidents.',
                'summary': 'Non-functional streetlights on Moi Avenue for months creating unsafe conditions, leading to increase in mugging incidents.',
                'category': 'infrastructure_damage',
                'county': 'Mombasa',
                'urgency': 'high',
                'sentiment': 'concerned',
                'department_name': 'Mombasa County Public Works',
                'ai_processed': True,
                'is_verified': True,
            },
            {
                'raw_text': 'Hospital staff at Kisumu County Hospital demand money before treating emergency patients. My brother was bleeding but they asked for 2000 shillings first.',
                'summary': 'Kisumu County Hospital staff demanding payment before emergency treatment, patient with bleeding injury denied immediate care.',
                'category': 'bribery',
                'county': 'Kisumu',
                'urgency': 'critical',
                'sentiment': 'angry',
                'department_name': 'Kisumu County Hospital',
                'ai_processed': True,
                'is_verified': True,
            },
            {
                'raw_text': 'Garbage has not been collected in our estate for 3 weeks. The piles are getting bigger and starting to smell. Health hazard for our children.',
                'summary': 'Three-week garbage collection failure creating health hazard with accumulating waste in residential estate.',
                'category': 'delay',
                'county': 'Nairobi',
                'urgency': 'high',
                'sentiment': 'concerned',
                'department_name': 'Nairobi City County Environment',
                'ai_processed': True,
                'is_verified': False,
            },
            {
                'raw_text': 'Traffic police on Thika Road constantly stop matatus for no reason and demand bribes. If you don\'t pay, they threaten to impound the vehicle.',
                'summary': 'Traffic police on Thika Road engaging in systematic bribery, threatening matatu operators with vehicle impoundment.',
                'category': 'corruption',
                'county': 'Nairobi',
                'urgency': 'high',
                'sentiment': 'frustrated',
                'department_name': 'Kenya Police Service - Traffic Division',
                'ai_processed': True,
                'is_verified': False,
            },
            {
                'raw_text': 'The county office refused to process my birth certificate because I did not have a "connection" there. They said to come back with someone they know.',
                'summary': 'County office denying birth certificate processing due to lack of personal connections, requiring insider referral.',
                'category': 'corruption',
                'county': 'Kakamega',
                'urgency': 'medium',
                'sentiment': 'frustrated',
                'department_name': 'Kakamega County Registration Office',
                'ai_processed': True,
                'is_verified': False,
            },
        ]

        created_count = 0
        for complaint_data in sample_complaints:
            # Assign random user or make anonymous
            if random.choice([True, False]):
                complaint_data['user'] = random.choice(users)
                complaint_data['is_anonymous'] = False
            else:
                complaint_data['user'] = None
                complaint_data['is_anonymous'] = True

            # Create complaint with backdated creation time for variety
            complaint = Complaint.objects.create(**complaint_data)

            # Backdate some complaints
            days_ago = random.randint(0, 30)
            complaint.created_at = datetime.now() - timedelta(days=days_ago)
            complaint.save()

            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} complaints'))
