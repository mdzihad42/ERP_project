from django.core.management.base import BaseCommand
from apps.management.models import Country, State, City, UnitNumber, Department, Position

class Command(BaseCommand):
    help = 'Seeds the database with initial master data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding initial data...")
        
        # Create Country
        bangladesh, _ = Country.objects.get_or_create(name='Bangladesh', code='BD')
        usa, _ = Country.objects.get_or_create(name='USA', code='US')

        # Create State
        dhaka_div, _ = State.objects.get_or_create(country=bangladesh, name='Dhaka Division')
        ca, _ = State.objects.get_or_create(country=usa, name='California')

        # Create City
        dhaka_city, _ = City.objects.get_or_create(state=dhaka_div, name='Dhaka')
        la, _ = City.objects.get_or_create(state=ca, name='Los Angeles')

        # Create Unit Numbers
        u1, _ = UnitNumber.objects.get_or_create(city=dhaka_city, unit_no='Dhaka-01', description='Main Factory')
        u2, _ = UnitNumber.objects.get_or_create(city=la, unit_no='LA-01', description='Showroom')

        # Create Departments
        hr, _ = Department.objects.get_or_create(unit=u1, name='Human Resources')
        it, _ = Department.objects.get_or_create(unit=u1, name='IT Department')

        # Create Positions
        Position.objects.get_or_create(department=hr, name='HR Manager')
        Position.objects.get_or_create(department=it, name='Lead Developer')

        self.stdout.write(self.style.SUCCESS('Successfully seeded Bavaria ERP database!'))
