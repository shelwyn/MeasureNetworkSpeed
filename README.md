# MeasureNetworkSpeed
Python script (with Selenium) to measure network speed (across multiple sites)

This script will do the following tasks
  - launch chrome
  - load https://www.linkedin.com/
  - login with credentials
  - load https://www.speedtest.net/
  - gather time spent on loading linkedin, loging into linkedin, scrape the download and upload speed from (speedtest.net) and save the data into an Azure-CosmosDb
  
Link to Cosmos DB tutorial: https://docs.microsoft.com/en-us/azure/cosmos-db/create-sql-api-python
  
Python packages required (Assuming you are on python3)
   - pip3 install azure-cosmos
   - pip3 install selenium
    
  
