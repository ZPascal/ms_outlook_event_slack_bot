# Table of Contents

* [outlook\_calendar](#outlook_calendar)
  * [OutlookCalendar](#outlook_calendar.OutlookCalendar)
    * [get\_events](#outlook_calendar.OutlookCalendar.get_events)
    * [get\_weekly\_events](#outlook_calendar.OutlookCalendar.get_weekly_events)

<a id="outlook_calendar"></a>

# outlook\_calendar

<a id="outlook_calendar.OutlookCalendar"></a>

## OutlookCalendar Objects

```python
class OutlookCalendar()
```

The class includes all necessary methods to access the Outlook calendar API endpoints

**Arguments**:

- `outlook_calendar_api` _OutlookCalendarApi_ - Inject an Outlook calendar API model object that includes all necessary values and information
  

**Attributes**:

- `outlook_calendar_api` _OutlookCalendarApi_ - This is where we store the outlook_calendar_api
- `outlook_graph_api_client` _httpx.Client_ - This is where we store the outlook_graph_api_client
- `outlook_graph_api_access_token` _str_ - This is where we store the outlook_graph_api_access_token

<a id="outlook_calendar.OutlookCalendar.get_events"></a>

#### get\_events

```python
def get_events(calendar_name: str, user_id: str) -> list
```

The method includes a functionality to get the events

**Arguments**:

- `calendar_name` _str_ - Specify the calendar name
- `user_id` _str_ - Specify the user id
  

**Raises**:

- `ConnectionError` - It is not possible to establish a connection to the endpoint
  

**Returns**:

- `events` _list_ - Returns the corresponding calendar events

<a id="outlook_calendar.OutlookCalendar.get_weekly_events"></a>

#### get\_weekly\_events

```python
@staticmethod
def get_weekly_events(events: list) -> list
```

The method includes a functionality to get the weekly events

**Arguments**:

- `events` _list_ - Specify the calendar events
  

**Raises**:

- `BaseException` - Unspecified error by extracting the datetime information
  

**Returns**:

- `events_cw` _list_ - Returns the corresponding weekly calendar events

