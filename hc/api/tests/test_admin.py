from hc.api.models import Channel, Check
from hc.test import BaseTestCase
from hc.api.transports import Pushbullet



class ApiAdminTestCase(BaseTestCase):

    def setUp(self):
        super(ApiAdminTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")
        self.alice.is_staff = True
        self.alice.is_superuser = True
        self.alice.save()
        ### Set Alice to be staff and superuser and save her :)

    def test_it_shows_channel_list_with_pushbullet(self):
        self.client.login(username="alice@example.org", password="password")
        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()
        rsp = ch.notify(self.check)
        self.assertIn('401', rsp)
        ### Assert for the push bullet