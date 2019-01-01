import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("https://aswbe-i.ana.co.jp/international_asw/pages/revenue/search/roundtrip/search_roundtrip_input.xhtml?CONNECTION_KIND=TWN&LANG=en")
#choice departureAirport-------------------------------------------
time.sleep(3)
departureAirport = driver.find_element_by_name("departureAirportCode:field_pctext")
departureAirport.send_keys("Taipei(Taoyuan)")
departureAirport.click()
#choice arrivalAirport----------------------------------------------
time.sleep(3)
arrivalAirport = driver.find_element_by_name("arrivalAirportCode:field_pctext")
arrivalAirport.send_keys("Tokyo(Narita)")
arrivalAirport.click()
time.sleep(3)
#-------------------------------------------------------------------
GoDateBtn = driver.find_element_by_id(u"departureDate:field_pctext")
BackDateBtn = driver.find_element_by_id(u"returnDate:field_pctext")
#choice go date----------------------------------------------------
GoDateBtn.click()
days = driver.find_elements_by_tag_name("td")
for td in days:
    if td.get_attribute("abbr")==("2016-12-20"):
        td.click()
        break
#choice back date-----------------------------------------------------------
time.sleep(3)
BackDateBtn.click()
days = driver.find_elements_by_tag_name("td")
for td in days:
    if td.get_attribute("abbr")==("2017-01-13"):
        td.click()
        break
#search flight----------------------------------------------------------------
search = driver.find_element_by_id("btnResearch")
search.click()
time.sleep(3)

#waiting response------------------------------------------------------------

#Next------------------------------------------------------------------------
nextstep1 = driver.find_element_by_css_selector('#j_idt277 > ul > li.btnArrowNext > input')
nextstep1.click()

#Next2-------------------------------------------------------------------------
nextstep2 = driver.find_element_by_id("nextButton")
nextstep2.click()
#to fill your data
nextstep3 = driver.find_element_by_name(u"j_idt1912")
nextstep3.click()
#fill_text----------------------------------------------------------------------
firstname = driver.find_element_by_id(u"passengers:0:firstName")
firstname.send_keys("Bryant")
lastname = driver.find_element_by_id(u"passengers:0:lastName")
lastname.send_keys("Kobe")
midlename = driver.find_element_by_id(u"passengers:0:middleName")
midlename.send_keys("God")

bdmonth = driver.find_element_by_name("passengers:0:adultDateOfBirth:select1")
bdmonth.send_keys("03")
bdmonth.click()

bdday = driver.find_element_by_name("passengers:0:adultDateOfBirth:select2")
bdday.send_keys("08")
bdday.click()

bdyear = driver.find_element_by_name("passengers:0:adultDateOfBirth:select3")
bdyear.send_keys("1994")
bdyear.click()

gendar = driver.find_element_by_name("passengers:0:gender:radioGroup")
gendar.send_keys("MALE")
gendar.click()

country = driver.find_element_by_name("passengers:0:nationality")
country.send_keys("Taiwan")
country.click()

mobile = driver.find_element_by_name("priorTravelCountryCode")
mobile.send_keys("Taiwan")
mobile.click()

mobile_num = driver.find_element_by_id("priorTravelDescription")
mobile_num.send_keys("0988888888")

email = driver.find_element_by_id("emailNotificationDescription")
email.send_keys("HelloWorld@ttu.edu.tw")
