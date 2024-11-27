import os
from datetime import datetime, date

from slack_sdk.web import WebClient

from unittest import TestCase

from outlook_event_slack_notification_bot.model import SlackAPI, OutlookCalendarApi
from outlook_event_slack_notification_bot.outlook_calendar import OutlookCalendar
from outlook_event_slack_notification_bot.slack import Slack


class OutlookCalendarTest(TestCase):
    outlook_calendar_api: SlackAPI = SlackAPI(
        webhook=os.environ["SLACK_WEBHOOK"]
    )
    slack: Slack = Slack(outlook_calendar_api)
    outlook_calendar_api: OutlookCalendarApi = OutlookCalendarApi(
        tenant=os.environ["OUTLOOK_TENANT"], client_id=os.environ["OUTLOOK_CLIENT_ID"],
        client_secret=os.environ["OUTLOOK_CLIENT_SECRET"]
    )
    outlook_calendar: OutlookCalendar = OutlookCalendar(outlook_calendar_api)
    calendar_name: str = os.environ["OUTLOOK_CALENDAR_NAME"]
    calendar_username: str = os.environ["OUTLOOK_CALENDAR_USERNAME"]
    events: list = outlook_calendar.get_events(calendar_name, calendar_username)

    def test_send_slack_message(self):
        target_date: date = datetime(2024, 11, 19).date()
        today: date = date.today()
        channel_id: str = ""

        self.slack.send_slack_message(
            self.outlook_calendar.get_events_by_days(self.events, -(today - target_date).days)
        )

        client = WebClient(os.environ["SLACK_TOKEN"])

        channels: list = client.conversations_list()["channels"]
        for channel in channels:
            if channel["name"] == os.environ["SLACK_CHANNEL_NAME"]:
                channel_id = channel["id"]

        if len(channel_id) == 0:
            raise SystemError

        message: str = client.conversations_history(channel=channel_id)["messages"][0]["text"]
        self.assertEqual("*Events of the week:*\nTest 20-11-2024\n", message)
