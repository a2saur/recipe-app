## Digital Meal Planner + Recipe Book
### Project Origin
This project was originally developed in January - March 2026 as a project for WPI's software engineering course by Team REST. The team members were Zoya Ahmad, Sunny Kang, Patricia Oltra, and Alexa Saur.

------------------------
### Running the Application
- The application can be run with either of the following commands:
    ```
    python meal_planner.py
    ```
    ```
    flask run
    ```
- Tests can be run via the ```run_tests_coverage.sh``` shell script or via the following commands:
    <br>For just pytest
    ```
    python3 -m pytest -v test_routes.py
    ```
    For pytest coverage report and display
    ```
    coverage run -m pytest test_routes.py
    coverage report -m
    coverage html
    coverage xml
    ```
- To prepolate the database, run the ```re_initialize_db.sh``` shell script or the following commands:
    <br>*NOTE: if you don't use the shell script, be sure to remove the migrations folder and meal_planner database*
    <br>Recreate the database
    ```
    flask db init
    flask db migrate -m "recreated db"
    flask db upgrade
    ```
    Pre populate the app with data
    ```
    python3 make_initialize_db_info_script.py
    python3 initialize_db_info.py
    ```

------------------------
### Repository organization
- ```app```: Contains the code for the application, organized into modules and an init python script
- ```class-materials```: Contains materials used for the class, including initial documentation, group reports, and the AWS Deployment guide
- ```tests```: Contains tests to be run for bug checking
- ```setup-files```: Files/scripts used for initializing the database
- ```documents```: Documentation about the application