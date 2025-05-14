# miRNA Gene Target Search (BF768 Spring 2025 - Homework 3)

## Overview
This Flask-based web application allows users to search for genes that are co-targeted by two miRNAs based on a specified maximum targeting score. It interacts with a MariaDB database to return a list of shared target genes meeting the user-specified score threshold.


## Database Credentials
To protect sensitive information, the database connection string (host, username, password) has been removed from nicolaspetrunich_Search.py.

## Repo Structure
├── nicolaspetrunich_Search.py: Flask app that handles routing, form input, database querying <br>
└── templates/nicolaspetrunich_Search.html: HTML template rendered with form and result output

## Features
- Input form for two miRNA names and a dropdown to select a maximum targeting score.
- Returns genes targeted by both miRNAs with scores ≤ selected threshold.
- Displays results in a sortable HTML table.
- Input validation and user-friendly error messages.
- Fully parameterized SQL queries for security.

## Example Inputs
- Suggested miRNAs: hsa-let-7a and hsa-miR-1294
- Score Dropdown: Score ≤ -0.1 to ≤ -0.7

## Hosting Status
This application is not currently deployed or hosted on any live server, and therefore cannot be accessed through a browser at this time.
