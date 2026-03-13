#!/bin/bash

python3 -m pytest -v test_routes.py
coverage run -m pytest test_routes.py
coverage report -m
coverage html
coverage xml