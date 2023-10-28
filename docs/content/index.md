# Microsoft Outlook Event API Slack Bot
The repository includes a Python-based Slack Bot for MS Outlook events

# TODO for the first pre-release:
- [ ] Unit tests
- [ ] Documentation
- [x] Error handling

# TODO for the first release:
- [ ] Integration tests

## Functionality


## Installation

`pip install outlook-event-slack-bot`

## Example

```python
import argparse

from outlook_event_slack_notification_bot.model import SlackAPI, OutlookCalendarApi
from outlook_event_slack_notification_bot.slack import Slack
from outlook_event_slack_notification_bot.outlook_calendar import OutlookCalendar


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local script to get the IP address of the "
                                                 "local machine and forward it.")
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
