#Flipkart Scraper

I used django rest framework to create this project , used railways to host my postgres database.

- API that lets users signup and log in through JWT based authentication using email and password

- Api that takes a Flipkart url as payload, scrapes the below-given
fields, and saves them in Postgres with proper schema with user info. This works only if a user is logged in, else proper error message is shown.

- Checks if the URL corresponding to the logged-in user is already present in the DB, and return from the DB. If the URL is not present or does not belong to a logged-in user show a proper error message.


API Endpoints :- 

    register/ -  Registering a new user
    login/ - Logging (Generates a jwt token)
    token/refresh/ - refresh login token
    user/ - provide current user info 
    scrape/ - scrape data about a product using a product page url



If you want to test it , you can simply clone it ,and then run server and visit 'localhost/scraper/' to directly store the product data to the db
