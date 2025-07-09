from app import db, app
from models import Coffee, Product

with app.app_context():
    db.create_all()

    db.session.commit()
