import click
from flask.cli import FlaskGroup

from data_subscriptions.app import create_app


def create_data_subscriptions(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_data_subscriptions)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user
    """
    from data_subscriptions.extensions import db
    from data_subscriptions.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@example.com", password="admin", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
