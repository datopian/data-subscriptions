import sys

from alembic.util.exc import CommandError
from alembic.config import Config
from alembic.script import ScriptDirectory


def test_only_single_head_revision():
    """
    Detect the existance of more than one head in the migrations tree.
    Generally, this is caused when 2+ people create migrations from
    the same branch.

    To solve it, you have two main options:

    1. Manually fix the revision in the new migration.
    2. Force Alembic to create a node to merge both conflicting heads:

        $ alembic -c migrations/alembic.ini merge heads -m merge_migration_tree

    Context: https://blog.jerrycodes.com/multiple-heads-in-alembic-migrations/
    """
    config = Config()
    config.set_main_option("script_location", "migrations")
    script = ScriptDirectory.from_config(config)
    script.get_current_head()
