from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Parse:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome('/home/xbtio/Downloads/chromedriver_linux64 (1)/chromedriver')
        self.wait = WebDriverWait(self.driver, 10)
    


    def getGrades(self, link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source)
        regMid = soup.find_all('td', class_='column-grade')
        values = {'Register Term': regMid[2].get_text(), 'Register Final': regMid[3].get_text()}
        return values

    def message(self, q, a):
        return '{0} \nRegister Term  : {1} \nRegister Final : {2}'.format(q, a['Register Term'], a['Register Final'])


    def parse(self, log, pas):
        self.driver.get('https://moodle.astanait.edu.kz/login/index.php')

        element1 = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'OpenID Connect')))
        element1.click()

        login = self.wait.until(EC.visibility_of_element_located((By.ID, "i0116"))).send_keys(log + '@astanait.edu.kz')

        button = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

        passw = self.wait.until(EC.visibility_of_element_located((By.ID, "i0118"))).send_keys(pas)
        
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click() 

        button = self.wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back")))
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()

        self.driver.get('https://moodle.astanait.edu.kz/grade/report/overview/index.php')

        listOfNames = []

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        for link in soup.find_all('td'):
            if link.attrs['class'][1] == 'c0' and link.find('a'):
                listOfNames.append((link.find('a').get_text(), self.getGrades(link.find('a').get('href'))))

        self.driver.get('https://moodle.astanait.edu.kz/login/logout.php?sesskey=h8SqwJrWsa')
        button1 = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))).click()
        self.driver.close()
        return dict(listOfNames)
        