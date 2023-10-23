from dataclasses import dataclass


@dataclass
class SlackAPI:
    """The class includes all necessary variables to establish a connection to the Slack channel

    Args:
        webhook (str): Specify the webhook url of the Slack channel
        retries (int): Specify the retries of the forwarding process (default 5)
    """

    webhook: str
    retries: int = 5


@dataclass
class MicrosoftApi:
    """The class includes all necessary variables to establish connections to the Microsoft endpoints

    Args:
        graph_api_url (str): Specify the Microsoft Graph API url (default https://graph.microsoft.com)
        microsoft_login_api (str): Specify the Microsoft login url (default https://login.microsoftonline.com)
    """

    graph_api_url: str = "https://graph.microsoft.com"
    microsoft_login_api: str = "https://login.microsoftonline.com"


@dataclass
class OutlookCalendarApi:
    """The class includes all necessary variables to establish connections the Outlook API endpoints

    Args:
        tenant (str): Specify the Microsoft Tenant
        client_id (str): Specify the Microsoft OAUTH client ID
        client_secret (str): Specify the Microsoft OAUTH client secret
        retries (int): Specify the retries of the process to establish a connection the Outlook API (default 5)
        microsoft_api (MicrosoftApi): Specify the Microsoft APi endpoint urls (default MicrosoftApi())
    """

    tenant: str
    client_id: str
    client_secret: str
    retries: int = 5
    microsoft_api: MicrosoftApi = MicrosoftApi()
