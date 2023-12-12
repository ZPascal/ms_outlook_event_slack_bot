import logging

from .model import OutlookCalendarApi
from datetime import datetime
import httpx
import msal


class OutlookCalendar:
    """The class includes all necessary methods to access the Outlook calendar API endpoints

    Args:
        outlook_calendar_api (OutlookCalendarApi): Inject an Outlook calendar API model object that includes all necessary values and information

    Attributes:
        outlook_calendar_api (OutlookCalendarApi): This is where we store the outlook_calendar_api
        outlook_graph_api_client (httpx.Client): This is where we store the outlook_graph_api_client
        outlook_graph_api_access_token (str): This is where we store the outlook_graph_api_access_token
    """  # noqa: E501

    def __init__(self, outlook_calendar_api: OutlookCalendarApi):
        self.outlook_calendar_api: OutlookCalendarApi = outlook_calendar_api
        transport: httpx.HTTPTransport = httpx.HTTPTransport(
            retries=self.outlook_calendar_api.retries
        )
        self.outlook_graph_api_client: httpx.Client = httpx.Client(
            transport=transport, http2=True
        )
        self.outlook_graph_api_access_token: str = self._get_oidc_access_token()

    def _get_oidc_access_token(self) -> str:
        """The method includes a functionality to get the Microsoft OIDC access token

        Raises:
            BaseException: Unspecified error by executing the API call

        Returns:
            access_token (str): Returns the corresponding access token
        """

        authority: str = (
            f"{self.outlook_calendar_api.microsoft_api.microsoft_login_api}/"
            f"{self.outlook_calendar_api.tenant}"
        )
        app = msal.ConfidentialClientApplication(
            self.outlook_calendar_api.client_id,
            authority=authority,
            client_credential=self.outlook_calendar_api.client_secret,
        )
        try:
            result = app.acquire_token_silent(
                f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/.default",
                account=None,
            )
        except BaseException as e:
            logging.error(
                f"It is not possible to get the OIDC token. Please, check the error: {e}."
            )
            raise e

        try:
            if not result:
                result = app.acquire_token_for_client(
                    scopes=[
                        f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/.default"
                    ]
                )
        except BaseException as e:
            logging.error(
                f"It is not possible to acquire the OIDC token. Please, check the error: {e}."
            )
            raise e

        return result["access_token"]

    def _get_specific_user_calendar_id(self, calendar_name: str, user_id: str) -> str:
        """The method includes a functionality to get a specific calendar id

        Args:
            calendar_name (str): Specify the calendar name
            user_id (str): Specify the user id

        Raises:
            BaseException: Unspecified error by executing the API call
            ConnectionError: It is not possible to establish a connection to the endpoint

        Returns:
            calendar_id (str): Returns the corresponding calendar id
        """

        url: str = f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/v1.0/users/{user_id}/calendars"
        headers: dict = {
            "Authorization": f"Bearer {self.outlook_graph_api_access_token}",
            "Content-Type": "application/json",
        }
        try:
            response: httpx.Response = self.outlook_graph_api_client.get(
                url=url, headers=headers
            )
        except ConnectionError as e:
            logging.error(
                f"It is not possible to get the calendar id. Please, check the error: {e}."
            )
            raise e

        try:
            for calendar in response.json()["value"]:
                if calendar["name"] == calendar_name:
                    return calendar["id"]
        except BaseException as e:
            logging.error(
                f"It is not possible to extract the calendar id. Please, check the error: {e}."
            )
            raise e

    def get_events(self, calendar_name: str, user_id: str) -> list:
        """The method includes a functionality to get the events

        Args:
            calendar_name (str): Specify the calendar name
            user_id (str): Specify the user id

        Raises:
            ConnectionError: It is not possible to establish a connection to the endpoint

        Returns:
            events (list): Returns the corresponding calendar events
        """

        url: str = (
            f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/v1.0/users/{user_id}/calendars/"
            f"{self._get_specific_user_calendar_id(calendar_name, user_id)}/events"
        )
        headers: dict = {
            "Authorization": f"Bearer {self.outlook_graph_api_access_token}",
            "Content-Type": "application/json",
        }
        try:
            response: httpx.Response = self.outlook_graph_api_client.get(
                url=url, headers=headers
            )
        except ConnectionError as e:
            logging.error(
                f"It is not possible to get the calendar events. Please, check the error: {e}."
            )
            raise e

        return response.json()["value"]

    @staticmethod
    def get_weekly_events(events: list) -> list:
        """The method includes a functionality to get the weekly events

        Args:
            events (list): Specify the calendar events

        Raises:
            BaseException: Unspecified error by extracting the datetime information

        Returns:
            events_cw (list): Returns the corresponding weekly calendar events
        """

        today: datetime = datetime.today()
        checked_days: int = 7
        events_cw: list = []

        try:
            for event in events:
                datetime_object_start: datetime = datetime.strptime(
                    event["start"]["dateTime"][0:-1], "%Y-%m-%dT%H:%M:%S.%f"
                )
                datetime_object_end: datetime = datetime.strptime(
                    event["end"]["dateTime"][0:-1], "%Y-%m-%dT%H:%M:%S.%f"
                )
                datetime_object_days_start: int = (datetime_object_start.date() - today.date()).days
                datetime_object_days_end: int = (datetime_object_end.date() - today.date()).days - 1

                if (-1 <= datetime_object_days_start <= checked_days) and (
                        0 <= datetime_object_days_end <= checked_days):
                    events_cw.append(event)
                    events.remove(event)
        except BaseException as e:
            logging.error(
                f"It is not possible to extract the weekly events. Please, check the error: {e}."
            )
            raise e

        return events_cw
