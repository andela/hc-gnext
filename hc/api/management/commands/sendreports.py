from datetime import timedelta
import time

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from hc.accounts.models import Profile
from hc.api.models import Check


def num_pinged_checks(profile):
    q = Check.objects.filter(user_id=profile.user.id,)
    q = q.filter(last_ping__isnull=False)
    return q.count()


class Command(BaseCommand):
    help = 'Send due monthly reports'
    tmpl = "Sending due report to %s"

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            dest='loop',
            default=False,
            help='Keep running indefinitely in a 300 second wait loop',
        )

    def handle_one_run(self, days):
        now = timezone.now()
        time_before = now - timedelta(days=days)

        report_due = Q(next_report_date__lt=now)
        report_not_scheduled = Q(next_report_date__isnull=True)

        q = Profile.objects.filter(report_due | report_not_scheduled)
        q = q.filter(reports_allowed=True)
        q = q.filter(reports_duration=days)
        q = q.filter(user__date_joined__lt=time_before)
        sent = 0
        for profile in q:
            if num_pinged_checks(profile) > 0:
                self.stdout.write(self.tmpl % profile.user.email)
                profile.send_report()
                sent += 1
        return sent

    def handle(self, *args, **options):
        choices = [1, 7, 30]
        if not options["loop"]:
            reports = 0
            for choice in choices:
                reports += self.handle_one_run(choice)
            return "Sent %d report(s)" % reports

        self.stdout.write("sendreports is now running")
        while True:

            for choice in choices:
                reports += self.handle_one_run(choice)

            formatted = timezone.now().isoformat()
            self.stdout.write("-- MARK %s --" % formatted)

            time.sleep(300)
