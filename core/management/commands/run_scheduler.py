from django.core.management.base import BaseCommand 
from core.tasks import scheduler_instance

class Command(BaseCommand):
    help = 'Run the APScheduler instance continuosly.'

    def handle(self, *args, **kwargs): 
        if not scheduler_instance.running: 
            scheduler_instance.start()
            print("Scheduler started.")
        
        try: 
            while True: 
                pass
        except (KeyboardInterrupt, SystemExit): 
            print("Scheduler stopped.")
            scheduler_instance.shutdown(wait=False)
            