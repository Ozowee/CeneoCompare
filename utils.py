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
                productID = str(product).split('data-productid="')[1].split('"')[0]
                productName = str(product).split('data-productname="')[1].split('"')[0]
                productPrice = str(product).split('data-productminprice="')[1].split('"')[0]
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
                productScore = str(product).split('<span class="product-score">')[1].split('<span class="screen-reader-text">')[0].replace("\n","")
                productReviews = str(product).split('<span class="prod-review__qo">')[1].split('</a>')[0].split('">')[1].replace("\n","")
                
                self.AllProductsDetails[productName] = {
                    "productID":productID,
                    "productPrice":productPrice,
                    "productIMG":productImageUrl,
                    "productScore":productScore,
                    "productReviews":productReviews
                                                        }

    def GetSpecificProduct(self,productID):
        req_specific = requests.get(f'https://www.ceneo.pl/{productID}',headers=self.headers)
        if req_specific.status_code !=200:
            print(f"Connection error, status code: {req_specific.status_code}")
        else:
            soup = BeautifulSoup(req_specific.text,'lxml')
            container = soup.findAll("li",{"class":"product-offers__list__item js_productOfferGroupItem"})
            for data in container:
                productPrice = str(data).split('data-price="')[1].split('"')[0]
                productName = str(data).split('data-gaproductname="')[1].split('"')[0].split('/')[1]
                retailerReviews = str(data).split('data-mini-shop-info-url="')[2].split('</span>')[0].split('>')[1]
                retailerScore = str(data).split('<span class="screen-reader-text">')[1].split('</span>')[0]
                try:
                    retailerUrl = "https://www.ceneo.pl"+str(data).split('<a class="button button--primary button--flex go-to-shop" ')[1].split('rel')[0].split('href="')[1].split('"')[0]
                    ratailerName = str(data).split('data-shopurl="')[1].split('"')[0]
                except IndexError:
                    dataOfferID = str(data).split('data-offerid="')[1].split('"')[0]
                    retailerUrl = f"https://koszyk.ceneo.pl/dodaj/{dataOfferID}"
                    ratailerName = str(data).split('img alt="')[1].split('"')[0]
                

    def PriceGraph(self):
        values = []
        indexes = []
        for i in self.AllProductsDetails:
            if len(indexes)<=10:
                price = i[2]
                productName = i[1]
                values.append(float(i[2]))
                indexes.append(i[1])
        unique_models = list(set(indexes))
        x = numpy.arange(len(unique_models))
        plt.bar(x,values)
        plt.xticks(x,unique_models,rotation=90)
        plt.xlabel("Model")
        plt.ylabel("Cena")
        plt.tight_layout()
        plt.show()


# iphone = GetProducts("iphone 14 pro")
# iphone.ScrapProducts()
# print(iphone.AllProductsDetails)
#iphone.ScrapProducts()
#iphone.PriceGraph()
# iphone.GetSpecificProduct("138536499")
