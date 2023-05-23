import requests
import matplotlib.pyplot as plt
import numpy
from bs4 import BeautifulSoup
from pprint import pprint

class GetProducts(): 
    def __init__(self,query):
        self.headers = {
            'Host': 'www.ceneo.pl',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="112", "Not_A Brand";v="24", "Opera GX";v="98"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.ceneo.pl/',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.query = query
        self.AllProductsDetails = {}
        self.SpecificProductDetails = {}
    def ScrapProducts(self):

        keyword = self.query.replace(" ","+")
        req_scrap = requests.get(f'https://www.ceneo.pl/Smartfony;szukaj-{keyword}', headers=self.headers)

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
                try:
                    self.AllProductsDetails[productName] = {
                        "productID":productID,
                        "productPrice":productPrice,
                        "productIMG":productImageUrl,
                        "productScore":productScore,
                        "productReviews":productReviews
                                                            }
                except UnboundLocalError:
                    self.AllProductsDetails["errorCode"] = {
                        "ErrorInfo":"Wrong variable on input"
                    }
            print(self.AllProductsDetails)
    def GetSpecificProduct(self,productID):
        req_specific = requests.get(f'https://www.ceneo.pl/{productID}',headers=self.headers)
        if req_specific.status_code !=200:
            print(f"Connection error, status code: {req_specific.status_code}")
        else:
            soup = BeautifulSoup(req_specific.text,'lxml')
            container = soup.findAll("li",{"class":"product-offers__list__item js_productOfferGroupItem"})
            for data in container:
                dataOfferID = str(data).split('data-offerid="')[1].split('"')[0]
                productPrice = str(data).split('data-price="')[1].split('"')[0]
                productName = str(data).split('data-gaproductname="')[1].split('"')[0].split('/')[1]
                retailerReviews = str(data).split('data-mini-shop-info-url="')[2].split('</span>')[0].split('>')[1]
                retailerScore = str(data).split('<span class="screen-reader-text">')[1].split('</span>')[0]
                try:
                    retailerUrl = "https://www.ceneo.pl"+str(data).split('<a class="button button--primary button--flex go-to-shop" ')[1].split('rel')[0].split('href="')[1].split('"')[0]
                    ratailerName = str(data).split('data-shopurl="')[1].split('"')[0]
                except IndexError:
                    # retailerUrl = f"https://koszyk.ceneo.pl/dodaj/{dataOfferID}"
                    # ratailerName = str(data).split('img alt="')[1].split('"')[0]
                    ratailerName = "ceneo.pl"

                self.SpecificProductDetails[dataOfferID] = {
                    "productName":productName,
                    "productPrice":productPrice,
                    "ratailerName":ratailerName,
                    "retailerUrl":retailerUrl,
                    "retailerReviews":retailerReviews,
                    "retailerScore":retailerScore
                                                        }
            sorted_data = dict(sorted(self.SpecificProductDetails.items(), key=lambda x: int(x[1]['productPrice'])))
            self.SpecificProductDetails = sorted_data
            
    def PriceGraph(self):
        prices = []
        retailers = []
        product_name = ""
        for key,value in self.SpecificProductDetails.items():
            if product_name=="":
                product_name = value.get('productName')
            prices.append(value.get('productPrice'))
            retailers.append(value.get('ratailerName'))
        plt.figure(figsize=(12,6))
        plt.bar(retailers,prices)
        plt.xlabel('Retailer')
        plt.ylabel('Product Price')
        plt.title(product_name)
        plt.xticks(rotation=90,fontsize=10)
        plt.tight_layout()
        plt.savefig(f'static/{product_name}.png')
        

        
iphone = GetProducts("iphone 14 pro")
#iphone.ScrapProducts()
iphone.GetSpecificProduct("138536499")
iphone.PriceGraph()

