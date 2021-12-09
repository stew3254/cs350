from majorizer.classes import *
from majorizer.models import *
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Just running a test while the program is running'

    def handle(self, *args, **kwargs):
        try:
            test_department, _ = DBDepartment.objects.get_or_create(name="Test Department")
            d = Department(test_department)
            print(d.db())
        except Exception as e:
            raise CommandError(f'Initalization failed due to error: {e}')

