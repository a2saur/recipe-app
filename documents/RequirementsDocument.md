# Software Requirements and Use Cases

## Digital Meal Planner + Recipe Book
--------
Prepared by:

* `<Sunny Kang>`,`<WPI - RBE & Physics>`
* `<Patricia Oltra>`,`<WPI - CS Major>`
* `<Zoya Ahmad>`,`<WPI - Computer Science>`
* `<Alexa Saur>`,`<WPI - CS & RBE>`

---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name=revision-history> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2026-1-30 |Initial draft | 1.0        |
|Revision 2 |2026-2-5 |Updated draft | 2.0        |
|      |      |         |         |

----
# 1. Introduction

This app is a recipe organizer for budgeting and meal planning, where users can publish and view published recipes. The two main interfaces are for **general users** and **certified users**, the latter being professional chefs who will benefit from the chance to advertise their work and/or business.

----
# 2. Requirements Specification

## Functional Requirements:
* After a user registers, they will be redirected to the login page.
* When a user logs in it brings them to the main page.
When a user is logged in, their username should be displayed on the navigation bar
* When a user creates an account, it should create a profile for them that saves their information.
* When a user likes a recipe it should add it to their profile under likes.
* When a user creates a recipe it should post it on the main page if they filled out all of the information.
* After a general user creates an account they should have the option to become a certified user in their profile page.
* When a general user requests to become a certified user they should fill out a form that requires them to fill out their certification and an email verification.
* Recipes posted by a certified user will display a certification mark on the main page.
* When a user uses the filter option, the displayed posts should contain the selected characteristics
* When a user uses the sort option, the displayed posts should be sorted according to the selected sorting method.
* When a user filters or sorts posts in the recipe page, they should be shown what filters/sort options are in use.
* A user should be able to select a post in the main page, and view all of its details.
* Users should be able to confirm the success or failure of an action in the page they see after performing said action.
* When a certified user creates or edits a cookbook, the updated cookbook should show up in their profile page
* When a certified user deletes a cookbook, it should no longer show in their profile page

## Non-functional Requirements:<br>
* The system should provide a web-based user interface accessible through a web browser, such as chrome
* The system should response to the user actions within 2 seconds 
* The system should store all data and ensure basic security, such as password hashing
* The system should be easy to use by first-time users without training.

## 2.1 Customer, Users, and Stakeholders

## Customer:
Any individuals that are interested in discovering, saving and cooking recipes from the ingredients that are available.

## Users:
**General Users:** Users will be able to post recipes, pick recipes they want to make, have a list of items they already have, and have a running grocery list based on the recipes they want to make and what they already have. The grocery list and recipes will include an estimated price, and the system will recommend recipes based on the ingredients users already have.
<br><br>
**Certified Users:** Certified Users will be professional chefs who, in addition to the general user functionalities, will be able to create digital cookbooks with a selection of their recipes. Their published recipes will be shown as certified, and they will have the option to link their business to the recipes/their profiles.<br>

## Stakeholders:
* Users who actually use the system to look for recipes
* Developers (us) who are responsible for implementing, testing the system

----
## 2.2 User Stories
**General Account Management - Iteration 1**
* As a general or certified user, I want to log in and out of my profile, so that I can view all of my account information and saved information every time I view the website.
* As a general or certified user, I want to register a profile so that all of my information is saved for the next time I log into my account.
* As a general or certified user, I want to edit my profile information so that I can update it when necessary.

**Browsing/Searching Recipes(Main Page) - Iteration 1**
* As a general or certified user, I want to view a list of recommended recipes that contain many ingredients on my ingredient list so that I can make use of what I already have.
* As a general user I want to see recipes posted by certified users because they are more trustworthy than those posted by general users.
* As a general or certified user, I want to view recipes posted by other users so that I can decide if I want to make them
* As a general or certified user, I want to sort posts based on likes, certified users, and date posted.
* As a general or certified user, I want to filter posts based on likes, certified users, date posted and tags.

**Creating and Managing Recipe Posts (Create Recipe/Edit Recipes) - Iteration 1**
* As a general or certified user, I want to create and post my own recipes so that I and other users can view and make them
* As a general or certified user, I want to edit recipes that I’ve posted so that I can update information
* As a general or certified user, I want to delete recipes that I’ve posted so that I can remove recipe posts I don’t want up anymore.
* As a general or certified user, I want to add descriptive tags to my recipes so that I can specify the type of recipe and reach the right audience.

**Certified user profile management - Iteration 2**
* As a certified user, I want to activate my certification status so that I can have access to more features and so my recipes have a certified mark to get boosted more.
* As a certified user, I want to add my business’ name and website to my profile so that I can advertise it.

**Creating and Managing Cookbooks (Accessed through Profile Page or Recipe within Cookbook) - Iteration 2**
* As a certified user, I want to create cookbooks with my posted recipes so that other users can view my selections.
* As a certified user, I want to edit my cookbooks so that I can change out of date information
* As a certified user, I want to delete my cookbooks so that I can remove cookbooks that I don’t want up
* As a general or certified user, I want to view recipes in a cookbook so that I can see recipes in a collection I like
* As a general or certified user, I want to access a cookbook that contains the recipe I’m interested in so that I can see similar recipes I might also like

**Viewing my saved recipes (Saved Recipes) - Iteration 3**<br>
* As a general or certified user, I want to save recipes to my profile so that I can choose to make them later.
* As a general or certified user, I want to remove recipes from my saved recipes in case I don’t want to make them anymore.
* As a general or certified user, I want the option to add ingredients automatically to my grocery list when I add a recipe to my saved list.

**Viewing Ingredient and Grocery List - Iteration 3**
* As a general or certified user, I want to edit my current ingredient lists so that I can get better recipe recommendations
* As a general or certified user, I want to view my grocery list based on what recipes I’m planning on making so that I know what to get


----
## 2.3 Use Cases

**Certified user profile management**

| Use case # 1      |   |
| ------------------ |--|
| Name              | Certified User Profile Management  |
| Participating actor  | Certified Users  |
| Entry condition(s)     | Selecting to edit your profile  |
| Exit condition(s)           | Saving your profile  |
| Flow of events | <ol><li> User selects to edit their profile. </li><li>System responds by opening up the edit profile page. </li><li>User selects the option to become certified. </li><li>System responds by bringing the user to the verification page. </li><li>User selects the certification they have from a preloaded list, then presses enter.</li><li>System responds by sending a verification code to the user’s given email address. </li><li>User enters the given verification code. </li><li>System verifies the code then proceeds with the certification. </li><li>User returns to page and saves profile. |</li><ol>
| Alternative flow of events    | In step 5 the user must select a certification to become a certified user. In step 3 the user can choose to cancel the certification process. In step 7 if the user enters the incorrect verification code the system prompts the user to enter it again. |
| Iteration #         | 1 |

**Recipe Searching/Browsing (Main Page)**
| Use case #1      |   |
| ------------------ |--|
| Name              | View a Recipe |
| Participating actor  | All  |
| Entry condition(s)     | Being Logged In  |
| Exit condition(s)           | User has viewed a selected recipe  |
| Flow of events | <ol><li> The User Selects the MIndex/Recipes Page button</li><li> The Software responds by redirecting to the Recipe Page, and displaying all existing posts in a scrollable page (not including the current user’s posts). These posts will be sorted by relevance (compatibility with user’s ingredient list).</li><li> The User selects the view button on the card of a recipe.</li><li> The Software responds by redirecting to the post’s ‘View Post’ page, where all details of the selected Recipe are shown </li></ol>|
| Alternative flow of events    | After Step 4, the user may choose to click the Back Button, in which case the software will respond by redirecting to the Index/Recipes Page   |
| Iteration #         | 1  |

| Use case #3      |   |
| ------------------ |--|
| Name              | Filter and Sort posts |
| Participating actor  | All  |
| Entry condition(s)     | Being Logged in, and In Main Page/Recipes Page  |
| Exit condition(s)           | The Desired Filter (if any) is in use, and the recipes are sorted as desired  |
| Flow of events | <ol><li>The User selects The first Drop-down next to the filter button.</li><li>The Software responds by showing all possible features the user can filter for: likes count, certified, date posted and tags</li><li>The User selects Tags</li><li>The Software responds by adding a drop-down next to the original drop-down.</li><li>The User Selects the new drop-down.</li><li>The software responds by showing a (multiple)selectable list of all tags in the database</li><li>The user chooses one tag Awesome</li><li>The user clicks the Filter Button</li><li>The System responds by applying the filter and displaying only posts that contain the tag Awesome</li><li> The User clicks the drop-down next to the sort button.</li><li> The Software responds by displaying all possible features the user can choose to sort by: likes, certified, date posted.</li><li> The User then selects like.</li><li> The User selects the Sort button</li><li> The Software responds by displaying the posts (Still maintaining the previous filter) sorted by likes (desc). </li></ol> |
| Alternative flow of events    | <ol><li>In Step 1, the user may choose to do the action in step 10 first, in which case, steps 10-14 will be performed before step 1, in which case the sorting will be performed first, and the filtering will be performed maintaining the sorting choice.</li><li>The User may only perform steps 1-8, in which case no sorting will be performed.</li><li>The User may only perform steps 10-14, in which sorting will be performed without any filters.</li><li>In step 3, the user may select likes, in which case the software will respond by adding an input box next to the drop-down. The User will input a number, and the system will respond by filtering and displaying only posts with equal or higher like count.</li><li>In step 3, the user may select certified, in which case skip to step 8, and instead of step 9, the software will display only certified posts.</li><li>In step 3, the user may select date, in which case a drop-down will be displayed, the user will click on it, and the system will show a list of time frames (today, this week, this month, last 6 month, last year). Proceed with step 8, and instead of step 9, the software will display recipes posted within the selected time frame.</li><li>In step 9, if there are no posts that fulfill the filter requirements, the No Posts will be shown instead of the list of posts.</li><li>In step 11, the user may select any of the other options, in which case, in step 14, posts will be sorted as follows: From most recent to oldest for date and Certified users first and non-certified after for certified.</li> |
| Iteration #         | 2  |


**Viewing saved recipes (Saved Recipes)**
| Use case # 5      |   |
| ------------------ |--|
| Name              | Save favorite recipes  |
| Participating actor  | All  |
| Entry condition(s)     | User is on the recipe page  |
| Exit condition(s)           | Recipe is saved on the user’s saved recipe page  |
| Flow of events | 1. The user clicks the ‘save to my recipes’ button.
2. The page prompts the user if they want to add the list of ingredients from the recipe to their grocery list. 
3. The user clicks ‘Yes’.
4. The system adds the ingredients to the user’s grocery list and adds the recipe to the user’s saved recipes and reloads to the main page.  |
| Alternative flow of events    | 1. In step 3, the user may click ‘No’, in which case the system proceeds to step 4 without saving adding the ingredients to the grocery list.   |
| Iteration #         | 3  |

| Use case # 6      |   |
| ------------------ |--|
| Name              | Remove saved recipes  |
| Participating actor  | All  |
| Entry condition(s)     | User is on recipe page which they have saved  |
| Exit condition(s)           | Recipe is removed from the user’s saved recipe page  |
| Flow of events | <ol><li>The user clicks the ‘remove from my saved recipes’ button.</li><li>The page prompts the user if they want to remove the list of ingredients from the recipe from their grocery list. </li><li>The user clicks ‘Yes’.</li><li>The system removes the ingredients from the user’s grocery list and removes the recipe from the user’s saved recipes and reloads to their saved recipes page.</li>  |
| Alternative flow of events    | <ol><li> In step 3, the user may click ‘No’, in which case the system proceeds to step 4 without saving removing the ingredients from the grocery list. </li><li> In step 4, if the ingredients already don’t exist in the grocery list, the system proceeds to step 4 without changing the grocery list and flashes a message that says ingredients already don’t exist in the grocery list. </li> |
| Iteration #         | 3  |

**Viewing Ingredient and Grocery List**

| Use case # 7      |   |
| ------------------ |--|
| Name              | Edit ingredient list  |
| Participating actor  | All  |
| Entry condition(s)     | User is on the edit profile page  |
| Exit condition(s)           | List of current ingredients is updated   |
| Flow of events | <ol><li> The user fills out the current ingredients text box with a list of updated ingredients, separated by commas. </li><li> The user clicks the edit profile button once they are done. </li><li> If the submission is validated, the system reloads to the view profile page where the current ingredient list is updated with the new user’s input. </li></ol> |
| Alternative flow of events    | <ol><li> In step 3, if the submission fails due to incorrect formatting of the ingredient list input (special characters used other than commas), it flashes an error message to the user and stays on the edit profile page. </li></ol>  |
| Iteration #         | 3  |

| Use case # 8      |   |
| ------------------ |--|
| Name              | view my grocery list  |
| Participating actor  | All  |
| Entry condition(s)     | User is on any other than the ingredient list page  |
| Exit condition(s)           | User is on the ingredient list page  |
| Flow of events | <ol><li>The user selects the ingredient list button on the navigation bar.</li><li>The system responds by loading the ingredient list page.</li><li>The system displays the list of grocery items (list of items they don’t have) and list of ingredients they already have.</li>  |
| Alternative flow of events    | <ol><li> In step 3, if there are no items in the grocery list or the ingredients list, it displays no items under each list.  </li></ol>|
| Iteration #         | 3  |

**Creating and Managing Recipe Posts (Create Recipe/Edit Recipes)**

| Use case # 9      |   |
| ------------------ |--|
| Name              | Creating and Managing Recipe Posts  |
| Participating actor  | General and Certified Users |
| Entry condition(s)     | Pressing the button to Create a Recipe  |
| Exit condition(s)           | Saving the Recipe  |
| Flow of events | <ol><li>User selects the option to create a recipe. </li><li>System responds by opening the form to create a recipe. Prompting the user to fill out the desired information. </li><li>User fills out the title, serving size, description, length of time to make recipe, ingredients needed to make the recipe, and the steps to make the recipe. </li><li>User submits the the form. </li><li>System verifies that all of the information is filled out and posts the recipe to the main page. </li><li>System saves the recipe to the user’s profile.</li> |
| Alternative flow of events    | In step 6, the user can view their posted recipes on their profile, if they want to edit a recipe there is an option to edit the recipe or delete it. The user can press the edit button to bring them back to the create recipe page where they can make any changes. <br>In step 6, when the system is posting the recipe it will calculate the estimated cost of ingredients. 
|
| Iteration #         | 1  |


**Creating and Managing Cookbooks (Accessed through Profile Page or Recipe within Cookbook)**

| Use case # 10      |   |
| ------------------ |--|
| Name              | Creating a cookbook  |
| Participating actor  | Certified users  |
| Entry condition(s)     | User is on their profile page  |
| Exit condition(s)           | The cookbook has been successfully created  |
| Flow of events | <ol><li>The user hits the create cookbook button</li><li>The system prompts the user to enter the cookbook title, description, and selection of recipes that will be in it</li><li>The user fills out the information and hits the create button</li><li>The system saves the cookbook and notifies the user that it has been created</li><ol> |
| Alternative flow of events    | <ol><li>In step 3, if the user doesn’t fill out all the information, the user will be notified with the errors, and the flow of events will go back to step 2</li><li>In step 3, if the user doesn’t want to create a cookbook, the user can close out and end the flow of events without creating a cookbook</li><ol> |
| Iteration #         | 2  |

| Use case # 11      |   |
| ------------------ |--|
| Name              | Editing a cookbook  |
| Participating actor  | Certified users  |
| Entry condition(s)     | User is on the cookbook page of a cookbook they created |
| Exit condition(s)           | The user saves their changes  |
| Flow of events | <ol><li>The user hits the edit button on their cookbook page</li><li>The system prompts the user to optionally enter the new cookbook title, description, and selection of recipes</li><li>The user fills out the information and hits the save button</li><li>The system updates the cookbook and notifies the user that their changes have been saved</li><ol> |
| Alternative flow of events    | <ol><li>In step 3, if the user doesn’t want to edit their cookbook, the user can close out and end the flow of events without saving their changes</li><ol>  |
| Iteration #         | 2  |

| Use case # 12      |   |
| ------------------ |--|
| Name              | Deleting a cookbook  |
| Participating actor  | Certified users  |
| Entry condition(s)     | User is on the cookbook page of a cookbook they created  |
| Exit condition(s)           | The cookbook has been deleted |
| Flow of events | <ol><li>The user hits the delete button on their cookbook page</li><li>The system prompts the user for a confirmation that they want to delete the cookbook</li><li>The user hits the confirmation</li><li>The system deletes the cookbook and notifies the user that their cookbook has been deleted</li><ol>  |
| Alternative flow of events    | <ol><li>In step 3, if the user doesn’t want to delete their cookbook, the user can select the cancel and end the flow of events without the cookbook being deleted</li><ol>  |
| Iteration #         | 2  |

----
# 3. User Interface
**Main Page**
<kbd>
      <img src=images/main.png  border=2>
</kbd>

**Registration**
<kbd>
      <br>General user registration
      <img src=images/user-registration.png  border=2>
      Certified user registration
      <img src=images/certified-user-registration.png  border=2>
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
      <br>Certified user, showing cookbooks
      <img src=images/pfp-certified-cookbooks.png  border=2>
      Certified user, showing posts
      <img src=images/pfp-certified-posts.png  border=2>
      General user, showing saved posts
      <img src=images/pfp-general-saved.png  border=2>
</kbd>

**View Post**
<kbd>
      <br>General User's Post
      <img src=images/view-post-certified.png  border=2>
      Certified User's Post
      <img src=images/view-post-general.png  border=2>
</kbd>
  
----
# 4. Product Backlog

https://github.com/WPI-CS3733-2026C/team-teamrest/issues

----
# 5. References

