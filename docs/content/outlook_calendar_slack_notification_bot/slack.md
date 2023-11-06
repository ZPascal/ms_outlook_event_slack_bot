# Table of Contents

* [slack](#slack)
  * [Slack](#slack.Slack)
    * [send\_slack\_message](#slack.Slack.send_slack_message)

<a id="slack"></a>

# slack

<a id="slack.Slack"></a>

## Slack Objects

```python
class Slack()
```

The class includes all necessary methods to access the Slack endpoints

**Arguments**:

- `slack_api` _SlackAPI_ - Inject a Slack API model object that includes all necessary values and information
- `custom_notification` _bool_ - Specify if the custom notification should be enabled or not (default False)
  

**Attributes**:

- `slack_api` _SlackAPI_ - This is where we store the slack_api
- `custom_notification` _bool_ - This is where we store the custom_notification
- `slack_client` _httpx.Client_ - This is where we store the slack_client

<a id="slack.Slack.send_slack_message"></a>

#### send\_slack\_message

```python
def send_slack_message(events_cw: list,
                       custom_successful_message: str = None,
                       custom_error_message: str = None)
```

The method includes a functionality to send the Slack messages

**Arguments**:

- `events_cw` _list_ - Specify the calendar events
- `custom_successful_message` _str_ - Specify the optional custom successful message (default None)
- `custom_error_message` _str_ - Specify the optional custom error message (default None)
  

**Raises**:

- `ConnectionError` - It is not possible to establish a connection to the endpoint
- `ValueError` - The return value of the Slack API call is not valid
  

**Returns**:

  None

