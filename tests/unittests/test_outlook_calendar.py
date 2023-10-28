import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock

from outlook_event_slack_notification_bot.model import OutlookCalendarApi
from outlook_event_slack_notification_bot.outlook_calendar import OutlookCalendar


class OutlookCalendarTestCase(TestCase):
    outlook_calendar_api: OutlookCalendarApi = OutlookCalendarApi(
        tenant=MagicMock(), client_id=MagicMock(), client_secret=MagicMock()
    )

    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_oidc_access_token(self, msal_confidential_client_application_mock):
        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        self.assertEqual("test", outlook_calendar._get_oidc_access_token())

    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_oidc_access_token_acquire_token_silent_not_possible(
        self, msal_confidential_client_application_mock
    ):
        mock: Mock = Mock()
        mock.acquire_token_silent.side_effect = BaseException
        msal_confidential_client_application_mock.return_value = mock

        with self.assertRaises(BaseException):
            OutlookCalendar(
                outlook_calendar_api=self.outlook_calendar_api
            )

    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_oidc_access_token_acquire_token_for_client_not_possible(
        self, msal_confidential_client_application_mock
    ):
        outlook_calendar_api: OutlookCalendarApi = OutlookCalendarApi(
            tenant=MagicMock(), client_id=MagicMock(), client_secret=MagicMock()
        )
        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = None
        mock.acquire_token_for_client.side_effect = BaseException
        msal_confidential_client_application_mock.return_value = mock

        with self.assertRaises(BaseException):
            OutlookCalendar(
                outlook_calendar_api=outlook_calendar_api
            )

    @patch("outlook_event_slack_notification_bot.outlook_calendar.httpx.Client.get")
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_specific_user_calendar_id(
        self, msal_confidential_client_application_mock, httpx_get_mock
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )
        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        httpx_mock: Mock = Mock()
        httpx_mock.json.return_value = dict(
            {"value": [{"name": "test", "id": "testid"}]}
        )
        httpx_get_mock.return_value = httpx_mock

        self.assertEqual(
            "testid", outlook_calendar._get_specific_user_calendar_id("test", "test")
        )

    @patch("outlook_event_slack_notification_bot.outlook_calendar.httpx.Client.get")
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_specific_user_calendar_id_no_calendars(
        self, msal_confidential_client_application_mock, httpx_get_mock
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        httpx_get_mock.side_effect = ConnectionError

        with self.assertRaises(ConnectionError):
            outlook_calendar._get_specific_user_calendar_id("test", "test")

    @patch("outlook_event_slack_notification_bot.outlook_calendar.httpx.Client.get")
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_specific_user_calendar_id_no_calendars_values(
        self, msal_confidential_client_application_mock, httpx_get_mock
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        httpx_mock: Mock = Mock()
        httpx_mock.json.side_effect = BaseException
        httpx_get_mock.return_value = httpx_mock

        with self.assertRaises(BaseException):
            outlook_calendar._get_specific_user_calendar_id("test", "test")

    @patch("outlook_event_slack_notification_bot.outlook_calendar.httpx.Client.get")
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_specific_user_calendar_id_no_matching_calendar_matching_value(
            self, msal_confidential_client_application_mock, httpx_get_mock
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        httpx_mock: Mock = Mock()
        httpx_mock.json.return_value = dict(
            {"value": [{"name": "test1", "id": "testid"}]}
        )
        httpx_get_mock.return_value = httpx_mock

        self.assertEqual(None, outlook_calendar._get_specific_user_calendar_id("test", "test"))

    @patch("outlook_event_slack_notification_bot.outlook_calendar.httpx.Client.get")
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_events(
        self, msal_confidential_client_application_mock, httpx_get_mock
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        httpx_mock: Mock = Mock()
        httpx_mock.json.return_value = dict(
            {"value": [{"name": "test", "id": "testid"}]}
        )
        httpx_get_mock.return_value = httpx_mock

        self.assertEqual(
            [{"name": "test", "id": "testid"}],
            outlook_calendar.get_events("test", "test"),
        )

    @patch("outlook_event_slack_notification_bot.outlook_calendar.httpx.Client.get")
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.OutlookCalendar._get_specific_user_calendar_id"
    )
    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_events_no_events_available(
        self,
        msal_confidential_client_application_mock,
        get_specific_user_calendar_id_mock,
        httpx_get_mock,
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        get_specific_user_calendar_id_mock.return_value = "test"

        httpx_get_mock.side_effect = ConnectionError

        with self.assertRaises(ConnectionError):
            outlook_calendar.get_events("test", "test")

    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_weekly_events(self, msal_confidential_client_application_mock):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        today: datetime.date = datetime.datetime.now().date().today()
        date: str = f"{today.year}-{today.month}-{today.day + 1}"
        self.assertEqual(
            [{"start": {"dateTime": f"{date}T22:03:01.0000000"}}],
            outlook_calendar.get_weekly_events(
                [{"start": {"dateTime": f"{date}T22:03:01.0000000"}}]
            ),
        )

    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_weekly_events_wrong_event_format(
        self, msal_confidential_client_application_mock
    ):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        with self.assertRaises(BaseException):
            outlook_calendar.get_weekly_events(
                [{"start": {"dateTime": "2023-10-27T22:03.0000000"}}]
            ),

    @patch(
        "outlook_event_slack_notification_bot.outlook_calendar.msal.ConfidentialClientApplication"
    )
    def test_get_weekly_events_no_matching_value(self, msal_confidential_client_application_mock):
        outlook_calendar: OutlookCalendar = OutlookCalendar(
            outlook_calendar_api=self.outlook_calendar_api
        )

        mock: Mock = Mock()
        mock.acquire_token_silent.return_value = dict({"access_token": "test"})
        mock.acquire_token_for_client.return_value = dict({"access_token": "test"})
        msal_confidential_client_application_mock.return_value = mock

        self.assertEqual(
            [],
            outlook_calendar.get_weekly_events(
                [{"start": {"dateTime": f"2023-10-10T22:03:01.0000000"}}]
            ),
        )