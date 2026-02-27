from datetime import datetime, timezone
from typing import Optional
from flask import flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash  
from flask_login import UserMixin

from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
import os

# types of ingredient units users can select
UNIT_OPTIONS = ["unit", "lb", "cup", "tbsp", "tsp", "g", "oz"]

# keeps track of which recipes are in which cookbooks
cookbook_recipes_table = db.Table('cookbook_recipes_table', db.metadata, sqla.Column('cookbook_id', sqla.Integer, sqla.ForeignKey('cookbook.id'), primary_key=True), 
                                 sqla.Column('recipe_id', sqla.Integer, sqla.ForeignKey('recipe.id'), primary_key=True))

# keeps track of which tags are on which recipes
recipe_tags_table = db.Table('recipe_tags_table', db.metadata, sqla.Column('recipe_id', sqla.Integer, sqla.ForeignKey('recipe.id'), primary_key=True), 
                                 sqla.Column('tag_id', sqla.Integer, sqla.ForeignKey('tag.id'), primary_key=True))

# keeps track of which users have saved which recipes
saved_recipes_table = db.Table('saved_recipes_table', db.metadata, sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True),
                               sqla.Column('recipe_id', sqla.Integer, sqla.ForeignKey('recipe.id'), primary_key=True))

# keeps track of which certifications each certified user has
user_certifications_table = db.Table('user_certifications_table', db.metadata, sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True),
                                     sqla.Column('certification_id', sqla.Integer, sqla.ForeignKey('certification.id'), primary_key=True))

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
    business_name: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(120))
    business_website: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))

    # --- RELATIONSHIPS ---
    # keeps track of what recipes this user has written
    written_recipes: sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(back_populates='writer', passive_deletes=True)
    written_cookbooks: sqlo.WriteOnlyMapped['Cookbook'] = sqlo.relationship(back_populates='cookbook_writer', passive_deletes=True)

    # keeps track of what recipes this user has saved
    saved_recipes : sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(
        secondary=saved_recipes_table,
        primaryjoin=(saved_recipes_table.c.user_id == id),
        back_populates='saved_by_users',
        passive_deletes=True)
    
    # keeps track of what certifications this user has
    certifications: sqlo.WriteOnlyMapped['Certification'] = sqlo.relationship(
        secondary=user_certifications_table, 
        primaryjoin=(user_certifications_table.c.user_id == id),
        back_populates='user', 
        passive_deletes=True)

    # helps keep track of the user's ingredient list
    curr_ingredients: sqlo.WriteOnlyMapped['UserIngredientListUse'] = sqlo.relationship(back_populates='userlist_user')

    # keep track of the user's grocery list
    grocery_list: sqlo.WriteOnlyMapped['UserGroceryListUse'] = sqlo.relationship(back_populates='grocerylist_user')

    # --- METHODS ---
    def __repr__(self):
        return '<User id: {} - username: {} - email: {}>'.format(self.id, self.username, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, id)
    
    # Returns a list of the user's saved recipes
    def get_saved(self):
        saved = db.session.scalars(self.saved_recipes.select()).all()
        return saved
    
    def get_user_recipes(self):
        return db.session.scalars(self.written_recipes.select().where(Recipe.is_draft == False)).all()
    
    def user_recipe_count(self):
        return len(db.session.scalars(self.written_recipes.select().where(Recipe.is_draft == False)).all())
    
    def get_user_cookbooks(self):
        return db.session.scalars(sqla.select(Cookbook).where(Cookbook.user_id == self.id)).all()
    
    def user_cookbook_count(self):
        return len(db.session.scalars(sqla.select(Cookbook).where(Cookbook.user_id == self.id)).all())

    def get_user_recipes_query(self):
        return sqla.select(Recipe).where(Recipe.user_id == self.id)
        
    # Returns the user's recipe drafts
    def get_drafted_recipes(self):
        return db.session.scalars(sqla.select(Recipe).where(Recipe.is_draft == True).where(Recipe.user_id == self.id)).all()
    
    # gets all the current ingredients of the user
    def get_curr_ingredients(self):
        return db.session.scalars(sqla.select(UserIngredientListUse).where(UserIngredientListUse.user_id==self.id)).all()

    # checks if the ingredient is already in the user's ingredient list
    def is_already_ingredient(self, ingredient):
        is_ingredient = db.session.scalars(sqla.select(UserIngredientListUse).where(UserIngredientListUse.user_id==self.id).where(UserIngredientListUse.ingredient_id==ingredient.id)).first()
        return is_ingredient is not None
    
    # adds a new ingredient to the user's ingredient list if it is not already in the list; otherwise, does nothing
    def add_ingredient(self, ingredient, quantity, unit):
        if not self.is_already_ingredient(ingredient): # if ingredient is not already in user's ingredient list, add it
            new_ingredient_use = UserIngredientListUse(
                user_id = self.id,
                ingredient_id = ingredient.id, 
                amount = quantity,
                unit = unit
            )
            db.session.add(new_ingredient_use)
            flash ('{} added to your ingredient list!'.format(ingredient.name))
        else: # if ingredient is already in user's ingredient list, update the quantity and unit
            ingredient_use = db.session.scalars(sqla.select(UserIngredientListUse).where(UserIngredientListUse.user_id==self.id).where(UserIngredientListUse.ingredient_id==ingredient.id)).first()
            ingredient_use.amount += quantity
            ingredient_use.unit = unit
            flash('{} is updated in your ingredient list!'.format(ingredient.name))
        db.session.commit()

    # gets all the user's grocery list of the user
    def get_grocery_list(self):
        return db.session.scalars(sqla.select(UserGroceryListUse).where(UserGroceryListUse.user_id==self.id)).all()
    
    # checks if the ingredient is already in the user's grocery list
    def is_already_grocery(self, ingredient):
        is_grocery = db.session.scalars(sqla.select(UserGroceryListUse).where(UserGroceryListUse.user_id==self.id).where(UserGroceryListUse.ingredient_id==ingredient.id)).first()
        return is_grocery is not None
    
    # adds a new ingredient to the user's grocery list if it is not already in the list AND not in the current ingredients list
    def add_grocery(self, ingredient, quantity, unit):
        grocery = db.session.scalars(sqla.select(UserGroceryListUse).where(UserGroceryListUse.user_id==self.id).where(UserGroceryListUse.ingredient_id==ingredient.id)).first()
        curr_ingredient = db.session.scalars(sqla.select(UserIngredientListUse).where(UserIngredientListUse.user_id==self.id).where(UserIngredientListUse.ingredient_id==ingredient.id)).first()
        if grocery:
            grocery.amount += quantity
            grocery.unit = unit
            flash('{} is updated in your grocery list!'.format(ingredient.name))
        elif curr_ingredient is not None and curr_ingredient.amount >= quantity:
            flash('{} is already in your current ingredient list'.format(ingredient.name))
        elif curr_ingredient is not None and curr_ingredient.amount < quantity:
            new_grocery = UserGroceryListUse(
                user_id = self.id,
                ingredient_id = ingredient.id, 
                amount = quantity - curr_ingredient.amount, # quantity needed is the difference between the quantity in the recipe and the quantity the user already has
                unit = unit
            )
            db.session.add(new_grocery)
            flash ('{} is added to your grocery list!'.format(ingredient.name))
        else:
            new_grocery = UserGroceryListUse(
                user_id = self.id,
                ingredient_id = ingredient.id, 
                amount = quantity,
                unit = unit
            )
            db.session.add(new_grocery)
            flash ('{} is added to your grocery list!'.format(ingredient.name))
        db.session.commit()
    
    def get_certifications(self):
        return db.session.scalars(self.certifications.select()).all()
    
    def get_num_certification(self):
        return len(self.get_certifications())
    
class Certification(db.Model):
    # --- ATTRIBUTES ---
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))
    dateRecieved: sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc))

    # --- RELATIONSHIPS ---
    # keeps track of what users have this certification
    user: sqlo.WriteOnlyMapped['User'] = sqlo.relationship(
        secondary=user_certifications_table, primaryjoin=(user_certifications_table.c.certification_id == id), back_populates='certifications')

    # --- METHODS ---
    def __repr__(self):
        return '<Certification id: {} - name: {} - date recieved: {}>'.format(self.id, self.name, self.dateRecieved)


class Recipe(db.Model):
    # --- ATTRIBUTES ---
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150), default="")
    pictFile : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String())
    description: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(215), default="")
    servingSize : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0)
    estimatedHrs : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    estimatedMins : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    timestamp : sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc)) 
    is_draft : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=True)
    save_count : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)

    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))

    # --- RELATIONSHIPS ---
    # keeps track of what user wrote this recipe
    writer : sqlo.Mapped['User'] = sqlo.relationship(back_populates='written_recipes')
    recipe_steps: sqlo.WriteOnlyMapped['RecipeStep'] = sqlo.relationship(back_populates='recipe_appearance', passive_deletes=True)

    # keeps track of what tags are on this recipe
    tags: sqlo.WriteOnlyMapped['Tag'] = sqlo.relationship(
        secondary=recipe_tags_table, 
        primaryjoin=(recipe_tags_table.c.recipe_id == id),
        back_populates='recipes', 
        passive_deletes=True)
    
    # keeps track of what users have saved this recipe
    saved_by_users : sqlo.WriteOnlyMapped['User'] = sqlo.relationship(
        secondary=saved_recipes_table,
        primaryjoin=(saved_recipes_table.c.recipe_id == id),
        back_populates='saved_recipes',
        passive_deletes=True)
    
    cookbook_appearances: sqlo.WriteOnlyMapped['Cookbook'] = sqlo.relationship(
        secondary=cookbook_recipes_table, primaryjoin=(cookbook_recipes_table.c.recipe_id == id), back_populates='included_recipes', passive_deletes=True)

    # keeps track of what ingredients + amounts are used in this recipe
    ingredients_used: sqlo.WriteOnlyMapped['RecipeIngredientUse'] = sqlo.relationship(back_populates='recipe_usecase_recipe', passive_deletes=True)
    
    # --- METHODS ---
    def __repr__(self):
        if self.is_draft:
            return '<[DRAFT] Recipe id: {} - title: {} (last edited {})>'.format(self.id, self.title, self.timestamp)
        else:
            return '<Recipe id: {} - title: {} (last edited {})>'.format(self.id, self.title, self.timestamp)
    
    def get_tags(self):
        return db.session.scalars(self.tags.select()).all()
    
    def get_num_tag(self):
        return len(self.get_tags())

    def get_ingredient_use_cases(self):
        return db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == self.id)).all()
    
    def get_num_ingredients(self):
        return len(db.session.scalars(sqla.select(RecipeIngredientUse).where(RecipeIngredientUse.recipe_id == self.id)).all())
    
    def get_steps(self):
        return db.session.scalars(self.recipe_steps.select().order_by(RecipeStep.stepNum)).all()
    
    def has_image(self):
        if self.pictFile is None or self.pictFile == "":
            return False
        else:
            basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/recipe-imgs')
            if os.path.exists(os.path.join(basedir, self.pictFile)):
                return True
            else:
                return False
        
    def get_pict_path(self):
        if self.has_image():
            return 'img/recipe-imgs/'+self.pictFile
        else:
            return None
    
    def get_cookbooks(self):
        return db.session.scalars(self.cookbook_appearances.select()).all()
    
class RecipeStep(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    stepNum: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    description: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(500))
    recipe_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('recipe.id'))

    recipe_appearance : sqlo.Mapped['Recipe'] = sqlo.relationship(back_populates='recipe_steps')


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


class Cookbook(db.Model):
    # --- ATTRIBUTES --
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150), default="")
    pictFile : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(), default="")
    description: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(215), default="")

    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))

    # --- RELATIONSHIPS --
    included_recipes: sqlo.WriteOnlyMapped['Recipe'] = sqlo.relationship(
        secondary=cookbook_recipes_table, 
        primaryjoin=(cookbook_recipes_table.c.cookbook_id == id),
        back_populates='cookbook_appearances', 
        passive_deletes=True)
    
    cookbook_writer : sqlo.Mapped['User'] = sqlo.relationship(back_populates='written_cookbooks')
    
    # --- METHODS --
    def __repr__(self):
        return '<Cookbook {} - name: {}>'.format(self.id, self.title)
    
    def get_recipes(self):
        return db.session.scalars(self.included_recipes.select()).all()
    
    def get_num_recipes(self):
        return len(db.session.scalars(self.included_recipes.select()).all())
    
    def get_writer(self):
        return self.cookbook_writer.username
    
    def has_image(self):
        if self.pictFile is None or self.pictFile == "":
            return False
        else:
            basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/recipe-imgs')
            if os.path.exists(os.path.join(basedir, self.pictFile)):
                return True
            else:
                return False
        
    def get_pict_path(self):
        if self.has_image():
            return 'img/recipe-imgs/'+self.pictFile
        else:
            return None


class Ingredient(db.Model):
    # --- ATTRIBUTES ---
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), index=True, unique=True)
    
    # --- RELATIONSHIPS ---
    # helps keep track of ingredients + amounts in recipes
    recipe_involvements: sqlo.WriteOnlyMapped['RecipeIngredientUse'] = sqlo.relationship(back_populates='recipe_usecase_ingredient')

    # helps keep track of ingredients + amounts in users' ingredient lists
    userlist_involvements: sqlo.WriteOnlyMapped['UserIngredientListUse'] = sqlo.relationship(back_populates='userlist_ingredient')

    # helps keep track of ingredients + amounts in users' grocery lists
    grocery_list_involvements: sqlo.WriteOnlyMapped['UserGroceryListUse'] = sqlo.relationship(back_populates='grocerylist_ingredient')

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
    
    def getName(self):
        return db.session.scalars(sqla.select(Ingredient.name).where(Ingredient.id == self.ingredient_id)).first().capitalize()


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
    
    def get_name(self):
        return db.session.scalars(sqla.select(Ingredient.name).where(Ingredient.id == self.ingredient_id)).first()
    

class UserGroceryListUse(db.Model):
    # --- ATTRIBUTES ---
    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    ingredient_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Ingredient.id), primary_key=True)
    amount : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    unit : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))

    # constrain unit to be one of the options in UNIT_OPTIONS
    __table_args__ = (
        sqla.CheckConstraint(unit.in_(UNIT_OPTIONS), name='grocerylist_unit_check'),
    )

    # --- RELATIONSHIPS ---
    # keeps track of the user who has a grocery list that this ingredient use is in
    grocerylist_user : sqlo.Mapped[User] = sqlo.relationship(back_populates = 'grocery_list')

    # keeps track of the ingredient this ingredient use is using
    grocerylist_ingredient : sqlo.Mapped[Ingredient] = sqlo.relationship(back_populates = 'grocery_list_involvements')

    # --- METHODS ---
    def __repr__(self):
        return '<User id: {} - ingredient: {} with {} {}>'.format(self.user_id, self.ingredient_id, self.amount, self.unit)
    
    def get_name(self):
        return db.session.scalars(sqla.select(Ingredient.name).where(Ingredient.id == self.ingredient_id)).first()
