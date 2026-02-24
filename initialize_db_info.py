from app import create_app, db
from config import Config
from datetime import datetime, timezone

app = create_app(Config)

from app.main.models import Recipe, Cookbook, User, Ingredient, Tag, RecipeIngredientUse, RecipeStep
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
first_name = "All", last_name = "Recipes", username = "AllRecipes", email = "chef@allrecipes.com", is_certified=False)
u3.set_password("123")
db.session.add(u3)


u4 = User(
first_name = "D", last_name = "Lish", username = "Delish", email = "delish@delish.com", is_certified=True)
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
name = "red pepper flakes")
db.session.add(i38)


i39 = Ingredient(
name = "chicken broth")
db.session.add(i39)


i40 = Ingredient(
name = "sundried-tomates")
db.session.add(i40)


i41 = Ingredient(
name = "heavy cream")
db.session.add(i41)

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
name = "gluten free")
db.session.add(t11)


t12 = Tag(
name = "easy")
db.session.add(t12)


t13 = Tag(
name = "difficult")
db.session.add(t13)

db.session.commit()

# --- Add Recipes ---
r0 = Recipe(title = "Corn Soup", description = "Known in Japan as \"corn potage\", this recipe is made from corn kernels cut from the cob. The soup becomes very smooth and strained after cooking, creating a thick paste-like texture, similar to seafood bisque.", servingSize = 1, estimatedHrs = 0, estimatedMins = 45, is_draft=False, user_id=u1.id)
r0.timestamp = datetime.now(timezone.utc)
r0.pictFile = "207add98-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-corn-potage.png"

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
r11 = Recipe(title = "The Original Marry Me Chicken", description = "", servingSize = 5, estimatedHrs = 0, estimatedMins = 40, is_draft=False, user_id=u4.id)
r11.timestamp = datetime.now(timezone.utc)
r11.pictFile = "d39f391b-0e9e-11f1-afc8-502e919fa289_marrymechicken.jpg"

db.session.add(r11)
db.session.commit()
r11.tags.add(t0)
db.session.commit()
s110 = RecipeStep(stepNum = 1, description = "Finely chop garlic and sundried tomatoesArrange a rack in center of oven; preheat to 375°.", recipe_id = r11.id)
db.session.add(s110)
s111 = RecipeStep(stepNum = 2, description = "In a large ovenproof skillet over medium-high heat, heat 1 Tbsp. oil.", recipe_id = r11.id)
db.session.add(s111)
s112 = RecipeStep(stepNum = 3, description = "Generously season chicken with salt and black pepper and cook, turning halfway through, until golden brown, about 5 minutes per side.", recipe_id = r11.id)
db.session.add(s112)
s113 = RecipeStep(stepNum = 4, description = "Transfer chicken to a plate.", recipe_id = r11.id)
db.session.add(s113)
s114 = RecipeStep(stepNum = 5, description = "In same skillet over medium heat, heat remaining 2 Tbsp. oil.", recipe_id = r11.id)
db.session.add(s114)
s115 = RecipeStep(stepNum = 6, description = "Stir in garlic, thyme, and red pepper flakes. Cook, stirring, until fragrant, about 1 minute.", recipe_id = r11.id)
db.session.add(s115)
s116 = RecipeStep(stepNum = 7, description = "Stir in broth, tomatoes, cream, and Parmesan; season with salt.", recipe_id = r11.id)
db.session.add(s116)
s117 = RecipeStep(stepNum = 8, description = "Bring to a simmer, then return chicken and any accumulated juices to skillet.", recipe_id = r11.id)
db.session.add(s117)
s118 = RecipeStep(stepNum = 9, description = "Transfer skillet to oven. Bake chicken until cooked through and an instant-read thermometer inserted into thickest part registers 165°, 10 to 12 minutes.", recipe_id = r11.id)
db.session.add(s118)
s119 = RecipeStep(stepNum = 10, description = "Arrange chicken on a platter. Spoon sauce over. Top with basil.", recipe_id = r11.id)
db.session.add(s119)
db.session.commit()
ri110 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i16.id, amount = 3, unit = "tbsp")
db.session.add(ri110)
ri111 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i37.id, amount = 4, unit = "unit")
db.session.add(ri111)
ri112 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i19.id, amount = 2, unit = "unit")
db.session.add(ri112)
ri113 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i17.id, amount = 1, unit = "tbsp")
db.session.add(ri113)
ri114 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i38.id, amount = 1, unit = "tsp")
db.session.add(ri114)
ri115 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i39.id, amount = 0.75, unit = "cup")
db.session.add(ri115)
ri116 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i40.id, amount = 0.5, unit = "cup")
db.session.add(ri116)
ri117 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i41.id, amount = 0.5, unit = "cup")
db.session.add(ri117)
ri118 = RecipeIngredientUse(recipe_id = r11.id, ingredient_id = i21.id, amount = 0.25, unit = "cup")
db.session.add(ri118)
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