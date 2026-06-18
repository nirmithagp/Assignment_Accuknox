import time
import threading
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from signal_assignment.models import TestModel
from signal_assignment import signals


class Command(BaseCommand):
    help = "Demonstrates Django signal behavior for sync, threading, and transactions."

    def handle(self, *args, **options):
        # ----------------------------------------------------------------
        # Question 1: Synchronous vs Asynchronous
        # ----------------------------------------------------------------
        self.stdout.write("\n=== Question 1: Are signals synchronous or asynchronous? ===")

        start = time.time()
        obj = TestModel.objects.create(name="sync-test")
        end = time.time()

        elapsed = end - start
        self.stdout.write(f"  Created TestModel and signal handler ran with 2s sleep.")
        self.stdout.write(f"  Total elapsed time: {elapsed:.2f} seconds")
        if elapsed >= 2:
            self.stdout.write("  => Signal executed SYNCHRONOUSLY (blocked until handler finished)")
        else:
            self.stdout.write("  => Signal executed ASYNCHRONOUSLY")

        # Clean up
        obj.delete()

        # ----------------------------------------------------------------
        # Question 2: Same thread
        # ----------------------------------------------------------------
        self.stdout.write("\n=== Question 2: Do signals run in the same thread as the caller? ===")

        caller_tid = threading.current_thread().ident
        signals.caller_thread_id = None

        obj2 = TestModel.objects.create(name="thread-test")
        receiver_tid = signals.caller_thread_id
        obj2.delete()

        self.stdout.write(f"  Caller thread ID:  {caller_tid}")
        self.stdout.write(f"  Receiver thread ID: {receiver_tid}")
        if caller_tid == receiver_tid:
            self.stdout.write("  => Signal runs in the SAME thread as the caller")
        else:
            self.stdout.write("  => Signal runs in a DIFFERENT thread")

        # ----------------------------------------------------------------
        # Question 3: Same database transaction
        # ----------------------------------------------------------------
        self.stdout.write("\n=== Question 3: Do signals run in the same DB transaction? ===")

        initial_count = TestModel.objects.count()
        self.stdout.write(f"  TestModel count before atomic block: {initial_count}")

        try:
            with transaction.atomic():
                obj3 = TestModel.objects.create(name="tx-test")
                # Inside the atomic block, the post_save handler already ran.
                # We now raise an exception to force a rollback.
                self.stdout.write(f"  TestModel count inside atomic block (after create+signal): {TestModel.objects.count()}")
                raise RuntimeError("Forcing rollback!")
        except RuntimeError:
            pass

        final_count = TestModel.objects.count()
        self.stdout.write(f"  TestModel count after atomic block rollback: {final_count}")
        if final_count == initial_count:
            self.stdout.write("  => Signal runs in the SAME database transaction (all changes rolled back)")
        else:
            self.stdout.write("  => Signal runs in a DIFFERENT database transaction (changes persisted)")
