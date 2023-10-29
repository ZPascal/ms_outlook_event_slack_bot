# Microsoft Outlook Event API Slack Bot
The repository includes a Python-based Slack Bot for MS Outlook events.

## Functionality

The application allows accessing shared calendars of a user and reading the corresponding weekly events via Microsoft API calls. In the next step, it is possible to send this event in the form of a Slack message to a connected Slack channel.

## Installation

`pip install outlook-event-slack-bot`

## Example of use

```python
import argparse

from outlook_event_slack_notification_bot.model import SlackAPI, OutlookCalendarApi
from outlook_event_slack_notification_bot.slack import Slack
from outlook_event_slack_notification_bot.outlook_calendar import OutlookCalendar


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to extract a user's Outlook calendar events and "
                                                 "forward them to a Slack channel.")
    parser.add_argument("-wh", "--webhook", type=str, required=True, help="Get the Slack webhook")
    parser.add_argument("-t", "--tenant", type=str, required=True, help="Get the Microsoft tenant")
    parser.add_argument("-ci", "--client-id", type=str, required=True, help="Get the Microsoft OAuth Client ID")
    parser.add_argument("-cs", "--client-secret", type=str, required=True, help="Get the Microsoft OAuth Client secret")
    parser.add_argument("-scu", "--shared_calendar_user", type=str, required=True,
                        help="Get the Outlook shared calendar user")
    parser.add_argument("-scn", "--shared_calendar_name", type=str, required=True,
                        help="Get the Outlook shared calendar name")
    parser.add_argument("-cn", "--custom_notification", type=str, required=True,
                        help="Should be custom notifications send to the corresponding users, "
                             "defined Outlook calendar event body?")
    args = parser.parse_args()

    outlook_calendar_api: OutlookCalendarApi = OutlookCalendarApi(
        tenant=args.tenant, client_id=args.client_id, client_secret=args.client_secret
    )
    outlook_calendar: OutlookCalendar = OutlookCalendar(outlook_calendar_api)
    events: list = outlook_calendar.get_events(
        args.shared_calendar_name, args.shared_calendar_user
    )
    events_cw: list = outlook_calendar.get_weekly_events(events)
    Slack(SlackAPI(args.webhook), args.custom_notification).send_slack_message(events_cw)
```

## Optimization potential:
- [ ] Add Integration tests

## Contribution
If you would like to contribute something, have an improvement request, or want to make a change inside the code, please open a pull request.

## Support
If you need support, or you encounter a bug, please don't hesitate to open an issue.

## Donations
If you would like to support my work, I ask you to take an unusual action inside the open source community. Donate the money to a non-profit organization like Doctors Without Borders or the Children's Cancer Aid. I will continue to build tools because I like it and it is my passion to develop and share applications.

## License
This product is available under the Apache 2.0 license.