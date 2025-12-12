"""
DEPRECATED: This command has been replaced by populate_real_data and load_excel_data

Use instead:
    python manage.py load_excel_data --file data/Yield_Statistics_Complete_Analysis.xlsx
    python manage.py populate_real_data --clear
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'DEPRECATED - Use populate_real_data and load_excel_data instead'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('=' * 80)
        )
        self.stdout.write(
            self.style.WARNING('This command is DEPRECATED!')
        )
        self.stdout.write(
            self.style.WARNING('=' * 80)
        )
        self.stdout.write('\nTo load real data from Excel, use:\n')
        self.stdout.write(
            self.style.SUCCESS('  python manage.py load_excel_data --file data/Yield_Statistics_Complete_Analysis.xlsx')
        )
        self.stdout.write('\nTo populate YieldData with real statistics, use:\n')
        self.stdout.write(
            self.style.SUCCESS('  python manage.py populate_real_data --clear')
        )
        self.stdout.write('\n' + '=' * 80 + '\n')

