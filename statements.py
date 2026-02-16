from app import db
import sqlalchemy as sqla

# Un-certify a user
theUser = db.session.scalars(sqla.select(User).where(User.username == "Insert Username")).first()
theUser.is_certified = False
db.session.commit()

# Change save count 