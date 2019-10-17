#!/usr/bin/python3
# Don't forget to set parameters!
import xlsxwriter
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# Set full path for <chromedriver.exe>
# Set Linkedin <username> and <password>
# Set <search query> which should 

# Parameters
target_company = '"<Legitimate Business Syndicate>"' # Keep the double quotes
file_name = r'dump.xlsx'
linkedin_username = '<linkedin_username>'
linkedin_password = '<linkedin_password'
chrome_options = Options() # making it work with linux
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=chrome_options) # http://chromedriver.chromium.org
search_query = 'site:linkedin.com/in/ AND "' + target_company + '"' # Just a standard google search, modify as desired
mind_row = 0

# function to ensure all key data fields have a value
def validate_field(field):
    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field

# defining new  variable passing two parameters
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()


# writerow() method to the write to the file object
worksheet.write(mind_row, 0, 'Name')
worksheet.write(mind_row, 1, 'Job Title')
worksheet.write(mind_row, 2, 'Company')
worksheet.write(mind_row, 3, 'College')
worksheet.write(mind_row, 4, 'Location')
worksheet.write(mind_row, 5, 'URL')
mind_row += 1

# driver.get method() will navigate to a page given by the URL address (2019 link fix)
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

# locate email form by_class_name
username = driver.find_element_by_id('username')
# send_keys() to simulate key strokes
username.send_keys(linkedin_username)

# sleep for 0.5 seconds
sleep(0.5)

# locate password form by_class_name
password = driver.find_element_by_id('password')
# send_keys() to simulate key strokes
password.send_keys(linkedin_password)
sleep(1.0)

# locate submit button by_xpath
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

# .click() to mimic button click
sign_in_button.click()
sleep(0.5)

# driver.get method() will navigate to a page given by the URL address
driver.get('https:www.google.com')
sleep(3)

# locate search form by_name
search_query_field = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query_field.send_keys(search_query)
sleep(0.5)

# navigate to the URL address specified by search_query in parameters.py
driver.get(search_query)

# .send_keys() to simulate the return key
search_query_field.send_keys(Keys.RETURN)
sleep(3)

# Get first 100 pages of results
linkedin_urls = []
for i in range(20):
    # Next Page
    next_page = driver.find_element_by_id('pnnext').get_attribute('href')
    driver.get(next_page)

for i in range(8):
    # locate URL by_class_name
    linkedin_urls_unparsed = driver.find_elements_by_partial_link_text(target_company)


    # variable linkedin_url is equal to the list comprehension
    for url in linkedin_urls_unparsed:
        linkedin_urls.append(url.get_attribute("href"))
        print(url.get_attribute("href"))
    sleep(0.5)

    # Next Page
    next_page = driver.find_element_by_id('pnnext').get_attribute('href')
    driver.get(next_page)

print(linkedin_urls)
# For loop to iterate over each URL in the list returned from the google search query
for linkedin_url in linkedin_urls:

    # get the profile URL
    driver.get(linkedin_url)
    sleep(5)

    # assigning the source code for the web page to variable sel
    sel = Selector(text=driver.page_source)

    # xpath to extract the text from the class containing the name
    # this is ugly, but it works with new HTML
    name = sel.xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
    # if name exists
    if name:
        # .strip() will remove the new line /n and white spaces
        name = name.strip()

    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/h2/text()').extract_first()

    if job_title:
        job_title = job_title.strip()

    # xpath to extract the text from the class containing the company
    company = sel.xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[2]/ul/li[1]/a/span/text()').extract_first()

    if company:
        company = company.strip()

    # xpath to extract the text from the class containing the college
    college = sel.xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[2]/ul/li[2]/a/span/text()').extract_first()

    if college:
        college = college.strip()

    # xpath to extract the text from the class containing the location
    location = sel.xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()

    if location:
        location = location.strip()

    # assignment of the current URL
    linkedin_url = driver.current_url

    # validating if the fields exist on the profile
    name = validate_field(name)
    job_title = validate_field(job_title)
    company = validate_field(company)
    college = validate_field(college)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)

    # printing the output to the terminal
    print('[+] ' + name + ' : ' + company)

    # writing the corresponding values to the header
    # encoding with utf-8 to ensure all characters get loaded
    worksheet.write(mind_row, 0, name)
    worksheet.write(mind_row, 1, job_title)
    worksheet.write(mind_row, 2, company)
    worksheet.write(mind_row, 3, college)
    worksheet.write(mind_row, 4, location)
    worksheet.write(mind_row, 5, linkedin_url)
    mind_row += 1
# terminates the application
try:
    workbook.close()
except IOError :
    print('Save error')
driver.quit()