from flask import Flask,render_template,jsonify,request
from utils import GetProducts
app = Flask(__name__)


@app.route('/',methods=['GET'])
def mainRoute():
    return render_template('searchSite.html')


@app.route('/search',methods=['GET'])
def searchProduct():
    data = request.args.get('s','')
    
    genOutput = GetProducts().ScrapProducts(data)

    return render_template('productSite.html')#,productData=genOutput)
    
@app.route('/product/<productID>',methods=['GET'])
def ProductPage():
    return render_template('productPage.html',productData='')

if __name__== "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run()