from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    def setUp(self):
        super(AddCheckTestCase, self).setUp()
        self.client.login(username="alice@example.org", password="password")
        self.url = "/checks/add/"

    def test_it_works(self):
        r = self.client.post(self.url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    def test_team_access(self):
        """ Tests if a check can be viewed by members on a
         team where by one member has team_access.
        """

        # creates an unnamed check on the Alice profile
        resp = self.client.post(self.url)
        self.assertRedirects(resp, "/checks/")
        alice_checks = Check.objects.filter(user=self.alice)
        self.client.logout()  # destroy the current session

        self.client.login(username="bob@example.org", password="password")

        resp = self.client.get("/checks/")
        # UUID of alice's check present in the URL
        self.assertContains(resp, alice_checks.first().code)
        self.assertIn(str(alice_checks.first().code), str(resp.content))
        self.client.logout()

        # Since Charlie has no team access, on getting the `/checks/` page,
        # `You don't have any checks yet.` should be displayed
        self.client.login(username="charlie@example.org", password="password")
        resp = self.client.get("/checks/")
        self.assertContains(resp, "You don't have any checks yet.")
        self.client.logout()
