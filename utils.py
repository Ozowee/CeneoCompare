import requests
from bs4 import BeautifulSoup
from pprint import pprint

class GetProducts(): 
    def __init__(self,query=""):
        self.query = query
    def ScrapProducts(self,query):
        self.query = query
        self.counter = 0
        headers = {
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
        keyword = self.query.replace(" ","+")
        req_scrap = requests.get(f'https://www.ceneo.pl/Smartfony;szukaj-{keyword}', headers=headers)

        if req_scrap.status_code != 200:
            print(f"Connection error, status code: {req_scrap.status_code}")
        else:
            AllProductsDetails = []
            soup = BeautifulSoup(req_scrap.text,'lxml')
            #cat-prod-row__body
            container = soup.find_all("div",{"class":"cat-prod-row js_category-list-item js_clickHashData js_man-track-event"})
            
            for product in container:
                if self.counter > 10:
                    break
                else:
                    self.counter += 1
                    singleProductDetails = []
                    productID = str(product).split('data-productid="')[1].split('"')[0]
                    productName = str(product).split('data-productname="')[1].split('"')[0]
                    productPrice = str(product).split('data-productminprice="')[1].split('"')[0]
                    try:
                        productImageUrl = "https:"+str(product).split('data-original="')[1].split('"')[0]
                    except IndexError:
                        req_image = requests.get(f'https://www.ceneo.pl/{productID}', headers=headers)
                        if req_image.status_code != 200:
                            print(f"Connection error, status code: {req_image.status_code}")
                        else:
                            soupImage = BeautifulSoup(req_image.text,'lxml')
                            containerImage = soupImage.find("a",{"class":"js_gallery-anchor js_gallery-item gallery-carousel__anchor"})
                            productImageUrl = str(containerImage).split('href="')[1].split('"')[0]
                    productScore = str(product).split('<span class="product-score">')[1].split('<span class="screen-reader-text">')[0].replace("\n","")
                    productReviews = str(product).split('<span class="prod-review__qo">')[1].split('</a>')[0].split('">')[1].replace("\n","")
                    #print(productID,productName,productPrice,productImageUrl,productScore,productReviews)
                    for i in [productID,productName,productPrice,productImageUrl,productScore,productReviews]:
                        singleProductDetails.append(i)
                    AllProductsDetails.append(singleProductDetails)
            print(AllProductsDetails)
            return AllProductsDetails
        

# iphone = GetProducts()
# iphone.ScrapProducts("iphone 14 pro")