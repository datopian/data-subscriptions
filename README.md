# Data Subscriptions

*Service to monitor and alert users about changes in datasets.*

## API

Base URI: `/api/v1/`

### Non-subscribable datasets

**Endpoint: `/nonsubscribable_datasets/<string:dataset_id>`**

By default, all datasets are subscribable. It is the data curator's work to disable subscriptions for a dataset.

Available methods:

* `GET` - Check if a dataset is non-subscribable.
* `POST` - Make a dataset non-subscribable, e.g., disable subscriptions.
* `DELETE` - Delete a dataset from list of non-subscribable datasets, e.g., make it subscribable again.

### Subscriptions

**Endpoint: `/subscription/<string:dataset_id>`**

Available methods:

* `GET` - Get if given user is subscribed to given dataset.
  * params: `user_id`
* `POST` - Subscribe a user to a dataset.
  * body: `{"user_id": <string:user_id>}`
* `DELETE` - Unsubscribe s user from a dataset.
  * body: `{"user_id": <string:user_id>}`

### User

**Endpoint: `/user/<string:user_id>`**

Available methods:

* `GET` - Get list of subscriptions for a given user.

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
