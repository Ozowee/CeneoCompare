import requests
import tls_client
import matplotlib.pyplot as plt
import numpy
from bs4 import BeautifulSoup
from pprint import pprint
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

class GetProducts(): 
    def __init__(self,query):
        self.session = tls_client.Session(client_identifier="chrome_113" )
        self.headers = {
            'Host': 'www.ceneo.pl',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/98.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.query = query
        self.AllProductsDetails = {}
        self.CurrentProductDetails = {}
        self.SpecificProductDetails = {}
    def ScrapProducts(self):

        keyword = self.query.replace(" ","+")
        req_scrap = self.session.get(f'https://www.ceneo.pl/Smartfony;szukaj-{keyword}', headers=self.headers)
        # print(req_scrap.text)
        if req_scrap.status_code != 200:
            print(f"Connection error, status code: {req_scrap.status_code}")
        else:
            soup = BeautifulSoup(req_scrap.text,'lxml')
            container = soup.find_all("div",{"class":"cat-prod-row js_category-list-item js_clickHashData js_man-track-event"})
            
            for product in container:
                singleProductDetails = []
                try:
                    productID = str(product).split('data-productid="')[1].split('"')[0]
                    productName = str(product).split('data-productname="')[1].split('"')[0]
                    productPrice = str(product).split('data-productminprice="')[1].split('"')[0]
                    productScore = str(product).split('<span class="product-score">')[1].split('<span class="screen-reader-text">')[0].replace("\n","")
                    productReviews = str(product).split('<span class="prod-review__qo">')[1].split('</a>')[0].split('">')[1].replace("\n","")
                    
                    try:
                        productImageUrl = "https:"+str(product).split('data-original="')[1].split('"')[0]
                    except IndexError:
                        req_image = requests.get(f'https://www.ceneo.pl/{productID}', headers=self.headers)
                        if req_image.status_code != 200:
                            print(f"Connection error, status code: {req_image.status_code}")
                        else:
                            soupImage = BeautifulSoup(req_image.text,'lxml')
                            containerImage = soupImage.find("a",{"class":"js_gallery-anchor js_gallery-item gallery-carousel__anchor"})
                            productImageUrl = "https:"+str(containerImage).split('href="')[1].split('"')[0]
                except IndexError:
                    productScore = "N/A"
                #try:
                self.AllProductsDetails[productName] = {
                    "productID":productID,
                    "productPrice":productPrice,
                    "productIMG":productImageUrl,
                    "productScore":productScore,
                    "productReviews":productReviews
                                                            }
                # except UnboundLocalError:
                #     self.AllProductsDetails["errorCode"] = {
                #         "ErrorInfo":"Wrong variable on input"
                #     }
            # print(self.AllProductsDetails)
    def GetSpecificProduct(self,productID):
        req_specific = self.session.get(f'https://www.ceneo.pl/{productID}',headers=self.headers)
        if req_specific.status_code !=200:
            print(f"Connection error, status code: {req_specific.status_code}")
        else:
            soup = BeautifulSoup(req_specific.text,'lxml')
            container = soup.findAll("li",{"class":"product-offers__list__item js_productOfferGroupItem"})
            productDesc = soup.find('div',{'class':'product-top__product-info__tags'}).text
            productTitle = soup.title.text.replace(' - Cena, opinie na Ceneo.pl','').replace('- ceny, opinie, sklepy - kup tanio na Ceneo.pl','')
            productParams = soup.find('div',{"class":"full-specs"}).table
            containerImage = soup.find("a",{"class":"js_gallery-anchor js_gallery-item gallery-carousel__anchor"})

            productImageUrl = 'https:'+ str(containerImage).split('href="')[1].split('"')[0]
            # https://image.ceneostatic.pl/data/products/138536499/i-apple-iphone-14-pro-128gb-gwiezdna-czern.jpg
            print(productImageUrl)

            self.CurrentProductDetails['title'] = productTitle
            self.CurrentProductDetails['desc'] = productDesc 
            self.CurrentProductDetails['img'] = productImageUrl

            params = {}
            for row in productParams.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    param_name = th.get_text(strip=True)
                    param_value = td.get_text(strip=True)
                    params[param_name] = param_value
            
            

            for data in container:
                dataOfferID = str(data).split('data-offerid="')[1].split('"')[0]
                productPrice = str(data).split('data-price="')[1].split('"')[0]
                productName = str(data).split('data-gaproductname="')[1].split('"')[0].split('/')[1]
                try:
                    retailerReviews = str(data).split('data-mini-shop-info-url="')[2].split('</span>')[0].split('>')[1]
                    retailerScore = str(data).split('<span class="screen-reader-text">')[1].split('</span>')[0]
                except IndexError:
                    retailerReviews = "Brak Opinii"
                    retailerScore = "N/A"
                
                retailerLogo = data.find('div',{"class":"product-offer__store__logo"}).img.get('data-original')
                try:
                    freeship = data.find('div',{'class':'free-delivery-label'}).text
                
                except:
                    freeship = 'Wysyłka dodatkowo płatna'

                try:
                    retailerUrl = "https://www.ceneo.pl"+str(data).split('<a class="button button--primary button--flex go-to-shop" ')[1].split('rel')[0].split('href="')[1].split('"')[0]
                    ratailerName = str(data).split('data-shopurl="')[1].split('"')[0]
                except IndexError:
                    # retailerUrl = f"https://koszyk.ceneo.pl/dodaj/{dataOfferID}"
                    # ratailerName = str(data).split('img alt="')[1].split('"')[0]
                    ratailerName = "ceneo.pl"

                self.SpecificProductDetails[dataOfferID] = {
                    "productName":productName,
                    "productPrice":float(productPrice),
                    "ratailerName":ratailerName,
                    "retailerUrl":retailerUrl,
                    "retailerReviews":retailerReviews,
                    "retailerScore":retailerScore,
                    "retailerLogo":retailerLogo,
                    "freeship":freeship
                                                        }
            sorted_data = dict(sorted(self.SpecificProductDetails.items(), key=lambda x: float(x[1]['productPrice'])))
            self.SpecificProductDetails = sorted_data
   
            
    def PriceGraph(self):
        prices = []
        retailers = []
        product_name = "priceGraph"
        for key,value in self.SpecificProductDetails.items():
            retailer = value.get('ratailerName')
            # if retailer in retailers:
            #     continue
            # if product_name=="":
            #     product_name = value.get('productName')
            prices.append(value.get('productPrice'))
            retailers.append(retailer)
        plt.figure(figsize=(12,6))
        bars = plt.bar(retailers,prices)

        for bar, price in zip(bars, prices):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                    str(price), ha='center', va='bottom')

        plt.xlabel('Retailer')
        plt.ylabel('Product Price')
        # plt.title(product_name)
        plt.xticks(rotation=90,fontsize=10)
        plt.tight_layout()
        plt.savefig(f'static/{product_name}.png')
        print("Graph successfully generated!")
        

        
