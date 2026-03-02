from app import create_app, db
from config import Config
from datetime import datetime, timezone

app = create_app(Config)

from app.main.models import Recipe, Cookbook, User, Ingredient, Tag, RecipeIngredientUse, RecipeStep, Certification
from config  import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
import os

if os.path.exists("meal_planner.db"):
    os.remove("meal_planner.db")

app.app_context().push()

db.create_all()
# --- Add Users ---
u0 = User(
first_name = "A", last_name = "S", username = "A2", email = "a@wpi.edu", is_certified=False)
u0.set_password("123")
db.session.add(u0)


u1 = User(
first_name = "Mama", last_name = "Nintendo", username = "CookingMama", email = "cooking@nintendo.com", is_certified=True)
u1.set_password("123")
db.session.add(u1)


u2 = User(
first_name = "Chat", last_name = "GPT", username = "ChatGPT", email = "chat@chat.com", is_certified=True)
u2.set_password("123")
db.session.add(u2)


u3 = User(
first_name = "All", last_name = "Recipes", username = "AllRecipes", email = "chef@allrecipes.com", is_certified=True)
u3.set_password("123")
db.session.add(u3)


u4 = User(
first_name = "D", last_name = "Lish", username = "Delish", email = "delish@delish.com", is_certified=False)
u4.set_password("123")
db.session.add(u4)

db.session.commit()

# --- Add Ingredients ---
i0 = Ingredient(
name = "chicken")
db.session.add(i0)


i1 = Ingredient(
name = "zucchini")
db.session.add(i1)


i2 = Ingredient(
name = "rice")
db.session.add(i2)


i3 = Ingredient(
name = "onion")
db.session.add(i3)


i4 = Ingredient(
name = "cream")
db.session.add(i4)


i5 = Ingredient(
name = "milk")
db.session.add(i5)


i6 = Ingredient(
name = "salt")
db.session.add(i6)


i7 = Ingredient(
name = "pepper")
db.session.add(i7)


i8 = Ingredient(
name = "butter")
db.session.add(i8)


i9 = Ingredient(
name = "corn")
db.session.add(i9)


i10 = Ingredient(
name = "avocado")
db.session.add(i10)


i11 = Ingredient(
name = "scallion")
db.session.add(i11)


i12 = Ingredient(
name = "chili")
db.session.add(i12)


i13 = Ingredient(
name = "bread")
db.session.add(i13)


i14 = Ingredient(
name = "pancake mix")
db.session.add(i14)


i15 = Ingredient(
name = "egg")
db.session.add(i15)


i16 = Ingredient(
name = "olive oil")
db.session.add(i16)


i17 = Ingredient(
name = "thyme")
db.session.add(i17)


i18 = Ingredient(
name = "rosemary")
db.session.add(i18)


i19 = Ingredient(
name = "garlic")
db.session.add(i19)


i20 = Ingredient(
name = "pasta")
db.session.add(i20)


i21 = Ingredient(
name = "parmesan")
db.session.add(i21)


i22 = Ingredient(
name = "parsley")
db.session.add(i22)


i23 = Ingredient(
name = "carrot")
db.session.add(i23)


i24 = Ingredient(
name = "bell pepper")
db.session.add(i24)


i25 = Ingredient(
name = "soy sauce")
db.session.add(i25)


i26 = Ingredient(
name = "sesame oil")
db.session.add(i26)


i27 = Ingredient(
name = "rice vinegar")
db.session.add(i27)


i28 = Ingredient(
name = "sugar")
db.session.add(i28)


i29 = Ingredient(
name = "ginger")
db.session.add(i29)


i30 = Ingredient(
name = "flour")
db.session.add(i30)


i31 = Ingredient(
name = "baking powder")
db.session.add(i31)


i32 = Ingredient(
name = "baking soda")
db.session.add(i32)


i33 = Ingredient(
name = "buttermilk")
db.session.add(i33)


i34 = Ingredient(
name = "brown sugar")
db.session.add(i34)


i35 = Ingredient(
name = "vanilla extract")
db.session.add(i35)


i36 = Ingredient(
name = "chocolate chips")
db.session.add(i36)


i37 = Ingredient(
name = "chicken breast")
db.session.add(i37)


i38 = Ingredient(
name = "chicken broth")
db.session.add(i38)


i39 = Ingredient(
name = "heavy cream")
db.session.add(i39)


i40 = Ingredient(
name = "lemon zest")
db.session.add(i40)


i41 = Ingredient(
name = "lemon juice")
db.session.add(i41)


i42 = Ingredient(
name = "red pepper")
db.session.add(i42)


i43 = Ingredient(
name = "baby spinach")
db.session.add(i43)


i44 = Ingredient(
name = "parmesan cheese")
db.session.add(i44)


i45 = Ingredient(
name = "red pepper flakes")
db.session.add(i45)


i46 = Ingredient(
name = "sundried-tomates")
db.session.add(i46)


i47 = Ingredient(
name = "bacon")
db.session.add(i47)


i48 = Ingredient(
name = "water")
db.session.add(i48)


i49 = Ingredient(
name = "worcestershire sauce")
db.session.add(i49)


i50 = Ingredient(
name = "unsalted butter")
db.session.add(i50)


i51 = Ingredient(
name = "white grits")
db.session.add(i51)


i52 = Ingredient(
name = "white cheddar cheese")
db.session.add(i52)


i53 = Ingredient(
name = "shrimp")
db.session.add(i53)


i54 = Ingredient(
name = "cajun seasoning")
db.session.add(i54)


i55 = Ingredient(
name = "jalapeno pepper")
db.session.add(i55)


i56 = Ingredient(
name = "green onion")
db.session.add(i56)


i57 = Ingredient(
name = "peanut butter")
db.session.add(i57)


i58 = Ingredient(
name = "protein powder")
db.session.add(i58)


i59 = Ingredient(
name = "maple syrup")
db.session.add(i59)


i60 = Ingredient(
name = "coconut oil")
db.session.add(i60)


i61 = Ingredient(
name = "wonton wrappers")
db.session.add(i61)


i62 = Ingredient(
name = "spinach")
db.session.add(i62)


i63 = Ingredient(
name = "artichoke hearts")
db.session.add(i63)


i64 = Ingredient(
name = "mayonnaise")
db.session.add(i64)


i65 = Ingredient(
name = "sour cream")
db.session.add(i65)


i66 = Ingredient(
name = "cream cheese")
db.session.add(i66)


i67 = Ingredient(
name = "red bell pepper")
db.session.add(i67)


i68 = Ingredient(
name = "green bell pepper")
db.session.add(i68)


i69 = Ingredient(
name = "large onion")
db.session.add(i69)


i70 = Ingredient(
name = "flour tortillas")
db.session.add(i70)


i71 = Ingredient(
name = "fajita seasoning mix")
db.session.add(i71)


i72 = Ingredient(
name = "lime juice")
db.session.add(i72)


i73 = Ingredient(
name = "almond milk")
db.session.add(i73)


i74 = Ingredient(
name = "chia seeds")
db.session.add(i74)


i75 = Ingredient(
name = "fresh blueberries")
db.session.add(i75)

db.session.commit()

# --- Add Tags ---
t0 = Tag(
name = "dinner")
db.session.add(t0)


t1 = Tag(
name = "lunch")
db.session.add(t1)


t2 = Tag(
name = "breakfast")
db.session.add(t2)


t3 = Tag(
name = "snack")
db.session.add(t3)


t4 = Tag(
name = "dessert")
db.session.add(t4)


t5 = Tag(
name = "side")
db.session.add(t5)


t6 = Tag(
name = "vegetarian")
db.session.add(t6)


t7 = Tag(
name = "vegan")
db.session.add(t7)


t8 = Tag(
name = "pescetarian")
db.session.add(t8)


t9 = Tag(
name = "kosher")
db.session.add(t9)


t10 = Tag(
name = "halal")
db.session.add(t10)


t11 = Tag(
name = "gluten-free")
db.session.add(t11)


t12 = Tag(
name = "easy")
db.session.add(t12)


t13 = Tag(
name = "difficult")
db.session.add(t13)

t14 = Tag(
name = "quick")
db.session.add(t14)

t15 = Tag(
name = "oven")
db.session.add(t15)

t16 = Tag(
name = "one-pot")
db.session.add(t16)

t14 = Tag(
name = "quick")
db.session.add(t14)

t15 = Tag(
name = "oven")
db.session.add(t15)

t16 = Tag(
name = "one-pot")
db.session.add(t16)

db.session.commit()

# --- Add Certifications ---
c0 = Certification(
name = "Certified Fundamental Cook")
db.session.add(c0)

c1 = Certification(
name = "Certified Sous Chef")
db.session.add(c1)

c2 = Certification(
name = "Certified Master Baker")
db.session.add(c2)

c3 = Certification(
name = "Certified Working Pastry Chef")
db.session.add(c3)

c4 = Certification(
name = "Retail Bakers of America")
db.session.add(c4)

c5 = Certification(
name = "Certified Pastry Culinarian")
db.session.add(c5)

c6 = Certification(
name = "Certified Foodservice Professional")
db.session.add(c6)

c7 = Certification(
name = "Master Certified Food Executive")
db.session.add(c7)

c8 = Certification(
name = "Certified Chef de Cuisine")
db.session.add(c8)

c9 = Certification(
name = "Certified Personal Chef")
db.session.add(c9)

c10 = Certification(
name = "Certified Executive Chef")
db.session.add(c10)

c11 = Certification(
name = "Certified Decorator")
db.session.add(c11)

c12 = Certification(
name = "Certified Culinary Educator")
db.session.add(c12)

db.session.commit()

# --- Add Recipes ---
r0 = Recipe(title = "Corn Soup", description = "Known in Japan as \"corn potage\", this recipe is made from corn kernels cut from the cob. The soup becomes very smooth and strained after cooking, creating a thick paste-like texture, similar to seafood bisque.", servingSize = 1, estimatedHrs = 0, estimatedMins = 45, is_draft=False, user_id=u1.id)
r0.timestamp = datetime.now(timezone.utc)
r0.pictFile = "207add98-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-corn-potage.png"
r0.dietary_restriction = "Vegan"

db.session.add(r0)
db.session.commit()
r0.tags.add(t5)
r0.tags.add(t6)
db.session.commit()
s00 = RecipeStep(stepNum = 1, description = "Finely dice it", recipe_id = r0.id)
db.session.add(s00)
s01 = RecipeStep(stepNum = 2, description = "Cut corn from cob", recipe_id = r0.id)
db.session.add(s01)
s02 = RecipeStep(stepNum = 3, description = "Spread the butter", recipe_id = r0.id)
db.session.add(s02)
s03 = RecipeStep(stepNum = 4, description = "Stir fry it", recipe_id = r0.id)
db.session.add(s03)
s04 = RecipeStep(stepNum = 5, description = "Boil it", recipe_id = r0.id)
db.session.add(s04)
s05 = RecipeStep(stepNum = 6, description = "Use the mixer", recipe_id = r0.id)
db.session.add(s05)
s06 = RecipeStep(stepNum = 7, description = "Strain", recipe_id = r0.id)
db.session.add(s06)
s07 = RecipeStep(stepNum = 8, description = "Boil it", recipe_id = r0.id)
db.session.add(s07)
db.session.commit()
ri00 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i3.id, amount = 0.5, unit = "unit")
db.session.add(ri00)
ri01 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i9.id, amount = 1, unit = "unit")
db.session.add(ri01)
ri02 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i8.id, amount = 4, unit = "tbsp")
db.session.add(ri02)
ri03 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i6.id, amount = 0.5, unit = "tsp")
db.session.add(ri03)
ri04 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i7.id, amount = 0.5, unit = "tsp")
db.session.add(ri04)
ri05 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i4.id, amount = 0.5, unit = "cup")
db.session.add(ri05)
ri06 = RecipeIngredientUse(recipe_id = r0.id, ingredient_id = i5.id, amount = 1, unit = "cup")
db.session.add(ri06)
db.session.commit()
r1 = Recipe(title = "Avocado Toast", description = "Guacamole spread topped with chilis!", servingSize = 1, estimatedHrs = 0, estimatedMins = 15, is_draft=False, user_id=u1.id)
r1.timestamp = datetime.now(timezone.utc)
r1.pictFile = "2b117cbc-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-avocado-toast.png"

db.session.add(r1)
db.session.commit()
r1.tags.add(t2)
r1.tags.add(t3)
r1.tags.add(t6)
r1.tags.add(t7)
db.session.commit()
s10 = RecipeStep(stepNum = 1, description = "Prep the avocado!", recipe_id = r1.id)
db.session.add(s10)
s11 = RecipeStep(stepNum = 2, description = "Mash the avocado!", recipe_id = r1.id)
db.session.add(s11)
s12 = RecipeStep(stepNum = 3, description = "Slice scallions and chilis!", recipe_id = r1.id)
db.session.add(s12)
s13 = RecipeStep(stepNum = 4, description = "Mix the guacamole!", recipe_id = r1.id)
db.session.add(s13)
s14 = RecipeStep(stepNum = 5, description = "Add salt and pepper!", recipe_id = r1.id)
db.session.add(s14)
s15 = RecipeStep(stepNum = 6, description = "Toast the bread!", recipe_id = r1.id)
db.session.add(s15)
s16 = RecipeStep(stepNum = 7, description = "Spread the guacamole!", recipe_id = r1.id)
db.session.add(s16)
db.session.commit()
ri10 = RecipeIngredientUse(recipe_id = r1.id, ingredient_id = i10.id, amount = 1, unit = "unit")
db.session.add(ri10)
ri11 = RecipeIngredientUse(recipe_id = r1.id, ingredient_id = i11.id, amount = 1, unit = "unit")
db.session.add(ri11)
ri12 = RecipeIngredientUse(recipe_id = r1.id, ingredient_id = i12.id, amount = 1, unit = "unit")
db.session.add(ri12)
ri13 = RecipeIngredientUse(recipe_id = r1.id, ingredient_id = i13.id, amount = 1, unit = "unit")
db.session.add(ri13)
db.session.commit()
r2 = Recipe(title = "Pancakes", description = "A thin and flat round cake prepared from a batter and sometimes milk or water, a pancake is a typically common breakfast food that one cooks using a griddle or frying pan. To cook one just right, one has to make sure they cook both sides and when it loses it's milky softness, its ready. Depending on the region, pancakes may be served at any time of day, with a variety of toppings or fillings including jam, chocolate chips, fruit, whip cream, syrup or even meat.", servingSize = 1, estimatedHrs = 0, estimatedMins = 15, is_draft=False, user_id=u1.id)
r2.timestamp = datetime.now(timezone.utc)
r2.pictFile = "12376e4c-112f-11f1-ba63-1ebf2a7aaad6_cooking-mama-pancakes.webp"

db.session.add(r2)
db.session.commit()
r2.tags.add(t2)
db.session.commit()
s20 = RecipeStep(stepNum = 1, description = "Mix in the ingredients!", recipe_id = r2.id)
db.session.add(s20)
s21 = RecipeStep(stepNum = 2, description = "Flip it!", recipe_id = r2.id)
db.session.add(s21)
db.session.commit()
ri20 = RecipeIngredientUse(recipe_id = r2.id, ingredient_id = i14.id, amount = 1, unit = "unit")
db.session.add(ri20)
ri21 = RecipeIngredientUse(recipe_id = r2.id, ingredient_id = i15.id, amount = 1, unit = "unit")
db.session.add(ri21)
ri22 = RecipeIngredientUse(recipe_id = r2.id, ingredient_id = i5.id, amount = 0.5, unit = "cup")
db.session.add(ri22)
db.session.commit()
r3 = Recipe(title = "Garlic Butter Chicken and Rice", description = "A simple one-pan meal with tender chicken cooked in garlic butter and served over fluffy rice.", servingSize = 2, estimatedHrs = 0, estimatedMins = 40, is_draft=False, user_id=u2.id)
r3.timestamp = datetime.now(timezone.utc)

db.session.add(r3)
db.session.commit()
r3.tags.add(t0)
r3.tags.add(t12)
r3.tags.add(t11)
db.session.commit()
s30 = RecipeStep(stepNum = 1, description = "Season the chicken with salt and pepper.", recipe_id = r3.id)
db.session.add(s30)
s31 = RecipeStep(stepNum = 2, description = "Melt butter in a pan and add minced garlic.", recipe_id = r3.id)
db.session.add(s31)
s32 = RecipeStep(stepNum = 3, description = "Sear the chicken on both sides until golden.", recipe_id = r3.id)
db.session.add(s32)
s33 = RecipeStep(stepNum = 4, description = "Remove chicken and cook rice in the same pan.", recipe_id = r3.id)
db.session.add(s33)
s34 = RecipeStep(stepNum = 5, description = "Return chicken to the pan and simmer until fully cooked.", recipe_id = r3.id)
db.session.add(s34)
db.session.commit()
ri30 = RecipeIngredientUse(recipe_id = r3.id, ingredient_id = i0.id, amount = 2, unit = "lb")
db.session.add(ri30)
ri31 = RecipeIngredientUse(recipe_id = r3.id, ingredient_id = i8.id, amount = 2, unit = "tbsp")
db.session.add(ri31)
ri32 = RecipeIngredientUse(recipe_id = r3.id, ingredient_id = i2.id, amount = 2, unit = "cup")
db.session.add(ri32)
ri33 = RecipeIngredientUse(recipe_id = r3.id, ingredient_id = i6.id, amount = 1, unit = "tsp")
db.session.add(ri33)
ri34 = RecipeIngredientUse(recipe_id = r3.id, ingredient_id = i7.id, amount = 1, unit = "tsp")
db.session.add(ri34)
db.session.commit()
r4 = Recipe(title = "Creamy Zucchini Skillet", description = "A quick stovetop zucchini dish finished with cream and seasoning. Perfect as a side or light lunch.", servingSize = 2, estimatedHrs = 0, estimatedMins = 25, is_draft=False, user_id=u2.id)
r4.timestamp = datetime.now(timezone.utc)

db.session.add(r4)
db.session.commit()
r4.tags.add(t1)
r4.tags.add(t5)
r4.tags.add(t6)
r4.tags.add(t12)
r4.tags.add(t11)
db.session.commit()
s40 = RecipeStep(stepNum = 1, description = "Slice the zucchini into rounds.", recipe_id = r4.id)
db.session.add(s40)
s41 = RecipeStep(stepNum = 2, description = "Dice the onion finely.", recipe_id = r4.id)
db.session.add(s41)
s42 = RecipeStep(stepNum = 3, description = "Melt butter in a skillet.", recipe_id = r4.id)
db.session.add(s42)
s43 = RecipeStep(stepNum = 4, description = "Cook onion until translucent.", recipe_id = r4.id)
db.session.add(s43)
s44 = RecipeStep(stepNum = 5, description = "Add zucchini and sauté until tender.", recipe_id = r4.id)
db.session.add(s44)
s45 = RecipeStep(stepNum = 6, description = "Stir in cream and simmer briefly.", recipe_id = r4.id)
db.session.add(s45)
s46 = RecipeStep(stepNum = 7, description = "Season with salt and pepper.", recipe_id = r4.id)
db.session.add(s46)
db.session.commit()
ri40 = RecipeIngredientUse(recipe_id = r4.id, ingredient_id = i1.id, amount = 2, unit = "unit")
db.session.add(ri40)
ri41 = RecipeIngredientUse(recipe_id = r4.id, ingredient_id = i3.id, amount = 0.5, unit = "unit")
db.session.add(ri41)
ri42 = RecipeIngredientUse(recipe_id = r4.id, ingredient_id = i8.id, amount = 2, unit = "tbsp")
db.session.add(ri42)
ri43 = RecipeIngredientUse(recipe_id = r4.id, ingredient_id = i4.id, amount = 0.5, unit = "cup")
db.session.add(ri43)
ri44 = RecipeIngredientUse(recipe_id = r4.id, ingredient_id = i6.id, amount = 0.5, unit = "tsp")
db.session.add(ri44)
ri45 = RecipeIngredientUse(recipe_id = r4.id, ingredient_id = i7.id, amount = 0.5, unit = "tsp")
db.session.add(ri45)
db.session.commit()
r5 = Recipe(title = "Simple Corn Fried Rice", description = "A fast fried rice using corn, onion, and butter for a comforting weeknight meal.", servingSize = 2, estimatedHrs = 0, estimatedMins = 30, is_draft=False, user_id=u2.id)
r5.timestamp = datetime.now(timezone.utc)

db.session.add(r5)
db.session.commit()
r5.tags.add(t0)
r5.tags.add(t12)
r5.tags.add(t6)
db.session.commit()
s50 = RecipeStep(stepNum = 1, description = "Cook the rice and let it cool slightly.", recipe_id = r5.id)
db.session.add(s50)
s51 = RecipeStep(stepNum = 2, description = "Dice the onion.", recipe_id = r5.id)
db.session.add(s51)
s52 = RecipeStep(stepNum = 3, description = "Melt butter in a pan.", recipe_id = r5.id)
db.session.add(s52)
s53 = RecipeStep(stepNum = 4, description = "Sauté onion until soft.", recipe_id = r5.id)
db.session.add(s53)
s54 = RecipeStep(stepNum = 5, description = "Add corn and cook briefly.", recipe_id = r5.id)
db.session.add(s54)
s55 = RecipeStep(stepNum = 6, description = "Stir in rice and fry until heated through.", recipe_id = r5.id)
db.session.add(s55)
s56 = RecipeStep(stepNum = 7, description = "Season with salt and pepper.", recipe_id = r5.id)
db.session.add(s56)
db.session.commit()
ri50 = RecipeIngredientUse(recipe_id = r5.id, ingredient_id = i2.id, amount = 2, unit = "cup")
db.session.add(ri50)
ri51 = RecipeIngredientUse(recipe_id = r5.id, ingredient_id = i9.id, amount = 1, unit = "unit")
db.session.add(ri51)
ri52 = RecipeIngredientUse(recipe_id = r5.id, ingredient_id = i3.id, amount = 0.5, unit = "unit")
db.session.add(ri52)
ri53 = RecipeIngredientUse(recipe_id = r5.id, ingredient_id = i8.id, amount = 2, unit = "tbsp")
db.session.add(ri53)
ri54 = RecipeIngredientUse(recipe_id = r5.id, ingredient_id = i6.id, amount = 1, unit = "tsp")
db.session.add(ri54)
ri55 = RecipeIngredientUse(recipe_id = r5.id, ingredient_id = i7.id, amount = 1, unit = "tsp")
db.session.add(ri55)
db.session.commit()
r6 = Recipe(title = "Herb Roasted Chicken with Vegetables", description = "A comforting oven-roasted chicken dish layered with aromatic herbs, tender zucchini, sweet corn, and caramelized onion. The vegetables roast in the chicken drippings, creating a rich and savory flavor throughout. This hearty meal is perfect for a relaxed dinner and makes excellent leftovers.", servingSize = 4, estimatedHrs = 1, estimatedMins = 15, is_draft=False, user_id=u2.id)
r6.timestamp = datetime.now(timezone.utc)

db.session.add(r6)
db.session.commit()
r6.tags.add(t0)
r6.tags.add(t11)
r6.tags.add(t13)
db.session.commit()
s60 = RecipeStep(stepNum = 1, description = "Preheat the oven to 400 degrees F.", recipe_id = r6.id)
db.session.add(s60)
s61 = RecipeStep(stepNum = 2, description = "Pat the chicken dry and season generously with salt, pepper, thyme, and rosemary.", recipe_id = r6.id)
db.session.add(s61)
s62 = RecipeStep(stepNum = 3, description = "Chop zucchini, onion, and corn into bite-sized pieces.", recipe_id = r6.id)
db.session.add(s62)
s63 = RecipeStep(stepNum = 4, description = "Melt butter and toss vegetables with olive oil, garlic, and a pinch of salt.", recipe_id = r6.id)
db.session.add(s63)
s64 = RecipeStep(stepNum = 5, description = "Spread vegetables evenly in a roasting pan.", recipe_id = r6.id)
db.session.add(s64)
s65 = RecipeStep(stepNum = 6, description = "Place seasoned chicken on top of the vegetables.", recipe_id = r6.id)
db.session.add(s65)
s66 = RecipeStep(stepNum = 7, description = "Roast for 60–75 minutes until the chicken reaches a safe internal temperature.", recipe_id = r6.id)
db.session.add(s66)
s67 = RecipeStep(stepNum = 8, description = "Let the chicken rest for 10 minutes before carving and serving with roasted vegetables.", recipe_id = r6.id)
db.session.add(s67)
db.session.commit()
ri60 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i0.id, amount = 1, unit = "lb")
db.session.add(ri60)
ri61 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i1.id, amount = 2, unit = "unit")
db.session.add(ri61)
ri62 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i3.id, amount = 1, unit = "unit")
db.session.add(ri62)
ri63 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i9.id, amount = 2, unit = "unit")
db.session.add(ri63)
ri64 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i8.id, amount = 2, unit = "tbsp")
db.session.add(ri64)
ri65 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i16.id, amount = 2, unit = "tbsp")
db.session.add(ri65)
ri66 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i17.id, amount = 2, unit = "tsp")
db.session.add(ri66)
ri67 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i18.id, amount = 2, unit = "tsp")
db.session.add(ri67)
ri68 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i6.id, amount = 2, unit = "tsp")
db.session.add(ri68)
ri69 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i7.id, amount = 1, unit = "tsp")
db.session.add(ri69)
ri610 = RecipeIngredientUse(recipe_id = r6.id, ingredient_id = i19.id, amount = 3, unit = "unit")
db.session.add(ri610)
db.session.commit()
r7 = Recipe(title = "Creamy Garlic Parmesan Pasta", description = "A rich and indulgent pasta coated in a velvety garlic cream sauce and finished with freshly grated parmesan. This dish balances savory depth with creamy smoothness and can be prepared quickly for an elegant weeknight dinner.", servingSize = 3, estimatedHrs = 0, estimatedMins = 35, is_draft=False, user_id=u2.id)
r7.timestamp = datetime.now(timezone.utc)

db.session.add(r7)
db.session.commit()
r7.tags.add(t0)
r7.tags.add(t6)
db.session.commit()
s70 = RecipeStep(stepNum = 1, description = "Bring a large pot of salted water to a boil.", recipe_id = r7.id)
db.session.add(s70)
s71 = RecipeStep(stepNum = 2, description = "Cook pasta according to package instructions until al dente.", recipe_id = r7.id)
db.session.add(s71)
s72 = RecipeStep(stepNum = 3, description = "Melt butter in a saucepan over medium heat.", recipe_id = r7.id)
db.session.add(s72)
s73 = RecipeStep(stepNum = 4, description = "Add minced garlic and sauté until fragrant but not browned.", recipe_id = r7.id)
db.session.add(s73)
s74 = RecipeStep(stepNum = 5, description = "Pour in cream and simmer gently for 5–7 minutes.", recipe_id = r7.id)
db.session.add(s74)
s75 = RecipeStep(stepNum = 6, description = "Stir in grated parmesan until melted and smooth.", recipe_id = r7.id)
db.session.add(s75)
s76 = RecipeStep(stepNum = 7, description = "Season with salt and pepper to taste.", recipe_id = r7.id)
db.session.add(s76)
s77 = RecipeStep(stepNum = 8, description = "Toss drained pasta in the sauce and garnish with chopped parsley before serving.", recipe_id = r7.id)
db.session.add(s77)
db.session.commit()
ri70 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i20.id, amount = 12, unit = "oz")
db.session.add(ri70)
ri71 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i8.id, amount = 2, unit = "tbsp")
db.session.add(ri71)
ri72 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i19.id, amount = 3, unit = "unit")
db.session.add(ri72)
ri73 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i4.id, amount = 1.5, unit = "cup")
db.session.add(ri73)
ri74 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i21.id, amount = 1, unit = "cup")
db.session.add(ri74)
ri75 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i6.id, amount = 1, unit = "tsp")
db.session.add(ri75)
ri76 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i7.id, amount = 1, unit = "tsp")
db.session.add(ri76)
ri77 = RecipeIngredientUse(recipe_id = r7.id, ingredient_id = i22.id, amount = 2, unit = "tbsp")
db.session.add(ri77)
db.session.commit()
r8 = Recipe(title = "Vegetable Stir Fry with Soy Ginger Sauce", description = "A vibrant and colorful stir fry featuring crisp vegetables tossed in a savory soy-ginger sauce. This flexible recipe works well as a main dish over rice or as a flavorful side.", servingSize = 2, estimatedHrs = 0, estimatedMins = 25, is_draft=False, user_id=u2.id)
r8.timestamp = datetime.now(timezone.utc)

db.session.add(r8)
db.session.commit()
r8.tags.add(t0)
r8.tags.add(t7)
r8.tags.add(t12)
db.session.commit()
s80 = RecipeStep(stepNum = 1, description = "Prepare all vegetables by slicing them into uniform pieces.", recipe_id = r8.id)
db.session.add(s80)
s81 = RecipeStep(stepNum = 2, description = "Heat sesame oil in a wok over high heat.", recipe_id = r8.id)
db.session.add(s81)
s82 = RecipeStep(stepNum = 3, description = "Add garlic and ginger and cook briefly until fragrant.", recipe_id = r8.id)
db.session.add(s82)
s83 = RecipeStep(stepNum = 4, description = "Add vegetables and stir fry quickly to retain crisp texture.", recipe_id = r8.id)
db.session.add(s83)
s84 = RecipeStep(stepNum = 5, description = "Mix soy sauce, a splash of rice vinegar, and a pinch of sugar in a bowl.", recipe_id = r8.id)
db.session.add(s84)
s85 = RecipeStep(stepNum = 6, description = "Pour sauce into the wok and toss to coat evenly.", recipe_id = r8.id)
db.session.add(s85)
s86 = RecipeStep(stepNum = 7, description = "Cook for another 2–3 minutes until slightly thickened.", recipe_id = r8.id)
db.session.add(s86)
s87 = RecipeStep(stepNum = 8, description = "Serve immediately over steamed rice.", recipe_id = r8.id)
db.session.add(s87)
db.session.commit()
ri80 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i1.id, amount = 1, unit = "unit")
db.session.add(ri80)
ri81 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i23.id, amount = 1, unit = "unit")
db.session.add(ri81)
ri82 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i24.id, amount = 1, unit = "unit")
db.session.add(ri82)
ri83 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i25.id, amount = 2, unit = "tbsp")
db.session.add(ri83)
ri84 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i26.id, amount = 1, unit = "tbsp")
db.session.add(ri84)
ri85 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i27.id, amount = 1, unit = "tbsp")
db.session.add(ri85)
ri86 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i28.id, amount = 1, unit = "tsp")
db.session.add(ri86)
ri87 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i19.id, amount = 2, unit = "unit")
db.session.add(ri87)
ri88 = RecipeIngredientUse(recipe_id = r8.id, ingredient_id = i29.id, amount = 1, unit = "tsp")
db.session.add(ri88)
db.session.commit()
r9 = Recipe(title = "Classic Buttermilk Pancakes", description = "Fluffy and golden pancakes made with tangy buttermilk for extra tenderness. These pancakes are light, airy, and perfect for stacking high with syrup, butter, or fresh fruit.", servingSize = 4, estimatedHrs = 0, estimatedMins = 30, is_draft=False, user_id=u2.id)
r9.timestamp = datetime.now(timezone.utc)

db.session.add(r9)
db.session.commit()
r9.tags.add(t2)
r9.tags.add(t6)
db.session.commit()
s90 = RecipeStep(stepNum = 1, description = "In a bowl, whisk together flour, sugar, baking powder, baking soda, and salt.", recipe_id = r9.id)
db.session.add(s90)
s91 = RecipeStep(stepNum = 2, description = "In another bowl, mix buttermilk, eggs, and melted butter.", recipe_id = r9.id)
db.session.add(s91)
s92 = RecipeStep(stepNum = 3, description = "Combine wet and dry ingredients gently until just mixed.", recipe_id = r9.id)
db.session.add(s92)
s93 = RecipeStep(stepNum = 4, description = "Heat a lightly buttered skillet over medium heat.", recipe_id = r9.id)
db.session.add(s93)
s94 = RecipeStep(stepNum = 5, description = "Pour batter onto the skillet and cook until bubbles form on the surface.", recipe_id = r9.id)
db.session.add(s94)
s95 = RecipeStep(stepNum = 6, description = "Flip and cook the other side until golden brown.", recipe_id = r9.id)
db.session.add(s95)
s96 = RecipeStep(stepNum = 7, description = "Repeat with remaining batter and serve warm.", recipe_id = r9.id)
db.session.add(s96)
db.session.commit()
ri90 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i30.id, amount = 2, unit = "cup")
db.session.add(ri90)
ri91 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i28.id, amount = 2, unit = "tbsp")
db.session.add(ri91)
ri92 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i31.id, amount = 2, unit = "tsp")
db.session.add(ri92)
ri93 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i32.id, amount = 1, unit = "tsp")
db.session.add(ri93)
ri94 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i33.id, amount = 2, unit = "cup")
db.session.add(ri94)
ri95 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i15.id, amount = 2, unit = "unit")
db.session.add(ri95)
ri96 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i8.id, amount = 3, unit = "tbsp")
db.session.add(ri96)
ri97 = RecipeIngredientUse(recipe_id = r9.id, ingredient_id = i6.id, amount = 1, unit = "tsp")
db.session.add(ri97)
db.session.commit()
r10 = Recipe(title = "Chocolate Chip Cookies", description = "Soft-centered cookies with crisp edges and generous pockets of melted chocolate chips. This timeless dessert is easy to prepare and perfect for sharing.", servingSize = 24, estimatedHrs = 0, estimatedMins = 45, is_draft=False, user_id=u2.id)
r10.timestamp = datetime.now(timezone.utc)

db.session.add(r10)
db.session.commit()
r10.tags.add(t4)
r10.tags.add(t6)
db.session.commit()
s100 = RecipeStep(stepNum = 1, description = "Preheat the oven to 350 degrees F.", recipe_id = r10.id)
db.session.add(s100)
s101 = RecipeStep(stepNum = 2, description = "Cream softened butter with brown sugar and white sugar until fluffy.", recipe_id = r10.id)
db.session.add(s101)
s102 = RecipeStep(stepNum = 3, description = "Add eggs one at a time, mixing well after each addition.", recipe_id = r10.id)
db.session.add(s102)
s103 = RecipeStep(stepNum = 4, description = "Stir in vanilla extract.", recipe_id = r10.id)
db.session.add(s103)
s104 = RecipeStep(stepNum = 5, description = "In a separate bowl, whisk flour, baking soda, and salt.", recipe_id = r10.id)
db.session.add(s104)
s105 = RecipeStep(stepNum = 6, description = "Gradually combine dry ingredients into the wet mixture.", recipe_id = r10.id)
db.session.add(s105)
s106 = RecipeStep(stepNum = 7, description = "Fold in chocolate chips evenly.", recipe_id = r10.id)
db.session.add(s106)
s107 = RecipeStep(stepNum = 8, description = "Scoop dough onto a baking sheet and bake for 10–12 minutes until golden.", recipe_id = r10.id)
db.session.add(s107)
s108 = RecipeStep(stepNum = 9, description = "Cool on a rack before serving.", recipe_id = r10.id)
db.session.add(s108)
db.session.commit()
ri100 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i30.id, amount = 2.25, unit = "cup")
db.session.add(ri100)
ri101 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i8.id, amount = 1, unit = "cup")
db.session.add(ri101)
ri102 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i28.id, amount = 0.75, unit = "cup")
db.session.add(ri102)
ri103 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i34.id, amount = 0.75, unit = "cup")
db.session.add(ri103)
ri104 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i15.id, amount = 2, unit = "unit")
db.session.add(ri104)
ri105 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i35.id, amount = 1, unit = "tsp")
db.session.add(ri105)
ri106 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i32.id, amount = 1, unit = "tsp")
db.session.add(ri106)
ri107 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i6.id, amount = 1, unit = "tsp")
db.session.add(ri107)
ri108 = RecipeIngredientUse(recipe_id = r10.id, ingredient_id = i36.id, amount = 2, unit = "cup")
db.session.add(ri108)
db.session.commit()
r11 = Recipe(title = "Spinach Lemon Chicken Bake", description = "This spinach lemon chicken bake features tender, moist chicken baked atop spinach in a bright lemon and rosemary cream sauce.", servingSize = 4, estimatedHrs = 0, estimatedMins = 45, is_draft=False, user_id=u3.id)
r11.timestamp = datetime.now(timezone.utc)
r11.pictFile = "b9ce822c-0c6f-11f1-bc73-b61437af3a7f_8788434-Spinach-Lemon-Chicken-Bake-ddmfs-4x3-beauty-b685b260cdc841d09f464d9a5b775846.webp"

db.session.add(r11)
db.session.commit()
r11.tags.add(t12)
r11.tags.add(t0)
db.session.commit()
s110 = RecipeStep(stepNum = 1, description = "Gather all ingredients.", recipe_id = r11.id)
db.session.add(s110)
s111 = RecipeStep(stepNum = 2, description = "Thinly slice the onion, mince the garlic, and chop the rosemary", recipe_id = r11.id)
db.session.add(s111)
s112 = RecipeStep(stepNum = 3, description = "Preheat the oven to 400 degrees F (200 degrees C).", recipe_id = r11.id)
db.session.add(s112)
s113 = RecipeStep(stepNum = 4, description = "Place a chicken breast between two sheets of plastic wrap and set on a cutting board. Pound with a meat mallet to 1/2-inch thickness. Repeat with remaining chicken.", recipe_id = r11.id)
db.session.add(s113)
s114 = RecipeStep(stepNum = 5, description = "Sprinkle chicken with salt and pepper. Then sprinkle chicken generously with flour, shaking off excess.", recipe_id = r11.id)
db.session.add(s114)
s115 = RecipeStep(stepNum = 6, description = "Heat oil in an ovenproof 12-inch skillet over medium-high heat. Add chicken to the skillet and brown 3 minutes per side (chicken may not be fully cooked). Transfer chicken from the skillet to a plate.", recipe_id = r11.id)
db.session.add(s115)
s116 = RecipeStep(stepNum = 7, description = "Reduce heat to medium. Add onion to the skillet; cook and stir until tender, 4 minutes. Add garlic; cook and stir until fragrant, 1 minute more.", recipe_id = r11.id)
db.session.add(s116)
s117 = RecipeStep(stepNum = 8, description = "Add broth, cream, lemon zest and juice, rosemary, and crushed red pepper. Bring to a boil, about 2 minutes.", recipe_id = r11.id)
db.session.add(s117)
s118 = RecipeStep(stepNum = 9, description = "Add spinach, in batches, stirring until wilted, about 1 minute.", recipe_id = r11.id)
db.session.add(s118)
s119 = RecipeStep(stepNum = 10, description = "Stir in 1/4 cup Parmesan cheese and simmer until desired consistency, about 5 minutes.", recipe_id = r11.id)
db.session.add(s119)
s1110 = RecipeStep(stepNum = 11, description = "Return chicken to skillet. Sprinkle with remaining 1/4 cup Parmesan cheese.", recipe_id = r11.id)
db.session.add(s1110)
s1111 = RecipeStep(stepNum = 12, description = "Bake in the preheated oven until chicken is cooked through and sauce is bubbling, 10 to 15 minutes. An instant read thermometer, inserted into the thickest part of chicken, should read 165 degrees F (74 degrees C).", recipe_id = r11.id)
db.session.add(s1111)
s1112 = RecipeStep(stepNum = 13, description = "Serve garnished with lemon slices.", recipe_id = r11.id)
db.session.add(s1112)
db.session.commit()
ri110 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i37.id, amount = 4, unit = "oz")
db.session.add(ri110)
ri111 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i6.id, amount = 0.5, unit = "tsp")
db.session.add(ri111)
ri112 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i7.id, amount = 0.25, unit = "tsp")
db.session.add(ri112)
ri113 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i30.id, amount = 2, unit = "tbsp")
db.session.add(ri113)
ri114 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i16.id, amount = 2, unit = "tbsp")
db.session.add(ri114)
ri115 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i3.id, amount = 1, unit = "unit")
db.session.add(ri115)
ri116 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i19.id, amount = 3, unit = "unit")
db.session.add(ri116)
ri117 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i38.id, amount = 0.75, unit = "cup")
db.session.add(ri117)
ri118 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i39.id, amount = 0.5, unit = "cup")
db.session.add(ri118)
ri119 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i40.id, amount = 1, unit = "tsp")
db.session.add(ri119)
ri1110 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i41.id, amount = 3, unit = "tbsp")
db.session.add(ri1110)
ri1111 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i18.id, amount = 1, unit = "tsp")
db.session.add(ri1111)
ri1112 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i42.id, amount = 0.25, unit = "tsp")
db.session.add(ri1112)
ri1113 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i43.id, amount = 2, unit = "unit")
db.session.add(ri1113)
ri1114 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i44.id, amount = 0.5, unit = "cup")
db.session.add(ri1114)
db.session.commit()
r12 = Recipe(title = "The Original Marry Me Chicken", description = "", servingSize = 5, estimatedHrs = 0, estimatedMins = 40, is_draft=False, user_id=u4.id)
r12.timestamp = datetime.now(timezone.utc)
r12.pictFile = "d39f391b-0e9e-11f1-afc8-502e919fa289_marrymechicken.jpg"

db.session.add(r12)
db.session.commit()
r12.tags.add(t0)
db.session.commit()
s120 = RecipeStep(stepNum = 1, description = "Finely chop garlic and sundried tomatoes", recipe_id = r12.id)
db.session.add(s120)
s121 = RecipeStep(stepNum = 2, description = "Arrange a rack in center of oven; preheat to 375°.", recipe_id = r12.id)
db.session.add(s121)
s122 = RecipeStep(stepNum = 3, description = "In a large ovenproof skillet over medium-high heat, heat 1 Tbsp. oil.", recipe_id = r12.id)
db.session.add(s122)
s123 = RecipeStep(stepNum = 4, description = "Generously season chicken with salt and black pepper and cook, turning halfway through, until golden brown, about 5 minutes per side.", recipe_id = r12.id)
db.session.add(s123)
s124 = RecipeStep(stepNum = 5, description = "Transfer chicken to a plate.", recipe_id = r12.id)
db.session.add(s124)
s125 = RecipeStep(stepNum = 6, description = "In same skillet over medium heat, heat remaining 2 Tbsp. oil.", recipe_id = r12.id)
db.session.add(s125)
s126 = RecipeStep(stepNum = 7, description = "Stir in garlic, thyme, and red pepper flakes. Cook, stirring, until fragrant, about 1 minute.", recipe_id = r12.id)
db.session.add(s126)
s127 = RecipeStep(stepNum = 8, description = "Stir in broth, tomatoes, cream, and Parmesan; season with salt.", recipe_id = r12.id)
db.session.add(s127)
s128 = RecipeStep(stepNum = 9, description = "Bring to a simmer, then return chicken and any accumulated juices to skillet.", recipe_id = r12.id)
db.session.add(s128)
s129 = RecipeStep(stepNum = 10, description = "Transfer skillet to oven. Bake chicken until cooked through and an instant-read thermometer inserted into thickest part registers 165°, 10 to 12 minutes.", recipe_id = r12.id)
db.session.add(s129)
s1210 = RecipeStep(stepNum = 11, description = "Arrange chicken on a platter. Spoon sauce over. Top with basil.", recipe_id = r12.id)
db.session.add(s1210)
db.session.commit()
ri120 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i16.id, amount = 3, unit = "tbsp")
db.session.add(ri120)
ri121 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i37.id, amount = 4, unit = "unit")
db.session.add(ri121)
ri122 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i19.id, amount = 2, unit = "unit")
db.session.add(ri122)
ri123 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i17.id, amount = 1, unit = "tbsp")
db.session.add(ri123)
ri124 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i45.id, amount = 1, unit = "tsp")
db.session.add(ri124)
ri125 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i38.id, amount = 0.75, unit = "cup")
db.session.add(ri125)
ri126 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i46.id, amount = 0.5, unit = "cup")
db.session.add(ri126)
ri127 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i39.id, amount = 0.5, unit = "cup")
db.session.add(ri127)
ri128 = RecipeIngredientUse(recipe_id = r12.id, ingredient_id = i21.id, amount = 0.25, unit = "cup")
db.session.add(ri128)
db.session.commit()
r13 = Recipe(title = "Chef John's Shrimp and Grits", description = "This classic Southern meal features the heat of jalapeño, cayenne, and Cajun seasoning. Absolutely delicious and very easy to execute.", servingSize = 4, estimatedHrs = 0, estimatedMins = 55, is_draft=False, user_id=u3.id)
r13.timestamp = datetime.now(timezone.utc)
r13.pictFile = "9e4844d0-11b9-11f1-9542-1ebf2a7aaad6_shrimp-grits.webp"

db.session.add(r13)
db.session.commit()
r13.tags.add(t0)
db.session.commit()
s130 = RecipeStep(stepNum = 1, description = "Gather the ingredients", recipe_id = r13.id)
db.session.add(s130)
s131 = RecipeStep(stepNum = 2, description = "Cut the 4 strips of bacon into 1/4-inch pieces", recipe_id = r13.id)
db.session.add(s131)
s132 = RecipeStep(stepNum = 3, description = "Mince jalapeno pepper, green onion, garlic, and chop parsley", recipe_id = r13.id)
db.session.add(s132)
s133 = RecipeStep(stepNum = 4, description = "Cook bacon in a large skillet over medium-high heat, turning occasionally, until almost crisp, 5 to 7 minutes.", recipe_id = r13.id)
db.session.add(s133)
s134 = RecipeStep(stepNum = 5, description = "Transfer bacon to a dish; reserve drippings in the skillet.", recipe_id = r13.id)
db.session.add(s134)
s135 = RecipeStep(stepNum = 6, description = "Whisk 1/4 cup water, cream, lemon juice, and Worcestershire sauce together in a bowl.", recipe_id = r13.id)
db.session.add(s135)
s136 = RecipeStep(stepNum = 7, description = "Combine 4 cups water, butter, and 1 teaspoon salt in a pot; bring to a boil. Whisk in grits; bring to a simmer, reduce heat to low, and cook until creamy, 20 to 25 minutes.", recipe_id = r13.id)
db.session.add(s136)
s137 = RecipeStep(stepNum = 8, description = "Take the mixture off heat, and stir in cheddar cheese", recipe_id = r13.id)
db.session.add(s137)
s138 = RecipeStep(stepNum = 9, description = "Season shrimp with Cajun seasoning, 1/2 teaspoon salt, black pepper, and a pinch of cayenne pepper in a large bowl.", recipe_id = r13.id)
db.session.add(s138)
s139 = RecipeStep(stepNum = 10, description = "Heat bacon drippings in the skillet over high heat. Add shrimp; cook 1 minute.", recipe_id = r13.id)
db.session.add(s139)
s1310 = RecipeStep(stepNum = 11, description = "Flip shrimp; add jalapeño and cook until fragrant, about 30 seconds.", recipe_id = r13.id)
db.session.add(s1310)
s1311 = RecipeStep(stepNum = 12, description = "Stir cream mixture, bacon, green onion, and garlic into shrimp mixture; cook and stir until shrimp cooked through, 3 to 4 minutes, adding water as necessary to thin sauce.", recipe_id = r13.id)
db.session.add(s1311)
s1312 = RecipeStep(stepNum = 13, description = "Take off heat, and stir in parsley", recipe_id = r13.id)
db.session.add(s1312)
s1313 = RecipeStep(stepNum = 14, description = "Ladle grits into a bowl; top with shrimp and sauce.", recipe_id = r13.id)
db.session.add(s1313)
db.session.commit()
ri130 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i47.id, amount = 4, unit = "unit")
db.session.add(ri130)
ri131 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i48.id, amount = 4.25, unit = "cup")
db.session.add(ri131)
ri132 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i39.id, amount = 2, unit = "tbsp")
db.session.add(ri132)
ri133 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i41.id, amount = 2, unit = "tsp")
db.session.add(ri133)
ri134 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i49.id, amount = 0.125, unit = "tsp")
db.session.add(ri134)
ri135 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i50.id, amount = 2, unit = "tbsp")
db.session.add(ri135)
ri136 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i6.id, amount = 1.5, unit = "tsp")
db.session.add(ri136)
ri137 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i51.id, amount = 1, unit = "cup")
db.session.add(ri137)
ri138 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i52.id, amount = 0.5, unit = "cup")
db.session.add(ri138)
ri139 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i53.id, amount = 1, unit = "lb")
db.session.add(ri139)
ri1310 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i54.id, amount = 0.5, unit = "tsp")
db.session.add(ri1310)
ri1311 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i7.id, amount = 0.25, unit = "tsp")
db.session.add(ri1311)
ri1312 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i55.id, amount = 1, unit = "tbsp")
db.session.add(ri1312)
ri1313 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i56.id, amount = 2, unit = "tbsp")
db.session.add(ri1313)
ri1314 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i19.id, amount = 3, unit = "unit")
db.session.add(ri1314)
ri1315 = RecipeIngredientUse(recipe_id = r13.id, ingredient_id = i22.id, amount = 1, unit = "tbsp")
db.session.add(ri1315)
db.session.commit()
r14 = Recipe(title = "Chocolate Peanut Butter Protein Bars", description = "Chocolate peanut butter protein bars are easy to make in a small batch, and absolutely delicious. Using a good protein powder is the key. If there is a downside, it might be how hard it will be to only eat one.", servingSize = 4, estimatedHrs = 0, estimatedMins = 40, is_draft=False, user_id=u3.id)
r14.timestamp = datetime.now(timezone.utc)
r14.pictFile = "91e18a80-11b9-11f1-9542-1ebf2a7aaad6_Chocolate-Peanut-Butter-Protein-Bars.webp"

db.session.add(r14)
db.session.commit()
r14.tags.add(t4)
r14.tags.add(t12)
db.session.commit()
s140 = RecipeStep(stepNum = 1, description = "Line an 8 1/2x4 1/2-inch loaf pan with parchment paper, leaving overhang on all sides to make it easy to remove bars from the pan. Set aside.", recipe_id = r14.id)
db.session.add(s140)
s141 = RecipeStep(stepNum = 2, description = "Place peanut butter, protein powder, maple syrup, vanilla and salt in a bowl and mix until well combined; press into the prepared pan. Set aside.", recipe_id = r14.id)
db.session.add(s141)
s142 = RecipeStep(stepNum = 3, description = "Place chocolate chips and oil in a microwave safe bowl. Microwave for 30 seconds, stir. Repeat until chips are completely melted when stirred. Pour over bars, smooth chocolate. Refrigerate until set, about 30 minutes. Cut into 8 bars.", recipe_id = r14.id)
db.session.add(s142)
db.session.commit()
ri140 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i57.id, amount = 0.75, unit = "cup")
db.session.add(ri140)
ri141 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i58.id, amount = 0.5, unit = "cup")
db.session.add(ri141)
ri142 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i59.id, amount = 2, unit = "tbsp")
db.session.add(ri142)
ri143 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i35.id, amount = 1, unit = "tsp")
db.session.add(ri143)
ri144 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i6.id, amount = 0.125, unit = "tsp")
db.session.add(ri144)
ri145 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i36.id, amount = 0.5, unit = "cup")
db.session.add(ri145)
ri146 = RecipeIngredientUse(recipe_id = r14.id, ingredient_id = i60.id, amount = 1, unit = "tsp")
db.session.add(ri146)
db.session.commit()
r15 = Recipe(title = "Artichoke Dip Wonton Cups", description = "These artichoke dip wonton cups are a fun twist on the traditional spinach artichoke dip with tortilla chips. Served as individual bites, they're ideal for a party.", servingSize = 4, estimatedHrs = 0, estimatedMins = 30, is_draft=False, user_id=u3.id)
r15.timestamp = datetime.now(timezone.utc)
r15.pictFile = "81e670d2-11b9-11f1-9542-1ebf2a7aaad6_artichoke-dip-wonton-cups.webp"

db.session.add(r15)
db.session.commit()
r15.tags.add(t3)
r15.tags.add(t12)
db.session.commit()
s150 = RecipeStep(stepNum = 1, description = "Preheat the oven to 350 degrees F (180 degrees C). Spray a standard 12-cup muffin tin with cooking spray.", recipe_id = r15.id)
db.session.add(s150)
s151 = RecipeStep(stepNum = 2, description = "Line each muffin cup with a wonton wrapper. Press the center of the wrapper down into the cup, leaving the edges sticking up out of the cup. Spray each wrapper lightly with cooking spray.", recipe_id = r15.id)
db.session.add(s151)
s152 = RecipeStep(stepNum = 3, description = "Bake cups in the preheated oven for 5 minutes, then remove from the oven.Add spinach, artichoke hearts, mayonnaise, sour cream, cream cheese, Parmesan cheese, and garlic in a bowl until well incorporated. Divide mixture evenly between wonton cups.", recipe_id = r15.id)
db.session.add(s152)
s153 = RecipeStep(stepNum = 4, description = "Return to the oven and bake until filling is heated through and edges of wrappers are golden brown, about 15 minutes.", recipe_id = r15.id)
db.session.add(s153)
db.session.commit()
ri150 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i61.id, amount = 12, unit = "unit")
db.session.add(ri150)
ri151 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i62.id, amount = 5, unit = "oz")
db.session.add(ri151)
ri152 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i63.id, amount = 1, unit = "unit")
db.session.add(ri152)
ri153 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i64.id, amount = 0.33, unit = "cup")
db.session.add(ri153)
ri154 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i65.id, amount = 0.25, unit = "cup")
db.session.add(ri154)
ri155 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i66.id, amount = 2, unit = "oz")
db.session.add(ri155)
ri156 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i44.id, amount = 0.5, unit = "cup")
db.session.add(ri156)
ri157 = RecipeIngredientUse(recipe_id = r15.id, ingredient_id = i19.id, amount = 2, unit = "unit")
db.session.add(ri157)
db.session.commit()
r16 = Recipe(title = "Easy Grilled Shrimp Fajitas", description = "Quick grilled shrimp fajitas with bell peppers, onions, and fajita seasoning served on warm tortillas", servingSize = 4, estimatedHrs = 0, estimatedMins = 40, is_draft=False, user_id=u3.id)
r16.timestamp = datetime.now(timezone.utc)
r16.pictFile = "98cbe5a2-11b9-11f1-9542-1ebf2a7aaad6_shrimp_fajitas.webp"

db.session.add(r16)
db.session.commit()
db.session.commit()
s160 = RecipeStep(stepNum = 1, description = "Preheat an outdoor grill for medium-high heat and lightly oil the grate", recipe_id = r16.id)
db.session.add(s160)
s161 = RecipeStep(stepNum = 2, description = "In a large bowl combine sliced red bell pepper, green bell pepper, onion, jalapeño, 2 teaspoons fajita seasoning, and olive oil; stir until evenly coated", recipe_id = r16.id)
db.session.add(s161)
s162 = RecipeStep(stepNum = 3, description = "In a separate bowl add raw shrimp, remaining 1/2 teaspoon fajita seasoning, and lime juice; gently stir to coat", recipe_id = r16.id)
db.session.add(s162)
s163 = RecipeStep(stepNum = 4, description = "Place the vegetable mixture in a grill basket and cook on the grill for about 10 minutes, stirring occasionally", recipe_id = r16.id)
db.session.add(s163)
s164 = RecipeStep(stepNum = 5, description = "Add the shrimp to the grill basket with the vegetables and cook for about 5 more minutes until shrimp are opaque", recipe_id = r16.id)
db.session.add(s164)
s165 = RecipeStep(stepNum = 6, description = "Remove the grill basket and place the tortillas on the grill to toast for about 2 minutes", recipe_id = r16.id)
db.session.add(s165)
s166 = RecipeStep(stepNum = 7, description = "Divide the shrimp and vegetable filling between the warm tortillas and serve while hot", recipe_id = r16.id)
db.session.add(s166)
db.session.commit()
ri160 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i53.id, amount = 12, unit = "oz")
db.session.add(ri160)
ri161 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i67.id, amount = 1, unit = "unit")
db.session.add(ri161)
ri162 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i68.id, amount = 1, unit = "unit")
db.session.add(ri162)
ri163 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i69.id, amount = 1, unit = "unit")
db.session.add(ri163)
ri164 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i55.id, amount = 1, unit = "unit")
db.session.add(ri164)
ri165 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i70.id, amount = 8, unit = "unit")
db.session.add(ri165)
ri166 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i71.id, amount = 2.5, unit = "tsp")
db.session.add(ri166)
ri167 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i16.id, amount = 1, unit = "tsp")
db.session.add(ri167)
ri168 = RecipeIngredientUse(recipe_id = r16.id, ingredient_id = i72.id, amount = 1, unit = "tbsp")
db.session.add(ri168)
db.session.commit()
r17 = Recipe(title = "Blueberry Chia Pudding with Almond Milk", description = "A light vegan chia pudding made with almond milk, fresh blueberries, and a touch of maple syrup and cinnamon. Great for breakfast or a healthy snack.", servingSize = 3, estimatedHrs = 8, estimatedMins = 10, is_draft=False, user_id=u3.id)
r17.timestamp = datetime.now(timezone.utc)
r17.pictFile = "8a70854e-11b9-11f1-9542-1ebf2a7aaad6_chia_pudding.webp"

db.session.add(r17)
db.session.commit()
r17.tags.add(t2)
r17.tags.add(t7)
r17.tags.add(t11)
r17.tags.add(t4)
db.session.commit()
s170 = RecipeStep(stepNum = 1, description = "Combine almond milk, chia seeds, blueberries, maple syrup, vanilla extract, and cinnamon in a blender; blend until smooth.", recipe_id = r17.id)
db.session.add(s170)
s171 = RecipeStep(stepNum = 2, description = "Pour into glasses or ramekins.", recipe_id = r17.id)
db.session.add(s171)
s172 = RecipeStep(stepNum = 3, description = "Chill until set, about 8 hours or overnight.", recipe_id = r17.id)
db.session.add(s172)
s173 = RecipeStep(stepNum = 4, description = "Serve chilled.", recipe_id = r17.id)
db.session.add(s173)
db.session.commit()
ri170 = RecipeIngredientUse(recipe_id = r17.id, ingredient_id = i73.id, amount = 2, unit = "cup")
db.session.add(ri170)
ri171 = RecipeIngredientUse(recipe_id = r17.id, ingredient_id = i74.id, amount = 6, unit = "tbsp")
db.session.add(ri171)
ri172 = RecipeIngredientUse(recipe_id = r17.id, ingredient_id = i75.id, amount = 0.33, unit = "cup")
db.session.add(ri172)
ri173 = RecipeIngredientUse(recipe_id = r17.id, ingredient_id = i59.id, amount = 1, unit = "tbsp")
db.session.add(ri173)
ri174 = RecipeIngredientUse(recipe_id = r17.id, ingredient_id = i35.id, amount = 0.5, unit = "tsp")
db.session.add(ri174)
db.session.commit()
c0 = Cookbook(title = "Cooking Mama's Recipes", description = "Recipes from the Cooking Mama Franchise", user_id = u1.id)
db.session.add(c0)
c0.pictFile = "9a462e80-1130-11f1-9a14-1ebf2a7aaad6_cooking-mama-cover.jpg"
c0.included_recipes.add(r0)
c0.included_recipes.add(r1)
c0.included_recipes.add(r2)
db.session.commit()
c1 = Cookbook(title = "ChatGPT's Kitchen Creations", description = "A curated collection of comforting dinners, quick breakfasts, indulgent desserts, and flavorful vegetarian dishes designed for both beginners and experienced home cooks.", user_id = u2.id)
db.session.add(c1)
c1.included_recipes.add(r3)
c1.included_recipes.add(r4)
c1.included_recipes.add(r5)
c1.included_recipes.add(r6)
c1.included_recipes.add(r7)
c1.included_recipes.add(r8)
c1.included_recipes.add(r9)
c1.included_recipes.add(r10)
db.session.commit()
c2 = Cookbook(title = "AllRecipe's Cookbook", description = "A collection of Allrecipe's best dishes", user_id = u3.id)
db.session.add(c2)
c2.pictFile = "b4458f2c-11b9-11f1-9542-1ebf2a7aaad6_allrecipes.jpg"
c2.included_recipes.add(r11)
c2.included_recipes.add(r13)
c2.included_recipes.add(r14)
c2.included_recipes.add(r15)
c2.included_recipes.add(r16)
c2.included_recipes.add(r17)
db.session.commit()