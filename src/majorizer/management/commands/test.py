from majorizer.serializers import *
from majorizer.classes import *
from majorizer.models import *
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Just running a test while the program is running'

    def handle(self, *args, **kwargs):
        try:
            test_schedule = DBSchedule.objects.filter(name="Test Schedule")[0]
            serial = ScheduleSerializer(test_schedule)
            print(serial.data)
        except Exception as e:
            raise CommandError(f'Initalization failed due to error: {e}')

