from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash  
from flask_login import UserMixin

from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

# types of ingredient units users can select
UNIT_OPTIONS = ["unit", "lb", "cup", "tbsp", "tsp", "g", "oz"]

# keeps track of which tags are on which recipes
recipe_tags_table = db.Table('recipe_tags_table', db.metadata, sqla.Column('recipe_id', sqla.Integer, sqla.ForeignKey('recipe.id'), primary_key=True), 
                                 sqla.Column('tag_id', sqla.Integer, sqla.ForeignKey('tag.id'), primary_key=True))

# keeps track of which users have saved which recipes
saved_recipes_table = db.Table(
    'saved_recipes_table', 
    db.metadata, 
    sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True),
    sqla.Column('recipe_id', sqla.Integer, sqla.ForeignKey('recipe.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    # --- ATTRIBUTES ---
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    first_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    last_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    password_hash: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(256))
    # only true for certified users
    is_certified: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)

    # --- RELATIONSHIPS ---
    # keeps track of what recipes this user has written
    written_recipes: sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(back_populates='writer')

    # keeps track of what recipes this user has saved
    users_saved_recipes : sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(
        secondary=saved_recipes_table,
        primaryjoin=(saved_recipes_table.c.user_id == id),
        back_populates='recipe_saved_by_users'
    )

    # helps keep track of the user's ingredient list
    curr_ingredients: sqlo.WriteOnlyMapped['UserIngredientListUse'] = sqlo.relationship(back_populates='userlist_user')

    # --- METHODS ---
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
        return db.session.scalars(self.written_recipes.select()).all()
    
    def get_user_recipes_query(self):
        return sqla.select(Recipe).where(Recipe.user_id == self.id)
    
    # Returns the user's draft (NOTE: currently assumes only one draft is possible;)
    # TODO: update to multiple drafts in further iterations
    def get_drafted_recipe(self):
        return db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True).where(Recipe.user_id == self.id)).first()


class Recipe(db.Model):
    # --- ATTRIBUTES ---
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150), default="")
    description: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500), default="")
    servingSize : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0)
    estimatedTime : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(25), default="")
    steps : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String, default="")
    timestamp : sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc)) 
    is_draft : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=True)

    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))

    # --- RELATIONSHIPS ---
    # keeps track of what user wrote this recipe
    writer : sqlo.Mapped['User'] = sqlo.relationship(back_populates='written_recipes')

    # keeps track of what tags are on this recipe
    tags: sqlo.WriteOnlyMapped['Tag'] = sqlo.relationship(
        secondary=recipe_tags_table, primaryjoin=(recipe_tags_table.c.recipe_id == id),back_populates='recipes', passive_deletes=True)
    
    # keeps track of what users have saved this recipe
    recipe_saved_by_users : sqlo.WriteOnlyMapped['User'] = sqlo.relationship(
        secondary=saved_recipes_table,
        primaryjoin=(saved_recipes_table.c.recipe_id == id),
        back_populates='users_saved_recipes'
    )
    def get_tags(self):
        return db.session.scalars(self.tags.select()).all()

    # keeps track of what ingredients + amounts are used in this recipe
    ingredients_used: sqlo.WriteOnlyMapped['RecipeIngredientUse'] = sqlo.relationship(back_populates='recipe_usecase_recipe')
    
    # --- METHODS ---
    def __repr__(self):
        if self.is_draft:
            return '<[DRAFT] Recipe id: {} - title: {} (last edited {})>'.format(self.id, self.title, self.timestamp)
        else:
            return '<Recipe id: {} - title: {} (last edited {})>'.format(self.id, self.title, self.timestamp)
    
    def get_ingredient_use_cases(self):
        return db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == self.id)).all()

    def get_tags(self):
        return db.session.scalars(self.tags.select()).all()


class Tag(db.Model):
    # --- ATTRIBUTES ---
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))

    # --- RELATIONSHIPS ---
    # keeps track of what recipes have this tag
    recipes: sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(
        secondary=recipe_tags_table, primaryjoin=(recipe_tags_table.c.tag_id == id), back_populates='tags')

    # --- METHODS ---
    def __repr__(self):
        return '<Tag id: {} - name: {}>'.format(self.id, self.name)


class Ingredient(db.Model):
    # --- ATTRIBUTES ---
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), index=True, unique=True)
    
    # --- RELATIONSHIPS ---
    # helps keep track of ingredients + amounts in recipes
    recipe_involvements: sqlo.WriteOnlyMapped['RecipeIngredientUse'] = sqlo.relationship(back_populates='recipe_usecase_ingredient')

    # helps keep track of ingredients + amounts in users' ingredient lists
    userlist_involvements: sqlo.WriteOnlyMapped['UserIngredientListUse'] = sqlo.relationship(back_populates='userlist_ingredient')

    # --- METHODS ---
    def __repr__(self):
        return '<Ingredient id: {} - name: {}>'.format(self.id, self.name)


class RecipeIngredientUse(db.Model):
    # --- ATTRIBUTES ---
    recipe_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Recipe.id), primary_key=True)
    ingredient_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Ingredient.id), primary_key=True)
    amount : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    unit : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))

    # constrain unit to be one of the options in UNIT_OPTIONS
    __table_args__ = (
        sqla.CheckConstraint(unit.in_(UNIT_OPTIONS), name='recipe_unit_check'),
    )

    # --- RELATIONSHIPS ---
    # keeps track of the recipe this ingredient use is in
    recipe_usecase_recipe : sqlo.Mapped[Recipe] = sqlo.relationship(back_populates = 'ingredients_used')

    # keeps track of the ingredient this ingredient use is using
    recipe_usecase_ingredient : sqlo.Mapped[Ingredient] = sqlo.relationship(back_populates = 'recipe_involvements')

    # --- METHODS ---
    def __repr__(self):
        return '<Recipe id: {} - ingredient: {} with {} {}>'.format(self.recipe_id, self.ingredient_id, self.amount, self.unit)


class UserIngredientListUse(db.Model):
    # --- ATTRIBUTES ---
    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    ingredient_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Ingredient.id), primary_key=True)
    amount : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    unit : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))

    # constrain unit to be one of the options in UNIT_OPTIONS
    __table_args__ = (
        sqla.CheckConstraint(unit.in_(UNIT_OPTIONS), name='userlist_unit_check'),
    )

    # --- RELATIONSHIPS ---
    # keeps track of the user who has an ingredient list that this ingredient use is in
    userlist_user : sqlo.Mapped[User] = sqlo.relationship(back_populates = 'curr_ingredients')

    # keeps track of the ingredient this ingredient use is using
    userlist_ingredient : sqlo.Mapped[Ingredient] = sqlo.relationship(back_populates = 'userlist_involvements')

    # --- METHODS ---
    def __repr__(self):
        return '<User id: {} - ingredient: {} with {} {}>'.format(self.user_id, self.ingredient_id, self.amount, self.unit)