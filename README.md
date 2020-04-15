# Data Subscriptions

_Service to monitor and notify users about changes in datasets._

Data Subscriptions is a service meant to notify users when CKAN datasets change. For the end-users, it works like this:

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgc3ViZ3JhcGggY2thbltcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIGN1cmF0b3IoKERhdGEgQ3VyYXRvcikpIC0tIHVwZGF0ZXMgbWV0YWRhdGEgLS0-IGRhdGFzZXRbXCJEYXRhc2V0L1Jlc291cmNlXCJdXG4gICAgY3VyYXRvciAtLSB1cGRhdGVzIGRhdGEgLS0-IGRhdGFzZXRcbiAgICB1c2VyKChVc2VyKSkgLS0gc3Vic2NyaWJlcyAtLT4gZGF0YXNldFxuICBlbmRcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgc3ViZ3JhcGggY2thbltcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIGN1cmF0b3IoKERhdGEgQ3VyYXRvcikpIC0tIHVwZGF0ZXMgbWV0YWRhdGEgLS0-IGRhdGFzZXRbXCJEYXRhc2V0L1Jlc291cmNlXCJdXG4gICAgY3VyYXRvciAtLSB1cGRhdGVzIGRhdGEgLS0-IGRhdGFzZXRcbiAgICB1c2VyKChVc2VyKSkgLS0gc3Vic2NyaWJlcyAtLT4gZGF0YXNldFxuICBlbmRcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

Every 10 minutes, it communicates with CKAN Classic to store the latest updates in a local database. Every 30 minutes, it sends an aggregated notification to users. The worker sends notifications only to users with an active subscription to datasets changed in the past minutes. You can configure all the time frequencies via environment variables.

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgc3ViZ3JhcGggZGF0YXN1YnNjcmlwdGlvbnNbXCJEYXRhIFN1YnNjcmlwdGlvbnNcIl1cbiAgICBXb3JrZXIgLS0gXCJwdWxscyBkYXRhc2V0IGFjdGl2aXR5ICh1cGRhdGVzKVwiIC0tPiBja2FuY2xhc3NpY1tcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIFdvcmtlciAtLSBzdG9yZXMgYWN0aXZpdHkgLS0-IGRiWyhEYXRhYmFzZSldXG4gICAgV29ya2VyIC0tIHByZXBhcmVzIGVtYWlsIC0tPiBzZW5kZ3JpZFtcIlNlbmRHcmlkPGJyPih0aGlyZC1wYXJ0eSlcIl1cbiAgICBXb3JrZXIgLS0gcHVsbHMgYWN0aXZpdHkgLS0-IGRiXG4gICAgc2VuZGdyaWQgLS0gc2VuZHMgZW1haWwgLS0-IHVzZXIoKFwiVXNlclwiKSlcbiAgZW5kIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgc3ViZ3JhcGggZGF0YXN1YnNjcmlwdGlvbnNbXCJEYXRhIFN1YnNjcmlwdGlvbnNcIl1cbiAgICBXb3JrZXIgLS0gXCJwdWxscyBkYXRhc2V0IGFjdGl2aXR5ICh1cGRhdGVzKVwiIC0tPiBja2FuY2xhc3NpY1tcIkNLQU4gQ2xhc3NpY1wiXVxuICAgIFdvcmtlciAtLSBzdG9yZXMgYWN0aXZpdHkgLS0-IGRiWyhEYXRhYmFzZSldXG4gICAgV29ya2VyIC0tIHByZXBhcmVzIGVtYWlsIC0tPiBzZW5kZ3JpZFtcIlNlbmRHcmlkPGJyPih0aGlyZC1wYXJ0eSlcIl1cbiAgICBXb3JrZXIgLS0gcHVsbHMgYWN0aXZpdHkgLS0-IGRiXG4gICAgc2VuZGdyaWQgLS0gc2VuZHMgZW1haWwgLS0-IHVzZXIoKFwiVXNlclwiKSlcbiAgZW5kIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

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

### Subscriptions

**Endpoint: `/subscription/<string:dataset_id>`**

Available methods:

- `GET` - Get if given user is subscribed to given dataset.
  - params: `user_id`
- `POST` - Subscribe a user to a dataset.
  - body: `{"user_id": <string:user_id>}`
- `DELETE` - Unsubscribe s user from a dataset.
  - body: `{"user_id": <string:user_id>}`

### User

**Endpoint: `/user/<string:user_id>`**

Available methods:

- `GET` - Get list of subscriptions for a given user.

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
