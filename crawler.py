from bs4 import BeautifulSoup
import urllib
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# from time import sleep

links = []
hotels = []
cnt = 0


def findreview(j):
    print j
    fp = open('datasets/' + hotels[j], "w")
    print hotels[j]
    driver = webdriver.Firefox()
    print "#######WebDriver created"
    driver.get('http://www.tripadvisor.in' + links[j] + '#REVIEW')
    print "#######Web page loaded"
    for i in range(10):
        print '\npage ' + str(i + 1)
        moreLink = driver.find_element_by_class_name('partnerRvw123')
        moreLink = moreLink.find_element_by_class_name('moreLink')
        moreLink.click()
        print "#######More clicked"
        driver.refresh()
        print "#######Page refreshed"
        moreLink = driver.find_element_by_class_name('partnerRvw')
        moreLink = moreLink.find_element_by_class_name('moreLink')
        moreLink.click()
        reviews = driver.find_elements_by_class_name('entry')
        for review in reviews:
            review = review.find_element_by_tag_name('p')
            data = review.text
            asciidata = data.encode("ascii", "ignore")
            fp.write('\n\n' + asciidata)
            print '.',
            # print review.text
        moreLink = driver.find_element_by_class_name(
            'pagination')
        moreLink = moreLink.find_element_by_class_name('next')
        try:
            moreLink.click()
        except Exception, e:
            driver.close()
            fp.close()
            return
    driver.close()
    fp.close()

    # try:
    #     moreLink = driver.find_element_by_class_name('partial_entry')
    #     reviews = driver.find_elements_by_class_name('entry')
    #     for review in reviews:
    #         review = review.find_element_by_tag_name('p')
    #         print review.text
    # except Exception, e:
    # print "#######Exception"
    # driver.find_element_by_class_name('close').click()
    # driver.execute_script("div.classlist.remove('spring2015 overlay')")
    #     driver.refresh()
    # print "#######Page refreshed"
    #     moreLink = driver.find_element_by_class_name('partnerRvw')
    #     moreLink = moreLink.find_element_by_class_name('moreLink')
    #     moreLink.click()
    #     reviews = driver.find_elements_by_class_name('entry')
    #     for review in reviews:
    #         review = review.find_element_by_tag_name('p')
    #         print review.text
    #     pass


contents = urllib.urlopen(
    'http://www.tripadvisor.in/Hotels-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Hotels.html')
soup = BeautifulSoup(contents.read())

for link in soup.find_all('a', {'class': 'property_title'}):
    links.append(link.get('href'))
    hotels.append(link.get_text())
    cnt = cnt + 1


fp = open('Hotels', 'w')
for hotel in hotels:
    for name in hotel.split('\n'):
        if name == '':
            continue
        fp.write(name + '\n')
    # endfor
# endfor
fp.close()


for i in range(cnt):
    findreview(i)
