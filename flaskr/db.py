import sqlite3

import click
from flask.cli import with_appcontext
from flask import current_app, g


def get_db():
    print('also ok here!')
    if 'db' not in g:
        print('is ok here?')
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    print('here is ok!')
    db = get_db()

    print('here is not ok!')
    with current_app.open_resource('schema.sql') as f:
        db.cursor().executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create the new tables."""
    print('run here!')
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
