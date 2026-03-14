# Project Design Document

## Table of Contents

- [1. Introduction](#1-introduction)  
- [2. Software Design](#2-software-design)  
  - [2.1 Database Model](#21-model)  
  - [2.2 Modules and Interfaces](#22-modules-and-interfaces)  
  - [2.2.1 Overview](#221-overview)  
  - [2.2.2 Interfaces](#222-interfaces)  
  - [2.3 User Interface Design](#23-view-and-user-interface-design)  
- [3. References](#3-references)  
- [Appendix: Grading Rubric](#appendix-grading-rubric)

### Document Revision History

| Name | Date | Changes | Version |
| :---- | :---- | :---- | :---- |
| Revision 1 | 2026-2-10 | Initial draft | 0.1 |
| Revision 2 | 2026-2-12 | Updated diagrams | 0.1 |
| Final Draft | 2026-2-20 | Changed to final draft | 1.0 |
| New Document | 2026-3-13 | Updated document to be concurrent with the class final project and ready for additional personal work | 2.0 |

# 1. Introduction

The purpose of this document is to describe the high-level software design for the Meal Planner web application. It outlines the overall architecture, database model, and major software modules that support the system.

# 2. Software Design

## 2.1 Database Model

**User:** Stores user account information, including first and last name, username, and password hash. Stores their written recipes, saved recipes and current ingredients as relationships.

**Recipe:** Stores recipe information, including the user who posted it, the date posted (or updated), the title, a brief description, steps, serving size, estimated time to complete, its tags, and ingredients used. Additionally keeps track of what users have saved the recipe. It contains an attribute is_draft that tracks whether the recipe is a draft to be completed and posted later.

**Cookbook:** Stores cookbook information, including the user who created it, the title, the description, and the recipes included in it.

**Ingredient:** Stores the name and id of an ingredient to be used for a recipe or ingredient list

**Tag:** Stores the name and id of a tag to be used for tagging and filtering recipes

**RecipeIngredientUse:** Stores an instance of an ingredient being used in a recipe, including the recipe and ingredient ids as well as the amount with units of the ingredient.

**UserIngredientListUse:** Stores an instance of an ingredient being used in a user’s ingredient list (ie ingredients the user currently has), including the user and ingredient ids as well as the amount with units of the ingredient.

**UserGroceryListUse:** Stores an instance of an ingredient being used in a user’s grocery list (ie the ingredients the user needs to get), including the user and ingredient ids as well as the amount with units of the ingredient.

<kbd>  
      <img src=images/uml_diagram.png  border=2>  
</kbd>

## 2.2 Modules and Interfaces

### 2.2.1 Overview

<kbd>  
      <img src=images/uml_module_diagram.png  border=2>  
</kbd>

### 2.2.2 Interfaces

#### 2.2.2.1 main routes

|  | Methods | URL Path | Description |
| :---- | :---- | :---- | :---- |
| 1. | GET, POST | /index | Displays the main page with a list of recipe posts or cookbooks (depending on the user's choice). Includes a filter and sort feature.   |

#### 2.2.2.2 user routes

|  | Methods | URL Path | Description |
| :---- | :---- | :---- | :---- |
| 1. | GET, POST | /user/profile | Displays the user profile and information |
| 2. | GET | /user/<user_id>/viewprofile | Displays another user's profile and information |
| 3. | GET, POST | /user/profile/edit | Renders an edit form to edit profile information |
| 6. | POST | /user/recipe/<recipe_id>/saverecipe | Adds a recipe to a user’s saved list, adds selected ingredients from the recipe to the user's grocery list |
| 7.  | POST | /user/<recipe_id>/removerecipe | Removes the recipe from the user’s saved recipes |
| 8. | GET, POST | /user/ingredients | Renders the page with a list of current ingredients + grocery list |
| 9. | POST | /user/grocery/move-or-delete | Allows the user to move items from the grocery list to their own ingredient list. Also allows the user to delete ingredients from the grocery list. |
| 10. | POST | /user/ingredient/delete | Allows the user to delete ingredients from the user’s current ingredient list. |
| 12. | GET | /user/<user_id>/viewprofile | Shows another user’s profile with information like saved posts and email hidden. |

#### 2.2.2.3 recipe routes

|  | Methods | URL Path | Description |
| :---- | :---- | :---- | :---- |
| 1. | GET, POST | /recipe/create | Redirects to a recipe draft, if there is no recipe draft creates a new one |
| 2. | GET, POST | /recipe/<recipe_id>/view | Renders the view recipe page  |
| 3. | GET, POST | /recipe/<recipe_id>/edit | Renders an edit form similar to the create recipe form  |
| 4. | POST | /recipe/<recipe_id>/delete | Deletes a recipe from the database |

#### 

#### 2.2.2.4 cookbook routes

#### 

|  | Methods | URL Path | Description |
| :---- | :---- | :---- | :---- |
| 1. | GET, POST | /cookbook/create | Renders a create form for creating a cookbook |
| 2. | GET | /cookbook/<cookbook_id>/view | Display the cookbook basic information and recipes |
| 3. | GET, POST | /cookbook/<cookbook_id>/edit | Renders an edit form to edit cookbook information |
| 4. | POST | /cookbook/<cookbook_id>/delete | Deletes a cookbook from the database |

#### 2.2.2.5 auth routes

|  | Methods | URL Path | Description |
| :---- | :---- | :---- | :---- |
| 1. | GET, POST | /user/register | Renders the register page, which contains form RegistrationForm. If the form is successful, registers user and redirects to login. |
| 2. | GET, POST | /user/login | If the user is not logged in, renders the login.html page using a LoginForm. If the user is already logged in, it redirects to the main page |
| 3. | GET | /user/logout | Logs out the user and redirects to the login page |

### 2.3 User Interface Design

**Main Page**  
<kbd>  
      <img src=images/main.png  border=2>  
</kbd>

**Registration**  
<kbd>  
      <br>General user registration  
      <img src=images/user-registration.png  border=2>  
</kbd>

**Creating + Editing Recipes/Cookbooks**  
<kbd>  
      <img src=images/create-edit-recipe.png  border=2>  
      <img src=images/create-edit-cookbook.png  border=2>  
</kbd>

**Ingredients**  
<kbd>  
      <img src=images/ingredients.png  border=2>  
</kbd>

**Profile Pages**  
<kbd> 
      General user, showing saved posts  
      <img src=images/pfp-general-saved.png  border=2>  
</kbd>

**View Post**  
<kbd>  
      <br>General User's Post  
      <img src=images/view-post-certified.png  border=2> 
</kbd>

# 3. References
