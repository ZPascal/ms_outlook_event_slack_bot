import os
from datetime import date, datetime

from unittest import TestCase

from outlook_event_slack_notification_bot.model import OutlookCalendarApi
from outlook_event_slack_notification_bot.outlook_calendar import OutlookCalendar


class OutlookCalendarTest(TestCase):
    outlook_calendar_api: OutlookCalendarApi = OutlookCalendarApi(
        tenant=os.environ["OUTLOOK_TENANT"], client_id=os.environ["OUTLOOK_CLIENT_ID"],
        client_secret=os.environ["OUTLOOK_CLIENT_SECRET"]
    )
    outlook_calendar: OutlookCalendar = OutlookCalendar(outlook_calendar_api)
    calendar_name: str = os.environ["OUTLOOK_CALENDAR_NAME"]
    calendar_username: str = os.environ["OUTLOOK_CALENDAR_USERNAME"]
    events: list = outlook_calendar.get_events(calendar_name, calendar_username)

    def test_a_get_events(self):
        for event in self.events:
            self.assertEqual("Test", event["subject"])

    def test_b_get_events_by_days(self):
        target_date: date = datetime(2024, 11, 19).date()
        today: date = date.today()

        self.assertEqual("Test",
                         self.outlook_calendar.get_events_by_days(self.events, -(today - target_date).days)[0][
                             "subject"])
