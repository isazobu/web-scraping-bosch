
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
import numpy as np
import pandas as pd
import logging
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='extractFromBoschLogs.txt')


logger = logging.getLogger('scraping')

class Refrigerator:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install()) 
        self.link = "https://www.bosch-home.com.tr/urun-listesi/buzdolaplari-derin-dondurucular/?pageNumber="
   
        self.allProductNames = np.array([])
        self.allProductCodes= np.array([])
        self.allProductScores= np.array([])
        
    def get_source(self,link):
        logger.info(f'Requesting {link}')
        self.driver.get(link)
        html = self.driver.page_source
        soup = BeautifulSoup(html)
        return soup

    def getProductNameAndCode(self,soup):
        
        productNames = soup.find_all("h2",attrs = {"class":"a-heading"})
        
        titles =[]
        codes = []
        
        for i in range(len(productNames)-1):    
            # Codes
            if(i%2==1):
                 # Remove '\n'
                 
                 codes.append(productNames[i].text[1:-1])
                 
        
            else:
                title = ""
                spans= productNames[i].find_all("span")
                for span in spans:
                    title += (span.text + ' ')
                if title != '':
                    titles.append(title)    
                
        
        return titles, codes
             
    
    def getScores(self, soup):
        # Patern -> ['Score','Vote','Score','Vote','Score','Vote'...]
        scoresandvotes = soup.find_all("span",attrs={"class":"text number"})
        
        scores = []
        # Get scores without votes --> 
        
        for score in range(0,len(scoresandvotes),2):
            scores.append(scoresandvotes[score].text)
    
        return scores
    
    def getData(self):
        for i in range(1,13):
            
            soup = self.get_source(self.link + str(i))
            names, codes = self.getProductNameAndCode(soup)
            scores = self.getScores(soup)
            
            self.allProductNames = np.append(self.allProductNames,names)
            self.allProductCodes = np.append(self.allProductCodes,codes)
            self.allProductScores =  np.append(self.allProductScores,scores)
        
    def toCSV(self):
        df = pd.DataFrame()

        df['Product_Name'] = self.allProductNames
        df['Product_Code'] = self.allProductCodes
        df['Product_Score'] = self.allProductScores


        df.to_csv('Bosch Refrigerator.csv',encoding="utf-8-sig")    
        
        
    
    def driverQuit(self):
        self.driver.quit()        






def main():
    start = time.time()
    logger.info("Data extract has been started.")
    refrigerator = Refrigerator()
    refrigerator.getData()
    refrigerator.driverQuit()
    refrigerator.toCSV()
    logger.info("Data extract has been ended.")
    end = time.time()
    print(f"Performance: {end - start}")



if __name__ == "__main__":
    main()

    
    

        



    



