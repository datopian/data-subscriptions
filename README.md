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
  - body: `{"dataset_id": <string:dataset_id>, "kind": "DATASET", "user_id": <string:user_id>}` //for a single dataset subscription
  - body: `{"kind": "NEW_DATASETS", "user_id": <string:user_id>}` //for a new dataset subscription
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
