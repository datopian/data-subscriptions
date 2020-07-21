# Data Subscriptions

_Service to monitor and notify users about changes in datasets._

Data Subscriptions is a service meant to notify users when CKAN datasets change. For the end-users, it works like this:

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgY3VyYXRvcigoRGF0YSBDdXJhdG9yKSlcbiAgdXNlcigoVXNlcikpXG5cbiAgc3ViZ3JhcGggY2thbltcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIGRhdGFzZXRbXCJEYXRhc2V0L1Jlc291cmNlXCJdXG4gIGVuZFxuXG5cbiAgY3VyYXRvciAtLSB1cGRhdGVzIG1ldGFkYXRhIC0tPiBkYXRhc2V0XG4gIGN1cmF0b3IgLS0gdXBkYXRlcyBkYXRhIC0tPiBkYXRhc2V0XG4gIHVzZXIgLS0gc3Vic2NyaWJlcyAtLT4gZGF0YXNldFxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgY3VyYXRvcigoRGF0YSBDdXJhdG9yKSlcbiAgdXNlcigoVXNlcikpXG5cbiAgc3ViZ3JhcGggY2thbltcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIGRhdGFzZXRbXCJEYXRhc2V0L1Jlc291cmNlXCJdXG4gIGVuZFxuXG5cbiAgY3VyYXRvciAtLSB1cGRhdGVzIG1ldGFkYXRhIC0tPiBkYXRhc2V0XG4gIGN1cmF0b3IgLS0gdXBkYXRlcyBkYXRhIC0tPiBkYXRhc2V0XG4gIHVzZXIgLS0gc3Vic2NyaWJlcyAtLT4gZGF0YXNldFxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

Every 10 minutes, it communicates with CKAN Classic to store the latest updates in a local database. Every 30 minutes, it sends an aggregated notification to users. The worker sends notifications only to users with an active subscription to datasets changed in the past minutes. You can configure all the time frequencies via environment variables.

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgc3ViZ3JhcGggZGF0YXN1YnNjcmlwdGlvbnNbXCJEYXRhIFN1YnNjcmlwdGlvbnNcIl1cbiAgICBEYXRhYmFzZVxuICAgIFdvcmtlclxuICBlbmRcblxuICBzdWJncmFwaCBja2FuY2xhc3NpY1tcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIGNrYW5hcGlbXCJBUElcIl1cbiAgZW5kXG5cbiAgV29ya2VyIC0tIFwicHVsbHMgZGF0YXNldCBhY3Rpdml0eSAodXBkYXRlcylcIiAtLT4gY2thbmFwaVxuICBXb3JrZXIgLS0gc3RvcmVzIGFjdGl2aXR5IC0tPiBEYXRhYmFzZVxuICBXb3JrZXIgLS0gcHJlcGFyZXMgZW1haWwgLS0-IHNlbmRncmlkW1wiU2VuZEdyaWQ8YnI-KHRoaXJkLXBhcnR5KVwiXVxuICBXb3JrZXIgLS0gcHVsbHMgYWN0aXZpdHkgLS0-IERhdGFiYXNlXG4gIHNlbmRncmlkIC0tIHNlbmRzIGVtYWlsIC0tPiB1c2VyKChcIlVzZXJcIikpIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgc3ViZ3JhcGggZGF0YXN1YnNjcmlwdGlvbnNbXCJEYXRhIFN1YnNjcmlwdGlvbnNcIl1cbiAgICBEYXRhYmFzZVxuICAgIFdvcmtlclxuICBlbmRcblxuICBzdWJncmFwaCBja2FuY2xhc3NpY1tcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIGNrYW5hcGlbXCJBUElcIl1cbiAgZW5kXG5cbiAgV29ya2VyIC0tIFwicHVsbHMgZGF0YXNldCBhY3Rpdml0eSAodXBkYXRlcylcIiAtLT4gY2thbmFwaVxuICBXb3JrZXIgLS0gc3RvcmVzIGFjdGl2aXR5IC0tPiBEYXRhYmFzZVxuICBXb3JrZXIgLS0gcHJlcGFyZXMgZW1haWwgLS0-IHNlbmRncmlkW1wiU2VuZEdyaWQ8YnI-KHRoaXJkLXBhcnR5KVwiXVxuICBXb3JrZXIgLS0gcHVsbHMgYWN0aXZpdHkgLS0-IERhdGFiYXNlXG4gIHNlbmRncmlkIC0tIHNlbmRzIGVtYWlsIC0tPiB1c2VyKChcIlVzZXJcIikpIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

This service also has a REST API to:

- Change a subscription status.
- Block a dataset from being subscribed.

## API

To list all available routes in the app, you can run the following docker-compose command:

```bash
docker-compose run --rm web data_subscriptions routes
```

Base URI: `/api/v1/`

### Non-subscribable datasets

**Endpoint: `/nonsubscribable_datasets/<string:dataset_id>`**

By default, all datasets are subscribable. It is the data curator's work to disable subscriptions for a dataset.

Available methods:

- `GET` - Check if a dataset is non-subscribable.
- `POST` - Make a dataset non-subscribable, i.e., disable subscriptions.
- `DELETE` - Delete a dataset from list of non-subscribable datasets, i.e., make it subscribable again.

### Subscription Status

**Endpoint: `/subscription_status`**

Available methods:

- `POST` - Check the a user's subscription status.
  - body: `{"dataset_id": <string:dataset_id>, "kind": "DATASET", "user_id": <string:user_id>}` //for a single dataset subscription
  - body: `{"kind": "NEW_DATASETS", "user_id": <string:user_id>}` //for a new dataset subscription

### Subscriptions

**Endpoint: `/subscription`**

Available methods:

- `POST` - Subscribe a user to notifications.
  - body: `{"dataset_id": <string:dataset_id>, "kind": "DATASET", "user_id": <string:user_id>, "username": <string:username>, "email": <string:email> }` //for a single dataset subscription
  - body: `{"kind": "NEW_DATASETS", "user_id": <string:user_id>, "username": <string:username>, "email": <string:email>}` //for a new dataset subscription
- `DELETE` - Unsubscribe a user from notifications.
  - body: `{"dataset_id": <string:dataset_id>, "kind": "DATASET", "user_id": <string:user_id>}` //for a single dataset subscription
  - body: `{"kind": "NEW_DATASETS", "user_id": <string:user_id>}`  //for a new dataset subscription

### User

**Endpoint: `/user/<string:user_id>`**

Available methods:

- `GET` - Get list of subscriptions for a given authorized user.

### Dataset

**Endpoint: `/dataset/<string:dataset_id>`

Available methods:

- `DELETE` - Delete the subscriptions for given dataset.

### Subscription Report

**Endpoint: `/stat`**

Available methods:

- `GET` - Get report of all subscribers in JSON.
- `GET` - Get report of all subscribers in CSV.
  - param: `download=yes`

## Development

To setup the project using Docker containers:

```sh
$ make setup
```

The project is backed by a test suite, which can be run with a single command:

```sh
$ make test
```

Finally, to start the services and get to see the logs in real time:

```
$ docker-compose up
```

## Deployment

We do continuous deployment [to Heroku](https://gitlab.com/datopian/clients/data-subscriptions/-/blob/master/heroku.yml) via [GitLab CI](https://gitlab.com/datopian/clients/data-subscriptions/-/blob/master/.gitlab-ci.yml).


# Design

## Domain Model

* **Subscription**: `tuple(account, dataset, {event-type-filter}, [frequency?], ...)`
  * `tuple(account, filter-function-on-activity-stream)`
* **Subscription Settings**: `tuple(account, media[web|email|sms|newsletter], other options)`
* **Account (User)**: a user for a subscription
  
Alternatively could seem them as any filter operation on an overall activity stream  => leads us into event bus type territory … 

In the most general sense, A "subscription" (for notifications) is a function f:

```
f(event stream) = user's event stream
```

And notifications are:

```
g(user's event stream, settings) => emails/sms etc
```

## Components

* SubscriptionDB + API
* NotifierService e.g. bulk email/sms
* UI
* Notification
* RulesDB (?) (for generating notifications)
 
Required but probably external

* Accounts (user identifier + email + sms)

Notes

* I (account) subscribe to dataset (dataset) X
* Curator updates dset (dataset) X
* I get a notification (event)
* Curator updates dataset (dataset) Y
* I don't get a notification (event)
* Curator updates dataset (dataset) X
* I get a notification (event)

## Sequence Diagrams

### Subscribe (/ Unsubscribe / Change subscription) button click

* TODO: add to sequence checking restrictions on which datasets you can subscribe to

```mermaid
sequenceDiagram

  Frontend->>API: POST /subscription?dataset=123&account=qwe&event-type=xxx
  API->>Authz: check authorization for {user, dataset}
  Authz-->>API: OK
  API->>DB: UPSERT INTO subscriptions {timestamp, account, dataset, event-type}
  API-->>Frontend: HTTP 201 CREATED
  Frontend->>Frontend: Update UI
```

### Event happens ...

* curator edits a datasets and event stream has a new event (EventStream = activity stream table in CKAN Classic))
* MetaStore->>EventStream: `INSERT INTO (dataset, eventType, message)`
* Prior to event happening SubsNotificationService has subscribed itself to the EventStream

```mermaid
sequenceDiagram

  EventStream->>Notifier: POST /event
  loop for xmedium in [email, sms]
    Notifier->>SubsDB: SELECT FROM subscribers JOIN subs_settings WHERE dataset = ? AND eventType = ? AND medium = xmedium
    SubsDB-->>Notifier: returns(account[])
    Notifier-->>Settings: get Email/SMS Template
    Notifier->>Emailer/SMS: send(account.email/mobile[], msg)
  end
```

* https://github.com/ckan/ckan/blob/master/ckan/model/activity.py
  * There is a big table of all the activities ...
  * Could turn this into an event hub service (esp if we )
    * Could we use postgres listen/notify ...
    * Or we could even just do polling if time internal is not too short ...


### Render subscribe UI in frontend ...

* Frontend needs to check before rendering if this is a dataset that allows subscriptions
* Frontend needs to check if user is subscribed
* TODO.QU: where do we save whether a dataset is subscribable
  * ANS: in a separate table: `nonsubscribable_datasets`

```mermaid
sequenceDiagram

  Frontend->>Frontend: is user logged in?
  Frontend->>API: GET /is_subscribable?dataset=xxx?
  API->>DB: SELECT NOT xxx FROM nonsubscribable_datasets
  API-->>Frontend: yes/no [if no, done]
  Frontend->>API: GET /subscription?dataset=123&account=qwe
  API->>Authz: check authorization for {user, dataset}
  Authz-->>API: OK
  API->>DB: SELECT subscriptions {timestamp, account, dataset, event-type}
  DB-->>API: return subscriptions[]
  API-->>Frontend: return event-type or null
  Frontend->>Frontend: showSubscribeUI(current-event-type | default-event-type)
```

### User views (and changes) notification settings

### User views all existing (and potential?) subscriptions (and changes)

* TODO.QU: does include potential - that's weird in my view (how does it work with 200 datasets or 200k). Just let people subscribe via the dataset page

### Admin views stats ...

### Admin sets subscribable status
