"""
This module seeds the database with initial data for beer styles.
It defines a function to add predefined beer styles to the database.
"""

from brewblog import create_app, db
from brewblog.models import Style

def seed_styles():
    """
    Seeds the database with predefined beer styles.

    If the styles table is empty, it adds a list of predefined beer styles to the database.
    """
    styles = [
        'Pale Ale',
        'IPA',
        'Wheat',
        'Amber',
        'Red',
        'Porter',
        'Stout',
        'Sour',
        'Pilsner'
    ]
    if not Style.query.first():
        for name in styles:
            new_style = Style(name=name)
            db.session.add(new_style)
    db.session.commit()

if __name__ == '__main__':
    """
    Main entry point for the script.

    Creates the Flask application context and seeds the database with initial data.
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_styles()
