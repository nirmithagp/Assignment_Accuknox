import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from signal_assignment.models import TestModel


# Track thread IDs for proof
caller_thread_id = None


@receiver(post_save, sender=TestModel)
def signal_handler_sync_proof(sender, instance, **kwargs):
    """Sleep to prove synchronous execution."""
    global caller_thread_id
    caller_thread_id = threading.current_thread().ident
    time.sleep(2)

