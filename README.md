# Basic data import from Excel to QBO
#### Sample App in Python that implements Connect to Quickbooks button and imports customer data from Excel to QBO company

This sample app is meant to provide working example of how to make API calls to Quickbooks. Specifically, this sample application demonstrates the following:

- Implementing OAuth to connect an application to a customer's QuickBooks Online company.
- Creating a QB customer with minimal fields that are added from Excel file.

Please note that while these examples work, features not called out above are not intended to be taken and used in production business applications. In other words, this is not a seed project to be taken cart blanche and deployed to your production environment.

For example, certain concerns are not addressed at all in our samples (e.g. security, privacy, scalability). In our sample apps, we strive to strike a balance between clarity, maintainability, and performance where we can. However, clarity is ultimately the most important quality in a sample app.

Therefore there are certain instances where we might forgo a more complicated implementation (e.g. caching a frequently used value, robust error handling, more generic domain model structure) in favor of code that is easier to read. In that light, we welcome any feedback that makes our samples apps easier to learn from.

Note: This app has been developed and tested for MacOS Sierra 10.12

## Requirements
1. Python 2.7
2. A [developer.intuit.com](https://developer.intuit.com/) account
3. An app on [developer.intuit.com](https://developer.intuit.com/) and the associated app token, consumer key, and consumer secret
4. This sample app uses several libraries which need to be installed including flask, flask_oauth, ConfigParser, openpyxl, requests_oauthlib  

## First Time Instructions
1. Clone the GitHub repo to your computer
2. Install libraries mentioned above in Requirements 4.
3. Fill in your [config.ini](config.ini) file values (consumer key and consumer secret) by copying over from the keys section for your app

## Running the code
1. cd to the project directory
2. Run the command: ```python app.py``` for MacOS/Linux 
3. open a browser and enter ```http://localhost:5000``` 

## High Level Project Overview

1. [app.py](app.py) module works as the view component for the Flask web app
2. [Customer.py](Customer.py) class creates a Customer object with minimum fields.
3. [qb.py](qb.py) modules has methods such as adding customer in Quickbooks Online, handling response, etc.

##### Utility modules
4. [excel.py](utils/excel.py) module deals with importing data from [Leads.xlsx](Leads.xlsx) and editing it
5. [configRead.py](utils/configRead.py) module deals with reading from config file
6. [context.py](utils/context.py) class for request context object which has all tokens and realm required to make an API call
7. [requestMethods.py](utils/requestMethods.py) module has post method for HTTP requests
