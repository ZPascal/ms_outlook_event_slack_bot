from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock

from outlook_event_slack_notification_bot.model import SlackAPI
from outlook_event_slack_notification_bot.slack import Slack


class SlackTestCase(TestCase):
    slack_api: SlackAPI = SlackAPI(webhook=MagicMock())
    slack: Slack = Slack(slack_api)

    @patch("outlook_event_slack_notification_bot.slack.httpx.Client.post")
    def test_send_slack_message(self, httpx_post_mock):
        slack_api: SlackAPI = SlackAPI(webhook="test")
        slack: Slack = Slack(slack_api)

        httpx_mock: Mock = Mock()
        httpx_mock.status_code = 200
        httpx_post_mock.return_value = httpx_mock

        self.assertEqual(None,
                         slack.send_slack_message([
                             {"name": "test", "start":
                             {"dateTime": "2023-10-27T22:03:01.0000000"},
                              "id": "testid",
                              "subject": "Test"
                              }])
                         )

    @patch("outlook_event_slack_notification_bot.slack.httpx.Client.post")
    def test_send_slack_message_connection_not_possible(self, httpx_post_mock):
        slack_api: SlackAPI = SlackAPI(webhook="test")
        slack: Slack = Slack(slack_api)

        httpx_post_mock.side_effect = ConnectionError

        with self.assertRaises(ConnectionError):
            slack.send_slack_message([
                {"name": "test", "start":
                    {"dateTime": "2023-10-27T22:03:01.0000000"},
                 "id": "testid",
                 "subject": "Test"
                 }])

    @patch("outlook_event_slack_notification_bot.slack.httpx.Client.post")
    def test_send_slack_message_send_not_possible(self, httpx_post_mock):
        slack_api: SlackAPI = SlackAPI(webhook="test")
        slack: Slack = Slack(slack_api)

        httpx_mock: Mock = Mock()
        httpx_mock.status_code = 400
        httpx_post_mock.return_value = httpx_mock

        with self.assertRaises(ValueError):
            slack.send_slack_message([
                {"name": "test", "start":
                    {"dateTime": "2023-10-27T22:03:01.0000000"},
                 "id": "testid",
                 "subject": "Test"
                 }])

    def test_create_slack_message(self):
        self.assertEqual("*Events of the week:*\nTest 27-10-2023\n",
                         self.slack._create_slack_message([
                             {"name": "test", "start":
                             {"dateTime": "2023-10-27T22:03:01.0000000"},
                              "id": "testid",
                              "subject": "Test"
                              }])
                         )

    def test_create_slack_message_custom_notification(self):
        slack: Slack = Slack(self.slack_api, custom_notification=True)
        self.assertEqual("*Events of the week:*\nTest 27-10-2023\n@test",
                         slack._create_slack_message([
                             {"name": "test", "start":
                             {"dateTime": "2023-10-27T22:03:01.0000000"},
                              "id": "testid",
                              "subject": "Test",
                              "bodyPreview": "@test"
                              }])
                         )

    def test_create_slack_message_no_events_this_week(self):
        self.assertEqual("*There are no events this week*\n",
                         self.slack._create_slack_message([])
                         )

    def test_create_slack_message_wrong_event_datetime_format(self):
        with self.assertRaises(BaseException):
         self.slack._create_slack_message([
             {"name": "test", "start":
             {"dateTime": "2023:10:27T22:03:01.0000000"},
              "id": "testid",
              "subject": "Test"
              }])