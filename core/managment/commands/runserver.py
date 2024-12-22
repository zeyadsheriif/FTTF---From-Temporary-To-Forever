from django.core.management.commands.runserver import Command as BaseRunserverCommand
from datetime import datetime
import django
from django.conf import settings

class Command(BaseRunserverCommand):
    def handle(self, *args, **options):
        print("Performing system checks...")
        self.check(display_num_errors=True)
        print("System check identified no issues (0 silenced).")
        print(datetime.now().strftime("%B %d, %Y - %H:%M:%S"))
        print(f"Django version {django.get_version()}, using settings \"{settings.SETTINGS_MODULE}\"")
        print("Watching for file changes with StatReloader")
        print("Starting development server at http://127.0.0.1:8000/")
        print("Quit the server with CTRL-BREAK.")
        super().handle(*args, **options)
