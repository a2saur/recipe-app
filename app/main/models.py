from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash  
from flask_login import UserMixin

from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

recipeTags = db.Table('recipeTags', db.metadata, sqla.Column('recipe_id', sqla.Integer, sqla.ForeignKey('recipe.id'), primary_key=True), 
                                 sqla.Column('tag_id', sqla.Integer, sqla.ForeignKey('tag.id'), primary_key=True))

friends = db.Table('friends', db.metadata, sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True), 
                                 sqla.Column('friend_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True))

class User(db.Model, UserMixin):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    password_hash: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(256))
    curr_ingredients = sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(2000))
    # relationships
    recipes: sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(back_populates='writer')
  
    def __repr__(self):
        return '<User id: {} - username: {} - email: {}>'.format(self.id, self.username, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    def get_user_recipes(self):
        return db.session.scalars(self.recipes.select()).all()
    
    def get_user_recipes_query(self):
        return sqla.select(Recipe).where(Recipe.user_id == self.id)



class Recipe(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))
    body: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500))
    timestamp : sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc)) 
    saves: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default = 0)
    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))
    # relationships
    writer : sqlo.Mapped['User'] = sqlo.relationship(back_populates='recipes')
    tags: sqlo.WriteOnlyMapped['Tag'] = sqlo.relationship(
        secondary=recipeTags, primaryjoin=(recipeTags.c.recipe_id == id),back_populates='recipes', passive_deletes=True)
    
    def get_tags(self):
        return db.session.scalars(self.tags.select()).all()
    
class Tag(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))

    # relationships
    recipes: sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(
        secondary=recipeTags, primaryjoin=(recipeTags.c.tag_id == id), back_populates='tags')

    def __repr__(self):
        return '<Tag id: {} - name: {}>'.format(self.id,self.name)

