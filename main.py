from flask import Flask,render_template,jsonify,request
from utils import GetProducts
app = Flask(__name__)


@app.route('/',methods=['GET'])
def mainRoute():
    return render_template('searchSite.html')


@app.route('/search',methods=['GET'])
def searchProduct():
    data = request.args.get('s','')    
    output = GetProducts(data)
    output.ScrapProducts()

    return render_template('productSite.html',data=output.AllProductsDetails)
    
@app.route('/product/<productID>',methods=['GET'])
def ProductPage(productID):
    return render_template('productPage.html')

if __name__== "__main__":
    app.run()