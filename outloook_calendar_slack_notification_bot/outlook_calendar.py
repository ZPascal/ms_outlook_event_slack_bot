from model import OutlookCalendarApi
from datetime import timedelta, datetime
import httpx
import msal


class OutlookCalendar:
    """The class includes all necessary methods to access the Grafana alerting API endpoints

    Args:
        grafana_api_model (APIModel): Inject a Grafana API model object that includes all necessary values and information

    Attributes:
        grafana_api_model (APIModel): This is where we store the grafana_api_model
    """


    def __init__(self, outlook_calendar_api: OutlookCalendarApi):
        self.outlook_calendar_api = outlook_calendar_api
        transport: httpx.HTTPTransport = httpx.HTTPTransport(
            retries=self.outlook_calendar_api.retries
        )
        self.outlook_graph_api_client = httpx.Client(transport=transport, http2=True)
        self.outlook_graph_api_access_token = self._get_oidc_access_token()

    def _get_oidc_access_token(self) -> str:
        # TODO Error handling
        authority: str = (
            f"{self.outlook_calendar_api.microsoft_api.microsoft_login_api}/"
            f"{self.outlook_calendar_api.tenant}"
        )
        app = msal.ConfidentialClientApplication(
            self.outlook_calendar_api.client_id,
            authority=authority,
            client_credential=self.outlook_calendar_api.client_secret,
        )
        result = app.acquire_token_silent(
            f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/.default",
            account=None,
        )
        if not result:
            result = app.acquire_token_for_client(
                scopes=[
                    f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/.default"
                ]
            )

        return result["access_token"]

    def _get_specific_user_calender_id(self, calender_name: str, user_id: str) -> str:
        # TODO Error handling
        url: str = f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/v1.0/users/{user_id}/calendars"
        headers: dict = {
            "Authorization": f"Bearer {self.outlook_graph_api_access_token}",
            "Content-Type": "application/json",
        }
        response: httpx.Response = self.outlook_graph_api_client.get(
            url=url, headers=headers
        )

        for calender in response.json()["value"]:
            if calender["name"] == calender_name:
                return calender["id"]

    def get_daily_events(self, calender_name: str, user_id: str) -> list:
        # TODO Error handling
        url: str = (
            f"{self.outlook_calendar_api.microsoft_api.graph_api_url}/v1.0/users/{user_id}/calendars/"
            f"{self._get_specific_user_calender_id(calender_name, user_id)}/events"
        )
        headers: dict = {
            "Authorization": f"Bearer {self.outlook_graph_api_access_token}",
            "Content-Type": "application/json",
        }
        response: httpx.Response = self.outlook_graph_api_client.get(
            url=url, headers=headers
        )

        return response.json()["value"]

    @staticmethod
    def get_weekly_events(events: list) -> list:
        # TODO Error handling
        today: datetime = datetime.today()
        checked_days: int = 12
        events_cw: list = []

        for event in events:
            datetime_object: datetime = datetime.strptime(
                event["start"]["dateTime"][0:-1], "%Y-%m-%dT%H:%M:%S.%f"
            )
            datetime_object_days: int = (datetime_object.date() - today.date()).days
            if 0 < datetime_object_days <= checked_days:
                events_cw.append(event)
                events.remove(event)

        return events_cw
