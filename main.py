from flask import Flask,render_template,jsonify,request

app = Flask(__name__)


@app.route('/',methods=['GET'])
def mainRoute():
    return render_template('searchSite.html')


@app.route('/search',methods=['GET'])
def searchProduct():
    data = request.args.get('s','')
    return (jsonify({"message":"Success",'data':data}),200)


if __name__== "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run()