# Recipe App API Documentation
- [1. Introduction](#1-introduction)
- [2. Data Models](#2-data-models)
- [3. ]

## 1. Overview

## 2. Data Models
### Recipe
> Represents a full recipe stored in the application

| Field | Type | Description | Additional |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier | Primary key |
| `title` | String (200) | Recipe title | Required |
| `description` | String | Recipe description |
| `serving_size` | Integer | Number of servings |
| `active_time` | Integer | Active preparation & cooking time in minutes |
| `overall_time` | Integer | Total preparation, cooking, resting, etc. time in minutes |
| `timestamp` | Datetime | Recipe's last edit time | Required |
| `is_draft` | Boolean | Whether the recipe is a draft | Required |
| `to_make` | Boolean | Whether the recipe is on the user's to-make list |

### Ingredient
> Represents an ingredient that can be used in recipes with no quantities

| Field | Type | Description | Additional |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier | Primary key |
| `name` | String (200) | Ingredient name | Required, Must be unique |

### IngredientGroup
> Represents a group an ingredient can be a part of, such as shellfish or nuts, for dietary restrictions

| Field | Type | Description | Additional |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier | Primary key |
| `name` | String (100) | Name of the ingredient group | Required |
| `group_type` | String (30) | Name of the group type, such as "allergen" | Required |

### IngredientGroupMembership
> Links ingredients with ingredient groups in a many-to-many relationship

### RecipeIngredientUse
> A use of an ingredient in a recipe (i.e., keeping track of the quantity used)

| Field | Type | Description | Additional |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier | Primary key |
| `recipe_id` | Integer | ID of the recipe | Foreign key |
| `ingredient_id` | Integer | ID of the ingredient | Foreign key |
| `amount` | Decimal | Numeric amount of the ingredient used | Required |
| `unit` | String | Unit amount of the ingredient used (e.g., "cup" or "kg") | Required |

### IngredientCostEntry
| Field | Type | Description | Additional |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier | Primary key |
| `ingredient_id` | Integer | ID of the ingredient | Foreign key |
| `brand` | String (150) | Ingredients brand for additional cost information (e.g., a fancier or cheaper brand) |
| `additional_details` | String | Additional information, such as organic |
| `timestamp` | Datetime | When the cost entry was added | Required |
| `payment_unit` | String (100) | What the unit bought was, such as 1 box or 1 bottle | Required |
| `amount_unit` | String (100) | Another unit equivalent to `payment_unit`, such as 16 oz or 500 g |
| `cost_per_unit` | Decimal | Price paid for the payment unit/package | Required |
| `cooking_unit` | String | Unit typically used in cooking, such as a cup or gram. Can be the same unit as amount_used | Required |
| `cost_per_cooking_unit` | Decimal | Cost per 1 unit specified in `cooking_unit`, such as how much 1 cup costs | Required |

### RecipeStep
| Field | Type | Description | Additional |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Unique identifier | Primary key |
| `recipe_id` | Integer | ID of the recipe | Foreign key |
| `step_number` | Integer | This step's number in the directions | Required |
| `instruction` | String | This step's content | Required |
| `ingredient_use_id` | Integer | What ingredients are used in this step | Foreign key, optional |


## 3. API Routs
| Method | URL Path | Corresponding function | Short Description |
| :--- | :--- | :--- | :--- |
| GET | /api/recipes | `get_recipes` | Returns recipe data for all recipes that aren't drafts |
| POST | /api/recipes | `save_recipe` | Saves a recipe to the database, with draft status based on which button the user presses |
| GET | /api/recipes/<recipe_id>/view | `view_recipe` | Returns recipe data for the specified recipe id |

