import logging

from .model import SlackAPI
import httpx
from datetime import datetime


class Slack:
    """The class includes all necessary methods to access the Slack endpoints

    Args:
        slack_api (SlackAPI): Inject a Slack API model object that includes all necessary values and information
        custom_notification (bool): Specify if the custom notification should be enabled or not (default False)

    Attributes:
        slack_api (SlackAPI): This is where we store the slack_api
        custom_notification (bool): This is where we store the custom_notification
        slack_client (httpx.Client): This is where we store the slack_client
    """

    def __init__(self, slack_api: SlackAPI, custom_notification: bool = False):
        self.slack_api: SlackAPI = slack_api
        self.custom_notification: bool = custom_notification
        transport: httpx.HTTPTransport = httpx.HTTPTransport(
            retries=self.slack_api.retries
        )
        self.slack_client: httpx.Client = httpx.Client(transport=transport, http2=True)

    def send_slack_message(self, events_cw: list, custom_successful_message: str = None,
                           custom_error_message: str = None):
        """The method includes a functionality to send the Slack messages

        Args:
            events_cw (list): Specify the calendar events
            custom_successful_message (str): Specify the optional custom successful message (default None)
            custom_error_message (str): Specify the optional custom error message (default None)

        Raises:
            ConnectionError: It is not possible to establish a connection to the endpoint
            ValueError: The return value of the Slack API call is not valid

        Returns:
            None
        """

        notification_message: str = self._create_slack_message(events_cw, custom_successful_message,
                                                               custom_error_message)
        try:
            response: httpx.Response = self.slack_client.post(
                self.slack_api.webhook,
                json={"link_names": True, "text": notification_message},
                headers={"Content-type": "application/json"},
            )
        except ConnectionError as e:
            logging.error(
                f"It is not possible to establish an valid connection. Please, check the error: {e}."
            )
            raise e

        if response.status_code != 200:
            logging.error(
                f"The corresponding return code {response.status_code} of the Slack call is not valid."
            )
            raise ValueError

    def _create_slack_message(self, events_cw: list, custom_successful_message: str = None, custom_error_message: str = None) -> str:
        """The method includes a functionality to create the Slack message

        Args:
            events_cw (list): Specify the calendar events
            custom_successful_message (str): Specify the optional custom successful message (default None)
            custom_error_message (str): Specify the optional custom error message (default None)

        Raises:
            BaseException: Unspecified error by extracting the datetime information

        Returns:
            message (str): Returns the message
        """

        if len(events_cw) != 0:
            message: str = "*Events of the week:*\n"
            if custom_successful_message is not None:
                message: str = f"{custom_successful_message}\n"

            for event_cw in events_cw:
                try:
                    event_datetime: str = event_cw["start"]["dateTime"][0:-1]
                    date: str = (
                        datetime.strptime(event_datetime, "%Y-%m-%dT%H:%M:%S.%f")
                        .date()
                        .strftime("%d-%m-%Y")
                    )
                except BaseException as e:
                    logging.error(
                        f"It is not possible to extract the weekly events. Please, check the error: {e}."
                    )
                    raise e

                message += f"{event_cw['subject']} {date}\n"
                if self.custom_notification:
                    message += f"{event_cw['bodyPreview']}"
        else:
            message: str = "*There are no events this week*\n"
            if custom_error_message is not None:
                message: str = f"{custom_error_message}\n"

        return message
