from django.apps import AppConfig


class SignalAssignmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "signal_assignment"

    def ready(self):
        import signal_assignment.signals