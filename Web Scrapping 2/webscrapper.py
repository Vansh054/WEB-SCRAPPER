from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

final_list = []

headers = ['Name', 'LIGHT_YEARS_FROM_EARTH', 'PLANET_MASS', 'STELLAR_MAGNITUDE', 'DISCOVERY_DATE',
           'HYPERLINK', 'PLANE_TYPE', 'PLANET_RADIUS', 'ORBITAL_RADIUS', 'ORBITAL_PERIOD', 'ECCENTRICITY']
planetdata = []

starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome(
    "C:/Users/my pc/Downloads/chromedriver_win32/chromedriver.exe")
browser.get(starturl)

time.sleep(10)


def scrapthedata():
    for i in range(0, 3):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        allultag = soup.find_all("ul", attrs={"class", "exoplanet"})
        for eachul in allultag:
            alllitags = eachul.find_all("li")
            templist = []
            for index, eachli in enumerate(alllitags):
                if index == 0:
                    templist.append(eachli.find_all("a")[0].contents[0])
                else:
                    templist.append(eachli.contents[0])
            hyperlinktag = alllitags[0]
            templist.append("https://exoplanets.nasa.gov" +
                            hyperlinktag.find_all("a", href=True)[0]["href"])
            planetdata.append(templist)

        browser.find_element_by_xpath(
            '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    


scrapthedata()

newplanetdata =[]
def scrapmoredata(hyperlinkk):
    page = requests.get(hyperlinkk)
    soup = BeautifulSoup(page.content, "html.parser")
    alltrtags = soup.find_all("tr",attrs={"class","fact_row"})
    templist= []
    for indextr,eachtr in enumerate(alltrtags) :
        alltdtag = eachtr.find_all("td")
        for indextd,eachtd in enumerate(alltdtag):
            if ( (indextr==0 and indextd==1) or (indextr==1 and indextd==0) or (indextr==3 and indextd==1) ) :
                continue
            else :
                data = eachtd.find_all("div",attrs={"class","value"})[0].contents[0].get_text()
                templist.append(data.replace("\n", ""))
            #print(eachtd.find_all("div",attrs={"class","value"})[0].contents)
    #print(templist)
    newplanetdata.append(templist)

for i in planetdata:
    scrapmoredata(i[5])

for index,i in enumerate(planetdata):
    final_list.append(planetdata[index]+newplanetdata[index])

with open('scrapping.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_list)