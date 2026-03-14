

users = [
    ["A", "S", "A2", "a@wpi.edu", "123", False],
    ["Mama", "Nintendo", "CookingMama", "cooking@nintendo.com", "123", True],
    ["Chat", "GPT", "ChatGPT", "chat@chat.com", "123", True],
    ["All", "Recipes", "AllRecipes", "chef@allrecipes.com", "123", True],
    ["D", "Lish", "Delish", "delish@delish.com", "123", False],
]
ingredients = ["chicken", "zucchini", "rice", "onion", "cream", "milk", "salt", "pepper", "butter", "corn"]
tags = ["dinner", "lunch", "breakfast", 
        "snack", "dessert", "side",
        "vegetarian", "vegan", "pescetarian", 
        "kosher", "halal",
        "gluten free",
        "easy", "difficult"]
# title, description, serving size, hrs, mins, user#, picture, tags, steps, ingredients
recipe0 = [
    "Corn Soup", 
    "Known in Japan as \\\"corn potage\\\", this recipe is made from corn kernels cut from the cob. The soup becomes very smooth and strained after cooking, creating a thick paste-like texture, similar to seafood bisque.", 
    1,
    0,
    45,
    1,
    "207add98-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-corn-potage.png",
    ["side", "vegetarian"],
    ["Finely dice it", "Cut corn from cob", "Spread the butter", "Stir fry it", "Boil it", "Use the mixer", "Strain", "Boil it"],
    [
        "0.5, unit, onion",
        "1, unit, corn",
        "4, tbsp, butter",
        "0.5, tsp, salt",
        "0.5, tsp, pepper",
        "0.5, cup, cream",
        "1, cup, milk"
    ]
]
recipe1 = [
    "Avocado Toast", 
    "Guacamole spread topped with chilis!", 
    1,
    0,
    15,
    1,
    "2b117cbc-112c-11f1-a181-1ebf2a7aaad6_cooking-mama-avocado-toast.png",
    ["breakfast", "snack", "vegetarian", "vegan"],
    ["Prep the avocado!", "Mash the avocado!", "Slice scallions and chilis!", "Mix the guacamole!", "Add salt and pepper!", "Toast the bread!", "Spread the guacamole!"],
    [
        "1, unit, avocado",
        "1, unit, scallion",
        "1, unit, chili",
        "1, unit, bread",
    ]
]
recipe2 = [
    "Pancakes", 
    "A thin and flat round cake prepared from a batter and sometimes milk or water, a pancake is a typically common breakfast food that one cooks using a griddle or frying pan. To cook one just right, one has to make sure they cook both sides and when it loses it's milky softness, its ready. Depending on the region, pancakes may be served at any time of day, with a variety of toppings or fillings including jam, chocolate chips, fruit, whip cream, syrup or even meat.", 
    1,
    0,
    15,
    1,
    "12376e4c-112f-11f1-ba63-1ebf2a7aaad6_cooking-mama-pancakes.webp",
    ["breakfast"],
    ["Mix in the ingredients!", "Flip it!"],
    [
        "1, unit, pancake mix",
        "1, unit, egg",
        "0.5, cup, milk",
    ]
]
recipe3 = [
    "Garlic Butter Chicken and Rice",
    "A simple one-pan meal with tender chicken cooked in garlic butter and served over fluffy rice.",
    2,
    0,
    40,
    2,
    "",
    ["dinner", "easy", "gluten free"],
    ["Season the chicken with salt and pepper.",
     "Melt butter in a pan and add minced garlic.",
     "Sear the chicken on both sides until golden.",
     "Remove chicken and cook rice in the same pan.",
     "Return chicken to the pan and simmer until fully cooked."],
    [
        "2, lb, chicken",
        "2, tbsp, butter",
        "2, cup, rice",
        "1, tsp, salt",
        "1, tsp, pepper"
    ]
]
recipe4 = [
    "Creamy Zucchini Skillet",
    "A quick stovetop zucchini dish finished with cream and seasoning. Perfect as a side or light lunch.",
    2,
    0,
    25,
    2,
    "",
    ["lunch", "side", "vegetarian", "easy", "gluten free"],
    ["Slice the zucchini into rounds.",
     "Dice the onion finely.",
     "Melt butter in a skillet.",
     "Cook onion until translucent.",
     "Add zucchini and sauté until tender.",
     "Stir in cream and simmer briefly.",
     "Season with salt and pepper."],
    [
        "2, unit, zucchini",
        "0.5, unit, onion",
        "2, tbsp, butter",
        "0.5, cup, cream",
        "0.5, tsp, salt",
        "0.5, tsp, pepper"
    ]
]
recipe5 = [
    "Simple Corn Fried Rice",
    "A fast fried rice using corn, onion, and butter for a comforting weeknight meal.",
    2,
    0,
    30,
    2,
    "",
    ["dinner", "easy", "vegetarian"],
    ["Cook the rice and let it cool slightly.",
     "Dice the onion.",
     "Melt butter in a pan.",
     "Sauté onion until soft.",
     "Add corn and cook briefly.",
     "Stir in rice and fry until heated through.",
     "Season with salt and pepper."],
    [
        "2, cup, rice",
        "1, unit, corn",
        "0.5, unit, onion",
        "2, tbsp, butter",
        "1, tsp, salt",
        "1, tsp, pepper"
    ]
]
recipe6 = [
    "Herb Roasted Chicken with Vegetables",
    "A comforting oven-roasted chicken dish layered with aromatic herbs, tender zucchini, sweet corn, and caramelized onion. The vegetables roast in the chicken drippings, creating a rich and savory flavor throughout. This hearty meal is perfect for a relaxed dinner and makes excellent leftovers.",
    4,
    1,
    15,
    2,
    "",
    ["dinner", "gluten free", "difficult"],
    ["Preheat the oven to 400 degrees F.",
     "Pat the chicken dry and season generously with salt, pepper, thyme, and rosemary.",
     "Chop zucchini, onion, and corn into bite-sized pieces.",
     "Melt butter and toss vegetables with olive oil, garlic, and a pinch of salt.",
     "Spread vegetables evenly in a roasting pan.",
     "Place seasoned chicken on top of the vegetables.",
     "Roast for 60–75 minutes until the chicken reaches a safe internal temperature.",
     "Let the chicken rest for 10 minutes before carving and serving with roasted vegetables."],
    [
        "1, lb, chicken",
        "2, unit, zucchini",
        "1, unit, onion",
        "2, unit, corn",
        "2, tbsp, butter",
        "2, tbsp, olive oil",
        "2, tsp, thyme",
        "2, tsp, rosemary",
        "2, tsp, salt",
        "1, tsp, pepper",
        "3, unit, garlic"
    ]
]
recipe7 = [
    "Creamy Garlic Parmesan Pasta",
    "A rich and indulgent pasta coated in a velvety garlic cream sauce and finished with freshly grated parmesan. This dish balances savory depth with creamy smoothness and can be prepared quickly for an elegant weeknight dinner.",
    3,
    0,
    35,
    2,
    "",
    ["dinner", "vegetarian"],
    ["Bring a large pot of salted water to a boil.",
     "Cook pasta according to package instructions until al dente.",
     "Melt butter in a saucepan over medium heat.",
     "Add minced garlic and sauté until fragrant but not browned.",
     "Pour in cream and simmer gently for 5–7 minutes.",
     "Stir in grated parmesan until melted and smooth.",
     "Season with salt and pepper to taste.",
     "Toss drained pasta in the sauce and garnish with chopped parsley before serving."],
    [
        "12, oz, pasta",
        "2, tbsp, butter",
        "3, unit, garlic",
        "1.5, cup, cream",
        "1, cup, parmesan",
        "1, tsp, salt",
        "1, tsp, pepper",
        "2, tbsp, parsley"
    ]
]
recipe8 = [
    "Vegetable Stir Fry with Soy Ginger Sauce",
    "A vibrant and colorful stir fry featuring crisp vegetables tossed in a savory soy-ginger sauce. This flexible recipe works well as a main dish over rice or as a flavorful side.",
    2,
    0,
    25,
    2,
    "",
    ["dinner", "vegan", "easy"],
    ["Prepare all vegetables by slicing them into uniform pieces.",
     "Heat sesame oil in a wok over high heat.",
     "Add garlic and ginger and cook briefly until fragrant.",
     "Add vegetables and stir fry quickly to retain crisp texture.",
     "Mix soy sauce, a splash of rice vinegar, and a pinch of sugar in a bowl.",
     "Pour sauce into the wok and toss to coat evenly.",
     "Cook for another 2–3 minutes until slightly thickened.",
     "Serve immediately over steamed rice."],
    [
        "1, unit, zucchini",
        "1, unit, carrot",
        "1, unit, bell pepper",
        "2, tbsp, soy sauce",
        "1, tbsp, sesame oil",
        "1, tbsp, rice vinegar",
        "1, tsp, sugar",
        "2, unit, garlic",
        "1, tsp, ginger"
    ]
]
recipe9 = [
    "Classic Buttermilk Pancakes",
    "Fluffy and golden pancakes made with tangy buttermilk for extra tenderness. These pancakes are light, airy, and perfect for stacking high with syrup, butter, or fresh fruit.",
    4,
    0,
    30,
    2,
    "",
    ["breakfast", "vegetarian"],
    ["In a bowl, whisk together flour, sugar, baking powder, baking soda, and salt.",
     "In another bowl, mix buttermilk, eggs, and melted butter.",
     "Combine wet and dry ingredients gently until just mixed.",
     "Heat a lightly buttered skillet over medium heat.",
     "Pour batter onto the skillet and cook until bubbles form on the surface.",
     "Flip and cook the other side until golden brown.",
     "Repeat with remaining batter and serve warm."],
    [
        "2, cup, flour",
        "2, tbsp, sugar",
        "2, tsp, baking powder",
        "1, tsp, baking soda",
        "2, cup, buttermilk",
        "2, unit, egg",
        "3, tbsp, butter",
        "1, tsp, salt"
    ]
]
recipe10 = [
    "Chocolate Chip Cookies",
    "Soft-centered cookies with crisp edges and generous pockets of melted chocolate chips. This timeless dessert is easy to prepare and perfect for sharing.",
    24,
    0,
    45,
    2,
    "",
    ["dessert", "vegetarian"],
    ["Preheat the oven to 350 degrees F.",
     "Cream softened butter with brown sugar and white sugar until fluffy.",
     "Add eggs one at a time, mixing well after each addition.",
     "Stir in vanilla extract.",
     "In a separate bowl, whisk flour, baking soda, and salt.",
     "Gradually combine dry ingredients into the wet mixture.",
     "Fold in chocolate chips evenly.",
     "Scoop dough onto a baking sheet and bake for 10–12 minutes until golden.",
     "Cool on a rack before serving."],
    [
        "2.25, cup, flour",
        "1, cup, butter",
        "0.75, cup, sugar",
        "0.75, cup, brown sugar",
        "2, unit, egg",
        "1, tsp, vanilla extract",
        "1, tsp, baking soda",
        "1, tsp, salt",
        "2, cup, chocolate chips"
    ]
]
recipe11 = [
    "Spinach Lemon Chicken Bake",
    "This spinach lemon chicken bake features tender, moist chicken baked atop spinach in a bright lemon and rosemary cream sauce.",
    4,
    0,
    45,
    3,
    "b9ce822c-0c6f-11f1-bc73-b61437af3a7f_8788434-Spinach-Lemon-Chicken-Bake-ddmfs-4x3-beauty-b685b260cdc841d09f464d9a5b775846.webp",
    ["easy", "dinner"],
    ["Gather all ingredients.", 
     "Thinly slice the onion, mince the garlic, and chop the rosemary",
     "Preheat the oven to 400 degrees F (200 degrees C).",
     "Place a chicken breast between two sheets of plastic wrap and set on a cutting board. Pound with a meat mallet to 1/2-inch thickness. Repeat with remaining chicken.",
     "Sprinkle chicken with salt and pepper. Then sprinkle chicken generously with flour, shaking off excess.",
     "Heat oil in an ovenproof 12-inch skillet over medium-high heat. Add chicken to the skillet and brown 3 minutes per side (chicken may not be fully cooked). Transfer chicken from the skillet to a plate.",
     "Reduce heat to medium. Add onion to the skillet; cook and stir until tender, 4 minutes. Add garlic; cook and stir until fragrant, 1 minute more.",
     "Add broth, cream, lemon zest and juice, rosemary, and crushed red pepper. Bring to a boil, about 2 minutes.",
     "Add spinach, in batches, stirring until wilted, about 1 minute.",
     "Stir in 1/4 cup Parmesan cheese and simmer until desired consistency, about 5 minutes.",
     "Return chicken to skillet. Sprinkle with remaining 1/4 cup Parmesan cheese.",
     "Bake in the preheated oven until chicken is cooked through and sauce is bubbling, 10 to 15 minutes. An instant read thermometer, inserted into the thickest part of chicken, should read 165 degrees F (74 degrees C).",
     "Serve garnished with lemon slices.",
     ],
    [
        "4, oz, chicken breast",
        "0.5, tsp, salt",
        "0.25, tsp, pepper",
        "2, tbsp, flour",
        "2, tbsp, olive oil",
        "1, unit, onion",
        "3, unit, garlic",
        "0.75, cup, chicken broth",
        "0.5, cup, heavy cream",
        "1, tsp, lemon zest",
        "3, tbsp, lemon juice",
        "1, tsp, rosemary",
        "0.25, tsp, red pepper",
        "2, unit, baby spinach",
        "0.5, cup, parmesan cheese",
    ]
]
recipe12 = [
    "The Original Marry Me Chicken",
    "",
    5,
    0,
    40,
    4,
    "d39f391b-0e9e-11f1-afc8-502e919fa289_marrymechicken.jpg",
    ["dinner"],
    ["Finely chop garlic and sundried tomatoes",
     "Arrange a rack in center of oven; preheat to 375°.",
     "In a large ovenproof skillet over medium-high heat, heat 1 Tbsp. oil.",
     "Generously season chicken with salt and black pepper and cook, turning halfway through, until golden brown, about 5 minutes per side.",
     "Transfer chicken to a plate.",
     "In same skillet over medium heat, heat remaining 2 Tbsp. oil.",
     "Stir in garlic, thyme, and red pepper flakes. Cook, stirring, until fragrant, about 1 minute.",
     "Stir in broth, tomatoes, cream, and Parmesan; season with salt.",
     "Bring to a simmer, then return chicken and any accumulated juices to skillet.",
     "Transfer skillet to oven. Bake chicken until cooked through and an instant-read thermometer inserted into thickest part registers 165°, 10 to 12 minutes.",
     "Arrange chicken on a platter. Spoon sauce over. Top with basil."
     ],
    [
        "3, tbsp, olive oil",
        "4, unit, chicken breast",
        "2, unit, garlic",
        "1, tbsp, thyme",
        "1, tsp, red pepper flakes",
        "0.75, cup, chicken broth",
        "0.5, cup, sundried-tomates",
        "0.5, cup, heavy cream",
        "0.25, cup, parmesan",
    ]
]
recipe13 = [
    "Chef John\'s Shrimp and Grits",
    "This classic Southern meal features the heat of jalapeño, cayenne, and Cajun seasoning. Absolutely delicious and very easy to execute.",
    4,
    0,
    55,
    3,
    "9e4844d0-11b9-11f1-9542-1ebf2a7aaad6_shrimp-grits.webp",
    ["dinner"],
    ["Gather the ingredients",
     "Cut the 4 strips of bacon into 1/4-inch pieces",
     "Mince jalapeno pepper, green onion, garlic, and chop parsley",
     "Cook bacon in a large skillet over medium-high heat, turning occasionally, until almost crisp, 5 to 7 minutes.",
     "Transfer bacon to a dish; reserve drippings in the skillet.",
     "Whisk 1/4 cup water, cream, lemon juice, and Worcestershire sauce together in a bowl.",
     "Combine 4 cups water, butter, and 1 teaspoon salt in a pot; bring to a boil. Whisk in grits; bring to a simmer, reduce heat to low, and cook until creamy, 20 to 25 minutes.",
     "Take the mixture off heat, and stir in cheddar cheese",
     "Season shrimp with Cajun seasoning, 1/2 teaspoon salt, black pepper, and a pinch of cayenne pepper in a large bowl.",
     "Heat bacon drippings in the skillet over high heat. Add shrimp; cook 1 minute.",
     "Flip shrimp; add jalapeño and cook until fragrant, about 30 seconds.",
     "Stir cream mixture, bacon, green onion, and garlic into shrimp mixture; cook and stir until shrimp cooked through, 3 to 4 minutes, adding water as necessary to thin sauce.",
     "Take off heat, and stir in parsley",
     "Ladle grits into a bowl; top with shrimp and sauce."
     ],
    [
        "4, unit, bacon",
        "4.25, cup, water",
        "2, tbsp, heavy cream",
        "2, tsp, lemon juice",
        "0.125, tsp, worcestershire sauce",
        "2, tbsp, unsalted butter",
        "1.5, tsp, salt",
        "1, cup, white grits",
        "0.5, cup, white cheddar cheese",
        "1, lb, shrimp",
        "0.5, tsp, cajun seasoning",
        "0.25, tsp, pepper",
        "1, tbsp, jalapeno pepper",
        "2, tbsp, green onion",
        "3, unit, garlic",
        "1, tbsp, parsley"
    ]
]
recipe14 = [
    "Chocolate Peanut Butter Protein Bars",
    "Chocolate peanut butter protein bars are easy to make in a small batch, and absolutely delicious. Using a good protein powder is the key. If there is a downside, it might be how hard it will be to only eat one.",
    4,
    0,
    40,
    3,
    "91e18a80-11b9-11f1-9542-1ebf2a7aaad6_Chocolate-Peanut-Butter-Protein-Bars.webp",
    ["dessert", "easy"],
    ["Line an 8 1/2x4 1/2-inch loaf pan with parchment paper, leaving overhang on all sides to make it easy to remove bars from the pan. Set aside.",
     "Place peanut butter, protein powder, maple syrup, vanilla and salt in a bowl and mix until well combined; press into the prepared pan. Set aside.",
     "Place chocolate chips and oil in a microwave safe bowl. Microwave for 30 seconds, stir. Repeat until chips are completely melted when stirred. Pour over bars, smooth chocolate. Refrigerate until set, about 30 minutes. Cut into 8 bars.",
     ],
    [
        "0.75, cup, peanut butter",
        "0.5, cup, protein powder",
        "2, tbsp, maple syrup",
        "1, tsp, vanilla extract",
        "0.125, tsp, salt",
        "0.5, cup, chocolate chips",
        "1, tsp, coconut oil",
    ]
]
recipe15 = [
    "Artichoke Dip Wonton Cups",
    "These artichoke dip wonton cups are a fun twist on the traditional spinach artichoke dip with tortilla chips. Served as individual bites, they're ideal for a party.",
    4,
    0,
    30,
    3,
    "81e670d2-11b9-11f1-9542-1ebf2a7aaad6_artichoke-dip-wonton-cups.webp",
    ["snack", "easy"],
    ["Preheat the oven to 350 degrees F (180 degrees C). Spray a standard 12-cup muffin tin with cooking spray.",
     "Line each muffin cup with a wonton wrapper. Press the center of the wrapper down into the cup, leaving the edges sticking up out of the cup. Spray each wrapper lightly with cooking spray.",
     "Bake cups in the preheated oven for 5 minutes, then remove from the oven."
     "Add spinach, artichoke hearts, mayonnaise, sour cream, cream cheese, Parmesan cheese, and garlic in a bowl until well incorporated. Divide mixture evenly between wonton cups.",
     "Return to the oven and bake until filling is heated through and edges of wrappers are golden brown, about 15 minutes."
     ],
    [
        "12, unit, wonton wrappers",
        "5, oz, spinach",
        "1, unit, artichoke hearts",
        "0.33, cup, mayonnaise",
        "0.25, cup, sour cream",
        "2, oz, cream cheese",
        "0.5, cup, parmesan cheese",
        "2, unit, garlic"
    ]
]
recipe16 = [
    "Easy Grilled Shrimp Fajitas",
    "Quick grilled shrimp fajitas with bell peppers, onions, and fajita seasoning served on warm tortillas",
    4,
    0,
    40,
    3,
    "98cbe5a2-11b9-11f1-9542-1ebf2a7aaad6_shrimp_fajitas.webp",
    [],
    [
        "Preheat an outdoor grill for medium-high heat and lightly oil the grate",
        "In a large bowl combine sliced red bell pepper, green bell pepper, onion, jalapeño, 2 teaspoons fajita seasoning, and olive oil; stir until evenly coated",
        "In a separate bowl add raw shrimp, remaining 1/2 teaspoon fajita seasoning, and lime juice; gently stir to coat",
        "Place the vegetable mixture in a grill basket and cook on the grill for about 10 minutes, stirring occasionally",
        "Add the shrimp to the grill basket with the vegetables and cook for about 5 more minutes until shrimp are opaque",
        "Remove the grill basket and place the tortillas on the grill to toast for about 2 minutes",
        "Divide the shrimp and vegetable filling between the warm tortillas and serve while hot",
    ],
    [
        "12, oz, shrimp",
        "1, unit, red bell pepper",
        "1, unit, green bell pepper",
        "1, unit, large onion",
        "1, unit, jalapeno pepper",
        "8, unit, flour tortillas",
        "2.5, tsp, fajita seasoning mix",
        "1, tsp, olive oil",
        "1, tbsp, lime juice",
    ]
]
recipe17 = [
    "Blueberry Chia Pudding with Almond Milk",
    "A light vegan chia pudding made with almond milk, fresh blueberries, and a touch of maple syrup and cinnamon. Great for breakfast or a healthy snack.",
    3,
    8,
    10,
    3,
    "8a70854e-11b9-11f1-9542-1ebf2a7aaad6_chia_pudding.webp",
    ["breakfast", "vegan", "gluten free", "dessert"],
    [
        "Combine almond milk, chia seeds, blueberries, maple syrup, vanilla extract, and cinnamon in a blender; blend until smooth.",
        "Pour into glasses or ramekins.",
        "Chill until set, about 8 hours or overnight.",
        "Serve chilled."
    ],
    [
        "2, cup, almond milk",
        "6, tbsp, chia seeds",
        "0.33, cup, fresh blueberries",
        "1, tbsp, maple syrup",
        "0.5, tsp, vanilla extract",
    ]
]
recipes = [recipe0, recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7, recipe8, recipe9, recipe10, recipe11, recipe12, recipe13, recipe14, recipe15, recipe16, recipe17]
for r in recipes:
    for i in r[9]:
        if i.split(", ")[2] not in ingredients:
            ingredients.append(i.split(", ")[2])

cookbooks = [
    ["Cooking Mama\'s Recipes", "Recipes from the Cooking Mama Franchise", 1, "9a462e80-1130-11f1-9a14-1ebf2a7aaad6_cooking-mama-cover.jpg", [0, 1, 2]],
    ["ChatGPT's Kitchen Creations", "A curated collection of comforting dinners, quick breakfasts, indulgent desserts, and flavorful vegetarian dishes designed for both beginners and experienced home cooks.", 2, "", [3, 4, 5, 6, 7, 8, 9, 10]],
    ["AllRecipe's Cookbook", "A collection of Allrecipe's best dishes", 3, "b4458f2c-11b9-11f1-9542-1ebf2a7aaad6_allrecipes.jpg", [11, 13, 14, 15, 16, 17]],
]
# ----------

script = '''from app import create_app, db
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

db.create_all()'''


# ----- Add Users -----
script += "\n# --- Add Users ---"
for i in range(len(users)):
    script += "\nu"
    script += str(i)
    script += " = User(\nfirst_name = \""
    script += users[i][0]
    script += "\", last_name = \""
    script += users[i][1]
    script += "\", username = \""
    script += users[i][2]
    script += "\", email = \""
    script += users[i][3]
    script += "\""
    if users[i][5]:
        script += ", is_certified=True"
    else:
        script += ", is_certified=False"
    script += ")\nu"
    script += str(i)
    script += ".set_password(\""
    script += users[i][4]
    script += "\")\ndb.session.add(u"
    script += str(i)
    script += ")\n\n"
script += "db.session.commit()\n"


# --- Add ingredients ---
script += "\n# --- Add Ingredients ---"
for i in range(len(ingredients)):
    script += "\ni"
    script += str(i)
    script += " = Ingredient(\nname = \""
    script += ingredients[i]
    script += "\")\ndb.session.add(i"
    script += str(i)
    script += ")\n\n"
script += "db.session.commit()\n"

# --- Add Tags ---
script += "\n# --- Add Tags ---"
for i in range(len(tags)):
    script += "\nt"
    script += str(i)
    script += " = Tag(\nname = \""
    script += tags[i]
    script += "\")\ndb.session.add(t"
    script += str(i)
    script += ")\n\n"
script += "db.session.commit()\n"

# --- Add Certifications ---
script += "\n# --- Add Certifications ---"
for i in range(len(certifications)):
    script += "\nc"
    script += str(i)
    script += " = Certification(\nname = \""
    script += certifications[i]
    script += "\")\ndb.session.add(c"
    script += str(i)
    script += ")\n\n"
script += "db.session.commit()\n"


# --- Add recipe ---
script += "\n# --- Add Recipes ---"
for i in range(len(recipes)):
    script += "\nr"
    script += str(i)
    script += " = Recipe(title = \""
    script += recipes[i][0]
    script += "\", description = \""
    script += recipes[i][1]
    script += "\", servingSize = "
    script += str(recipes[i][2])
    script += ", estimatedHrs = "
    script += str(recipes[i][3])
    script += ", estimatedMins = "
    script += str(recipes[i][4])
    script += ", is_draft=False, user_id=u"
    script += str(recipes[i][5])
    script += ".id)\nr"
    script += str(i)
    script += ".timestamp = datetime.now(timezone.utc)\n"
    if recipes[i][6] != "":
        script += "r"
        script += str(i)
        script += ".pictFile = \""
        script += recipes[i][6]
        script += "\"\n"
    script += "\ndb.session.add(r"
    script += str(i)
    script += ")"
    script += "\ndb.session.commit()"
    
    # recipe tags
    for t in recipes[i][7]:
        script += "\nr"
        script += str(i)
        script += ".tags.add(t"
        script += str(tags.index(t))
        script += ")"
    script += "\ndb.session.commit()"

    # recipe steps
    for j in range(len(recipes[i][8])):
        step = recipes[i][8][j]
        script += "\ns"
        script += str(i)
        script += str(j)
        script += " = RecipeStep(stepNum = "
        script += str(j+1)
        script += ", description = \""
        script += step
        script += "\""
        script += ", recipe_id = r"
        script += str(i)
        script += ".id)\ndb.session.add(s"
        script += str(i)
        script += str(j)
        script += ")"
    script += "\ndb.session.commit()"

    # recipe ingredients
    for j in range(len(recipes[i][9])):
        recipeIngredient = recipes[i][9][j].split(", ")
        script += "\nri"
        script += str(i)
        script += str(j)
        script += " = RecipeIngredientUse(recipe_id = r"
        script += str(i)
        script += ".id, ingredient_id = i"
        script += str(ingredients.index(recipeIngredient[2]))
        script += ".id, amount = "
        script += recipeIngredient[0]
        script += ", unit = \""
        script += recipeIngredient[1]
        script += "\")\ndb.session.add(ri"
        script += str(i)
        script += str(j)
        script += ")"
    script += "\ndb.session.commit()"

# --- Add cookbooks ---
for i in range(len(cookbooks)):
    script += "\nc"
    script += str(i)
    script += " = Cookbook(title = \""
    script += cookbooks[i][0]
    script += "\", description = \""
    script += cookbooks[i][1]
    script += "\", user_id = u"
    script += str(cookbooks[i][2])
    script += ".id"
    script += ")\ndb.session.add(c"
    script += str(i)
    script += ")"
    if cookbooks[i][3] != "":
        script += "\nc"
        script += str(i)
        script += ".pictFile = \""
        script += cookbooks[i][3]
        script += "\""
    for j in cookbooks[i][4]:
        script += "\nc"
        script += str(i)
        script += ".included_recipes.add(r"
        script += str(j)
        script += ")"
    script += "\ndb.session.commit()"


file = open("initialize_db_info.py", "w")
file.write(script)
file.close()