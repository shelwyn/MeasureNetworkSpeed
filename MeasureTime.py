from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import azure.cosmos.cosmos_client as cosmos_client
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.add_experimental_option("detach", True)

#options.add_argument("--window-position=0,0")
#options.add_argument("--headless")

driver = webdriver.Chrome("C:\sel\chromedriver", options=options) # Path where chrome driver is located
start = millis = int(round(time.time() * 1000))
#LOAD linkedin
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
end = millis = int(round(time.time() * 1000))
total_load_ln = end-start
print('time taken to load Linkedin: ' ,total_load_ln/1000)

#LOGIN TO linkedin
driver.find_element_by_id('username').send_keys('yourId@email.com') # email id used to login to linkedin
driver.find_element_by_id('password').send_keys('yourPassword') # password used to login to linkedin
start = millis = int(round(time.time() * 1000))
driver.find_element_by_class_name('btn__primary--large').click()
end = millis = int(round(time.time() * 1000))
total_login_ln = end-start
print('time taken to login Linkedin: ' ,total_login_ln/1000)

#Delay for loading another website
time.sleep(5)

#Load speedtest from Ookla
driver.get('https://www.speedtest.net/')
driver.find_element_by_class_name('start-text').click()
#Delay to let the website run pings to calculate download and upload speed
time.sleep(40)
downloadSpeed=driver.find_element_by_class_name('download-speed').text
uploadSpeed=driver.find_element_by_class_name('upload-speed').text
print("Download speed: ", downloadSpeed)
print("Upload speed:" ,uploadSpeed)

#Upload details to Cosmos
config = {
   'ENDPOINT': 'https://YOUR-AZURE-COSMOS_DB-ENDPOINT:443/',
    'PRIMARYKEY': 'YOUR AZURE COSMOS DB PRIMARY KEY',
    'DATABASE': 'YOUR COSMOS DB NAME',
    'CONTAINER': 'YOUR COSMOS DB CONTAINER NAME'
}
client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']}) # Initialize the Cosmos client
database_link = 'dbs/' + config['DATABASE']
db = client.ReadDatabase(database_link)
collection_link = database_link + '/colls/{0}'.format(config['CONTAINER'])
collection = client.ReadContainer(collection_link)
item1 = client.CreateItem(collection['_self'], {
    'Time taken to load Linkedin:': total_load_ln,
    'Time taken to login to Linkedin': total_login_ln,
    'Ookla download speed': downloadSpeed,
    'Ookla upload speed': uploadSpeed,
    'Data Added at': str(datetime.now())
}
)
#Exit
driver.quit()
