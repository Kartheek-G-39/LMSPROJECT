# app_name/management/commands/fill_academic_year.py

from django.core.management.base import BaseCommand
from lmsapp.models import Userdata

class Command(BaseCommand):
    help = 'Fill academic year based on roll number for existing Userdata objects'

    def handle(self, *args, **options):
        userdatas = Userdata.objects.all()

        for userdata in userdatas:
            if userdata.rollnumber:
                joining_year = userdata.rollnumber[:2]  # Assuming first two characters represent joining year
                academic_year = f"20{joining_year}-{int(joining_year) + 4}"  # Example: 2021-2025
                userdata.academic_year = academic_year
                userdata.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated academic years for Userdata objects'))
