from selenium import webdriver
import time
import json
import os
import webbrowser
from selenium.webdriver.common.by import By


def main():

    # by past week
    # url = "https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer%20Intern&location=United%20States&locationId=&geoId=103644278&f_TPR=r604800&position=1&pageNum=0"

    # by past 24 hours
    url = "https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer%20Intern&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&position=1&pageNum=0"

    # opening chrome
    driver = webdriver.Chrome(
        executable_path=r"C:\Users\moyue\Downloads\chromedriver.exe"
    )
    driver.get(url)
    driver.implicitly_wait(10)

    numOfJobs = int(
        driver.find_element(By.CLASS_NAME, "results-context-header__job-count").text
    )

    # keep scrolling down until the number of jobs is reached
    i = numOfJobs
    while i > 0:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        i -= 25

        try:
            x = driver.find_elements(
                By.XPATH, "//button[@aria-label='Load more results']"
            )
            driver.execute_script("arguments[0].click();", x[0])
            time.sleep(1)
        except:
            pass

    try:
        with open("companiesList.json", "r") as f:
            companies = json.load(f)
    except:
        companies = {}

    companyNames = driver.find_elements(By.CLASS_NAME, "base-search-card__subtitle")
    jobTitles = driver.find_elements(By.CLASS_NAME, "base-search-card__title")
    jobLinks = driver.find_elements(By.CLASS_NAME, "base-card__full-link")

    for company in companyNames:
        if company.text not in companies:
            companies[company.text] = []

    newJobs = {}
    changesMade = False

    for job in range(numOfJobs):
        try:
            name = companyNames[job].text
            title = jobTitles[job].text
            link = jobLinks[job].get_attribute("href")

            alreadyExists = False
            for i in companies[name]:
                if title == i[0]:
                    alreadyExists = True
                    break

            if not alreadyExists:
                changesMade = True
                if name not in newJobs:
                    newJobs[name] = []


                

                newJobs[name].append((title, link))
                companies[name].append((title, link))

        except:
            print("DONE")
            break
        
    with open("newJobs.json", "w") as f:
            json.dump(newJobs, f)

    if changesMade:
        with open("companiesList.json", "w") as f:
            json.dump(companies, f)
    
    driver.quit()

    webbrowser.open('file://' + os.path.realpath('newjobs.json'))


if __name__ == "__main__":
    main()
