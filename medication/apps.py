from django.apps import AppConfig

class MedicationConfig(AppConfig):
    name = 'medication'

    def ready(self):
        import medication.signals
