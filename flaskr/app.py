from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# import redis
from  selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Ecommerce'
# db = SQLAlchemy(app)

# r = redis.StrictRedis(url='redis://:root.redislabs.com@:8085/Ecommerce')
# class Products(db.Model):
#     id = db.Column(db.String(50), unique=True, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     image_url = db.Column(db.String(50), nullable=False)
#     price = db.Column(db.String(10), nullable=False)
#     date = db.Column(db.String(12), nullable=False)

@app.route('/')
def products():
    # ------------Scrape on amazon--------------
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/stonex/Desktop/Training/chromedriver')
    search = 'smartphone'
    url = 'https://www.amazon.com/s?k='
    browserdriver.get(url+search)
    content = browserdriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    amazon_search_area = soup.findAll('div', 's-result-item')
    print('--------------------------------------area------------------------------------------: ', amazon_search_area)
    url = 'https://www.flipkart.com/s?k='
    browserdriver.get(url+search)
    content = browserdriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    flipkart_search_area = soup.findAll('div', '_13oc-S')
    # -----------Scrape on flipkart-------------

    return render_template("products.html", amazon_area=amazon_search_area, flipkart_area=flipkart_search_area)

@app.route('/history/<product>')
def history(product):
    print('product: ', product)
    return render_template("history.html", data=product)