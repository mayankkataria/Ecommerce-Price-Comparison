from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def products():
    return render_template("products.html")

@app.route('/history/<product>')
def history(product):
    print('product: ', product)
    return render_template("history.html", data=product)