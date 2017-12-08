import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        response = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(response.status_code, 400)
            # Assert that the expected error is the response error
            self.assertIn(str(expected_error), str(response._container))
            
        return response

    def test_it_works(self):
        '''
        checks that pings are working
        '''
        check = Check()
        check.n_pings = 10

        response = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(re.status_code, 201)

        doc = response.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        # Assert the expected last_ping and n_pings value
        self.assertEqual(check.last_ping,None)
        self.assertEqual(check.n_pings,10)

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        '''
        Accepts api into the header
        '''
        # Make the post request and get the response
        payload = json.dumps({"name": "Foo"})
        response = self.client.post(self.URL, payload,content_type="application/json", HTTP_X_API_KEY="abc")
        self.assertEqual(response.status_code, 201)
        

    def test_it_handles_missing_request_body(self):
        '''
        Checks for missing body data in the requests
        '''
        # Make the post request with a missing body and get the response
        response = self.client.post(self.URL, content_type="application/json", HTTP_X_API_KEY="ujyhi")
        self.assertEqual(response.status_code, 400)

    def test_it_handles_invalid_json(self):
        # Make the post request with invalid json data type
        response = self.client.post(self.URL,{'name'},content_type="application/json", HTTP_X_API_KEY="abc")
        self.assertEqual(response.json()["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        '''
        This checks the timeout section if the values are non numeric then returns an error if the values are not intergers(numbers)
        '''
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        '''
        checks that only strings are accepted
        '''
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")
    
    # Test for the assignment of channels
    def test_assign_channels(self):
        check = Check()
        check.user = self.alice
        check.status = "up"
        check.save()

        channel = Channel(user=self.alice)
        channel.kind = "slack"
        channel.value ="http://myexample.com"
        channel.email_verified = True
        channel.save()
        channel.checks.add(check)

        self.assertNotEqual(channel.checks, None)
        self.assertEqual(channel.user, self.alice)

    # Test for the 'timeout is too small' and 'timeout is too large' errors
    def test_timeout_too_small(self):
        self.post({"api_key": "abc", "timeout": 0},
                  expected_error="timeout is too small")

    def test_timeout_too_large(self):
        self.post({"api_key": "abc", "timeout": 99999999},
                  expected_error="timeout is too large")
