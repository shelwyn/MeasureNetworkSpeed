from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import requests
import random
import string
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import azure.cosmos.cosmos_client as cosmos_client

class organisation: 
    start_time=0
    end_time=0
    time_to_get_new_details = 0
    time_to_load_ehub=0
    time_to_login=0
    time_to_add_emp=0
    time_to_add_payroll=0
    time_to_generate_pdf=0
    def add_new_emp():

        organisation.start_time = int(round(time.time() * 1000))
        response = requests.get("https://randomuser.me/api/?results=1").json()
        gender=response['results'][0]['gender']
        firstname=response['results'][0]['name']['first']
        lastname=response['results'][0]['name']['last']
        city=response['results'][0]['location']['city']
        state=response['results'][0]['location']['state']
        country=response['results'][0]['location']['country']
        email=response['results'][0]['email']
        organisation.end_time = int(round(time.time() * 1000))
        organisation.time_to_get_new_details = organisation.end_time - organisation.start_time
        organisation.time_to_get_new_details = organisation.time_to_get_new_details / 1000

        letters = string.ascii_lowercase
        uid=''.join(random.choice(letters) for i in range(10))
        usertype=random.choice([1, 0])
        designation=random.choice(['Analyst', 'Engineer', 'Developer', 'Administrator'])
        department=random.choice(['PAL/BEV', 'PAL/BIL', 'PAL/SEC'])
        salary=random.choice([5000, 6000,7000,8000])
        options = Options()
        options.add_experimental_option("detach", True)
        #options.add_argument("--window-position=0,0")
        #options.add_argument("--headless")
        driver = webdriver.Chrome("C:\sel\chromedriver", options=options)
        #LOAD bluerabbit
        organisation.start_time = int(round(time.time() * 1000))
        driver.get('http://bluerabbit.me/ehub/')
        organisation.end_time = int(round(time.time() * 1000))
        organisation.time_to_load_ehub = organisation.end_time - organisation.start_time
        organisation.time_to_load_ehub = organisation.time_to_load_ehub / 1000

        organisation.start_time = int(round(time.time() * 1000))
        driver.find_element_by_id('userid').send_keys('admin')
        driver.find_element_by_id('pass').send_keys('1981')
        driver.find_element_by_id('submit').click()
        organisation.end_time = int(round(time.time() * 1000))
        organisation.time_to_login = organisation.end_time - organisation.start_time
        organisation.time_to_login = organisation.time_to_login / 1000

        time.sleep(2)
        organisation.start_time = int(round(time.time() * 1000))
        driver.find_element_by_id('firstname').send_keys(firstname)
        driver.find_element_by_id('lastname').send_keys(lastname)
        driver.find_element_by_id('gender').send_keys(gender)
        driver.find_element_by_id('city').send_keys(city)
        driver.find_element_by_id('state').send_keys(state)
        driver.find_element_by_id('country').send_keys(country)
        driver.find_element_by_id('email').send_keys(email)
        driver.find_element_by_id('uid').send_keys(uid)
        driver.find_element_by_id('save').click()
        organisation.end_time = int(round(time.time() * 1000))
        organisation.time_to_add_emp = organisation.end_time - organisation.start_time
        organisation.time_to_add_emp = organisation.time_to_add_emp / 1000
        time.sleep(2)

        organisation.start_time = int(round(time.time() * 1000))
        driver.find_element_by_id('designation').send_keys(designation)
        driver.find_element_by_id('department').send_keys(department)
        driver.find_element_by_id('uuid').send_keys(uid)
        driver.find_element_by_id('salary').send_keys(salary)
        driver.find_element_by_id('user_type').send_keys(usertype)
        driver.find_element_by_id('savepay').click()
        organisation.end_time = int(round(time.time() * 1000))
        organisation.time_to_add_payroll = organisation.end_time - organisation.start_time
        organisation.time_to_add_payroll = organisation.time_to_add_payroll / 1000
        time.sleep(2)

        organisation.start_time = int(round(time.time() * 1000))
        driver.find_element_by_class_name('genorg').click()
        organisation.end_time = int(round(time.time() * 1000))
        organisation.time_to_generate_pdf = organisation.end_time - organisation.start_time
        organisation.time_to_generate_pdf = organisation.time_to_generate_pdf / 1000

    def save_to_cloud():
        config = {
            'ENDPOINT': '',
            'PRIMARYKEY': '',
            'DATABASE': '',
            'CONTAINER': ''
        }
        client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
            'masterKey': config['PRIMARYKEY']})  # Initialize the Cosmos client

        database_link = 'dbs/' + config['DATABASE']
        db = client.ReadDatabase(database_link)
        collection_link = database_link + '/colls/{0}'.format(config['CONTAINER'])
        collection = client.ReadContainer(collection_link)
        shel = str(5)
        item1 = client.CreateItem(collection['_self'], {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'time_to_get_new_details': organisation.time_to_get_new_details,
            'time_to_load_ehub': organisation.time_to_load_ehub,
            'time_to_login': organisation.time_to_login,
            'time_to_add_emp': organisation.time_to_add_emp,
            'time_to_add_payroll': organisation.time_to_add_payroll,
            'time_to_generate_pdf': organisation.time_to_generate_pdf
        })

add_emp = organisation.add_new_emp()
save_cloud = organisation.save_to_cloud()
