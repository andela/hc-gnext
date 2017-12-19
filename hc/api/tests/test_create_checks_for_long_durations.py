from datetime import timedelta
from freezegun import freeze_time
from django.core.urlresolvers import reverse
from django.test import Client
from hc.test import BaseTestCase
from hc.front.templatetags.hc_extras import YEAR, MONTH


class LongDurationChecksTestCase(BaseTestCase):
    """
    Test checks that have long timeout and grace periods for over one month
    """

    def setUp(self):
        super(LongDurationChecksTestCase, self).setUp()
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.client.login(username=self.alice.email, password="password")
        add_check_url = reverse('hc-add-check')

        # create check
        self.client.post(add_check_url)

        # get check instance.
        self.check = self.alice.check_set.first()

    def test_check_in_grace_period(self):
        # use 3 months as the grace and timeout periods
        self.check.timeout = timedelta(seconds=(MONTH.nsecs * 3))
        self.check.grace = timedelta(seconds=(MONTH.nsecs * 3))
        self.check.save()

        # Ping the check to start monitoring it.
        self.client.get(reverse('hc-ping-slash', args=[self.check.code]))
        self.check.refresh_from_db()

        # assert status of check.
        self.assertEqual(self.check.status, "up")

        # at in_grace, check has entered its grace period
        in_grace = (self.check.last_ping +
                    self.check.timeout + timedelta(seconds=1))

        with freeze_time(in_grace):
            self.check.refresh_from_db()
            self.assertEqual(self.check.get_status(), "up")
            self.assertTrue(self.check.in_grace_period())

    def test_check_is_down_when_no_ping_after_one_year(self):
        # set timeout and grace durations
        self.check.timeout = timedelta(seconds=YEAR.nsecs)
        self.check.grace = timedelta(seconds=YEAR.nsecs)
        self.check.save()

        # make ping: start monitoring the check
        self.client.get(reverse('hc-ping-slash', args=[self.check.code]))
        self.check.refresh_from_db()

        # assert status of check.
        self.assertEqual(self.check.status, "up")

        fail_date = (self.check.last_ping + self.check.timeout +
                     self.check.grace)

        with freeze_time(fail_date):
            self.check.refresh_from_db()
            self.assertFalse(self.check.in_grace_period())
            self.assertEqual(self.check.get_status(), 'down')
