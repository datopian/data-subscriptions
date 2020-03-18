import click
from flask.cli import FlaskGroup

from data_subscriptions.app import create_app


def create_data_subscriptions(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_data_subscriptions)
def cli():
    """Service to monitor and alert users about changes in datasets."""


if __name__ == "__main__":
    cli()
