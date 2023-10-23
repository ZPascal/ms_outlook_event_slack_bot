from dataclasses import dataclass


@dataclass
class SlackAPI:
    """The class includes all necessary variables to establish a connection to the Grafana API endpoints

    Args:
        webhook (str): Specify the host of the Grafana system
        retries (int): Specify the access token of the Grafana system
    """

    webhook: str
    retries: int = 5


@dataclass
class MicrosoftApi:
    """The class includes all necessary variables to establish a connection to the Grafana API endpoints

    Args:
        graph_api_url (str): Specify the host of the Grafana system
        microsoft_login_api (str): Specify the access token of the Grafana system
    """

    graph_api_url: str = "https://graph.microsoft.com"
    microsoft_login_api: str = "https://login.microsoftonline.com"


@dataclass
class OutlookCalendarApi:
    """The class includes all necessary variables to establish a connection to the Grafana API endpoints

    Args:
        tenant (str): Specify the host of the Grafana system
        client_id (str): Specify the access token of the Grafana system
        client_secret (str): Specify the username of the Grafana system
        retries (int): Specify the password of the Grafana system
    """

    tenant: str
    client_id: str
    client_secret: str
    retries: int = 5
    microsoft_api: MicrosoftApi = MicrosoftApi()
