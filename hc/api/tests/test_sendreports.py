import datetime
from hc.api.management.commands.sendreports import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from freezegun import freeze_time
from unittest import mock


class SendReportsTestCase(BaseTestCase):

    def setUp(self):
        super(SendReportsTestCase, self).setUp()
        self.alice.date_joined = datetime.datetime(
            2017, 1, 11, 5, 34, 3
            )
        self.alice.save()

    @mock.patch("hc.api.management.commands.sendreports.num_pinged_checks")
    @freeze_time("2018-01-12 06:33:24", tz_offset=+0)
    def test_handle_one_run_sends_monthly_email(self, mock_pings):
        """
        Test a user who subscribed to monthly reports
        receives a report at the next report date
        """
        self.profile.reports_duration = 30
        self.profile.next_report_date = datetime.datetime(
            2018, 1, 12, 5, 34, 3
            )
        self.profile.save()
        mock_pings.return_value = 1
        result = Command().handle_one_run(30)
        self.assertEqual(result, 1)

    @mock.patch("hc.api.management.commands.sendreports.num_pinged_checks")
    @freeze_time("2017-12-30 06:33:24", tz_offset=+0)
    def test_handle_one_run_does_not_send_monthly_email(self, mock_pings):
        """
        Test a user who subscribed to monthly reports does not receive
        a report until the next report date
        """
        self.profile.reports_duration = 30
        self.profile.next_report_date = datetime.datetime(
            2018, 1, 12, 5, 34, 3
            )
        self.profile.save()
        mock_pings.return_value = 1
        result = Command().handle_one_run(30)
        self.assertEqual(result, 0)

    @mock.patch("hc.api.management.commands.sendreports.num_pinged_checks")
    @freeze_time("2017-12-19 06:33:24", tz_offset=+0)
    def test_handle_one_run_sends_weekly_email(self, mock_pings):
        """
        Test a user who subscribed to weekly reports receives
        a report at the next report date
        """
        self.profile.reports_duration = 7
        self.profile.next_report_date = datetime.datetime(
            2017, 12, 19, 5, 34, 3
            )
        self.profile.save()
        mock_pings.return_value = 1
        result = Command().handle_one_run(7)
        self.assertEqual(result, 1)

    @mock.patch("hc.api.management.commands.sendreports.num_pinged_checks")
    @freeze_time("2017-12-14 06:33:24", tz_offset=+0)
    def test_handle_one_run_does_not_send_weekly_email(self, mock_pings):
        """
        Test a user who subscribed to weekly reports does not receive
        a report until the next report date
        """
        self.profile.reports_duration = 7
        self.profile.next_report_date = datetime.datetime(
            2017, 12, 19, 5, 34, 3
            )
        self.profile.save()
        mock_pings.return_value = 1
        result = Command().handle_one_run(7)
        self.assertEqual(result, 0)

    @mock.patch("hc.api.management.commands.sendreports.num_pinged_checks")
    @freeze_time("2017-12-13 06:33:24", tz_offset=+0)
    def test_handle_one_run_sends_daily_email(self, mock_pings):
        """
        Test a user who subscribed to daily reports receives
        a report at the next report date
        """
        self.profile.reports_duration = 1
        self.profile.next_report_date = datetime.datetime(
            2017, 12, 13, 5, 34, 3
            )
        self.profile.save()
        mock_pings.return_value = 1
        result = Command().handle_one_run(1)
        self.assertEqual(result, 1)

    @mock.patch("hc.api.management.commands.sendreports.num_pinged_checks")
    @freeze_time("2017-12-12 06:33:24", tz_offset=+0)
    def test_one_run_does_not_send_daily_email(self, mock_pings):
        """
        Test a user who subscribed to daily reports does not receive
        a report until the next report date
        """
        self.profile.reports_duration = 1
        self.profile.next_report_date = datetime.datetime(
            2017, 12, 13, 5, 34, 3
            )
        self.profile.save()
        mock_pings.return_value = 1
        result = Command().handle_one_run(1)
        self.assertEqual(result, 0)
