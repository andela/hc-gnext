import logging
import time

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from hc.api.models import Check
from hc.lib import emails

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends escalation messages to a group of users'

    def handle_many(self):
        """ Send escalation emails for many checks at once """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down = query.filter(alert_after__lt=now, status="up")
        going_up = query.filter(alert_after__gt=now, status="down")
        needs_escalation = query.filter(
            escalate_after__lt=now, status='down', is_high_priority=True)

        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down.iterator()) + list(going_up.iterator()) +\
            list(needs_escalation.iterator())

        if not checks:
            return False

        futures = [executor.submit(self.escalate_one, check)
                   for check in checks]
        for future in futures:
            future.result()

        return True

    def escalate_one(self, check):
        check.status = check.get_status()
        check.save()  # save the status

        if check.status == "down":
            check.escalate_after = (
                timezone.now() + check.interval + check.interval)
        check.save()  # save the escalate_after field

        tmpl = "\nSending escalated alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))

        emails.escalate(check.emails_list(), ctx={
                        "check": check, "now": timezone.now()})
        connection.close()
        return True

    def handle(self, *args, **options):
        self.stdout.write("escalatechecks is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)
