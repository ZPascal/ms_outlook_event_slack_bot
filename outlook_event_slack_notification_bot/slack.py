from model import SlackAPI
import httpx
from datetime import datetime


class Slack:
    """The class includes all necessary methods to access the Grafana alerting API endpoints

    Args:
        grafana_api_model (APIModel): Inject a Grafana API model object that includes all necessary values and information

    Attributes:
        grafana_api_model (APIModel): This is where we store the grafana_api_model
    """

    def __init__(self, slack_api: SlackAPI, custom_notification: bool):
        self.slack_api = slack_api
        self.custom_notification = custom_notification
        transport: httpx.HTTPTransport = httpx.HTTPTransport(
            retries=self.slack_api.retries
        )
        self.slack_client = httpx.Client(transport=transport, http2=True)

    def send_slack_message(self, events_cw: list):
        # TODO Update the error message
        notification_message: str = self._create_slack_message(events_cw)
        response: httpx.Response = self.slack_client.post(
            self.slack_api.webhook,
            json={"link_names": True, "text": notification_message},
            headers={"Content-type": "application/json"},
        )

        if response.status_code >= 200:
            print(response.status_code)

    def _create_slack_message(self, events_cw: list) -> str:
        # TODO Error handling
        if len(events_cw) != 0:
            message: str = "*Events of the week:*\n"

            for event_cw in events_cw:
                event_datetime: str = event_cw["start"]["dateTime"][0:-1]
                date: str = (
                    datetime.strptime(event_datetime, "%Y-%m-%dT%H:%M:%S.%f")
                    .date()
                    .strftime("%d-%m-%Y")
                )
                message += f"{event_cw['subject']} {date}\n"
                if self.custom_notification:
                    message += f"{event_cw['bodyPreview']}"
        else:
            message: str = "*There are no events this week*\n"

        return message
