# Table of Contents

* [model](#model)
  * [SlackAPI](#model.SlackAPI)
  * [MicrosoftApi](#model.MicrosoftApi)
  * [OutlookCalendarApi](#model.OutlookCalendarApi)

<a id="model"></a>

# model

<a id="model.SlackAPI"></a>

## SlackAPI Objects

```python
@dataclass
class SlackAPI()
```

The class includes all necessary variables to establish a connection to the Slack channel

**Arguments**:

- `webhook` _str_ - Specify the webhook url of the Slack channel
- `retries` _int_ - Specify the retries of the forwarding process (default 5)

<a id="model.MicrosoftApi"></a>

## MicrosoftApi Objects

```python
@dataclass
class MicrosoftApi()
```

The class includes all necessary variables to establish connections to the Microsoft endpoints

**Arguments**:

- `graph_api_url` _str_ - Specify the Microsoft Graph API url (default https://graph.microsoft.com)
- `microsoft_login_api` _str_ - Specify the Microsoft login url (default https://login.microsoftonline.com)

<a id="model.OutlookCalendarApi"></a>

## OutlookCalendarApi Objects

```python
@dataclass
class OutlookCalendarApi()
```

The class includes all necessary variables to establish connections the Outlook API endpoints

**Arguments**:

- `tenant` _str_ - Specify the Microsoft Tenant
- `client_id` _str_ - Specify the Microsoft OAUTH client ID
- `client_secret` _str_ - Specify the Microsoft OAUTH client secret
- `retries` _int_ - Specify the retries of the process to establish a connection the Outlook API (default 5)
- `microsoft_api` _MicrosoftApi_ - Specify the Microsoft APi endpoint urls (default MicrosoftApi())

