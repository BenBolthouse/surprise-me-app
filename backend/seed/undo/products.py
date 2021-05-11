from models import db


def down():
    db.session.execute('DELETE FROM products;')
    db.session.execute('ALTER SEQUENCE products_id_seq RESTART WITH 1;')
    db.session.commit()
