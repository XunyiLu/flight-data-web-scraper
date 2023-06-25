# Flight Data Scraper and Database Storage

This project aims to scrape flight data from the "Global Flight Tracking Radar" website(https://flightadsb.variflight.com/) and store it in a MySQL database. It uses web scraping techniques with Selenium and BeautifulSoup libraries to extract required information and perform database operations using pymysql library. 



## Requisites

Before running the code, ensure you have the following prerequisites: 



+ Chrome Webdriver: Download the Chrome WebDriver from official website(https://chromedriver.chromium.org/downloads) and ensure the **'driver_path**' variable in the code points to the correct location of the Chrome WebDriver on your system. 
  + Remember the webdriver should match with your browser and the version of the browser. 

+ MySQL: Install MySQL on your system and obtain the username and password to access the database. 

+ Python Packages: Install the required Python packages using the following command



## Usage

1. Configuration: 
   + Update the 'driver_path' variable to in the code with the correct path to the Chrome WebDriver on your system
   + Modify the database host, user, password and database name in the 'DatabaseManager' initialization

2. Run the code



## Code Explanation

1. 'login_and_scrape_flight_data(db_manager)': This function performs as scraping process. It uses Selenium to simulate user actions and load the target webpage, then extracts the required flight data using BeautifulSoup. The data is parsed and stored in the MySQL database using 'db_manager'
2. 'parsed_data(html)': This function recerives the HTML source code and uses BS4 to extract the desired flight data. It returns a dictionary containg the parsed data. 
3. 'Databasemanager': This class manages the database operations such as creating the database, creating the tables, inserting queries and visualisation(which is not well implemented, but it's not our goal). 









