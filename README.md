[![Sample Banner](views/Sample.png)][ss1]

# Data import from Excel to QBO
#### Sample App in Python that implements Connect to Quickbooks button and imports customer data from Excel to QBO company.

This sample app is meant to provide working example of how to make API calls to Quickbooks. Specifically, this sample application demonstrates the following:

- Implementing OAuth to connect an application to a customer's QuickBooks Online company for both OAuth1 and OAuth2.
- Creating a QB customer that are added from Excel file using Customer API.
- Gets company data using CompanyInfo API

Please note that while these examples work, features not called out above are not intended to be taken and used in production business applications. In other words, this is not a seed project to be taken cart blanche and deployed to your production environment. For example, certain concerns are not addressed at all in our samples (e.g. security, privacy, scalability). In our sample apps, we strive to strike a balance between clarity, maintainability, and performance where we can. However, clarity is ultimately the most important quality in a sample app.

## Requirements
1. Python 3.6
2. A [developer.intuit.com](https://developer.intuit.com/) account
3. An app on [developer.intuit.com](https://developer.intuit.com/) and the associated app keys:  
    - Client Id and Client Secret for OAuth2 apps; Configure the RedirectUri[http://localhost:5000/callback] in your app's Keys tab on the Intuit developer account, only Accounting scope needed  
    - Consumer key and Consumer secret for OAuth1 apps
4. This sample app uses several libraries listed in [requirements.txt](requirements.txt) which need to be installed including flask, flask_oauth, openpyxl, requests_oauthlib  

## First Time Instructions
1. Clone the GitHub repo to your computer
2. Install libraries mentioned above in Requirements 4.
3. Fill in your [config.py](config.py) file values by copying over from the keys section for your app

## Running the code
1. cd to the project directory
2. ```pip install -r requirements.txt```
3. Run the command: ```python app.py``` for MacOS/Linux 
4. open a browser and enter ```http://localhost:5000``` 

## High Level Project Overview

1. [app.py](app.py) module contains all routes for the Flask web app
2. [QBOService.py](QBOService.py) class creates a Customer in QBO and gets QBO company info

### Utility modules
3. [excel.py](utils/excel.py) module deals with importing data from [Leads.xlsx](Leads.xlsx) and editing it
4. [context.py](utils/context.py) class for request context object which has all tokens and realm required to make an API call
5. [APICallService.py](utils/APICallService.py) module has POST and GET methods for QBO API
6. [OAuth2Helper.py](utils/OAuth2Helper.py) module has the methos required for OAuth2 flow

#### Note: For other OAuth2 services like Refresh token, Revoke token, etc, refer to [this](https://github.com/IntuitDeveloper/OAuth2PythonSampleApp) app

[ss1]: https://help.developer.intuit.com/s/samplefeedback?cid=9010&repoName=SampleApp-QuickBooksV3API-Python
