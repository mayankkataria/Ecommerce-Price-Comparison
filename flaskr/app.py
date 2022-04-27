import datetime
from enum import unique
from unicodedata import category
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import redis
import json
import urllib.parse
from  selenium import webdriver
from bs4 import BeautifulSoup
from sqlalchemy import exists
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Arcgate1!@localhost/Ecommerce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8080/Ecommerce'
db = SQLAlchemy(app)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

PRODUCTS = [
    {
        'name': 'Vivo Y21T (Midnight Blue, 4GB RAM, 128GB ROM)',
        'amazon_id': 'B09Q5Z5M9D',
        'amazon_uuid': '100c89c9-5268-4356-b084-be9f0d15a566',
        'flipkart_id': 'MOBG5VFCSKRABKAM',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'OPPO A31 (Fantasy White, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444SXZ6',
        'amazon_uuid': '8f6f83fa-c73d-4a83-b5b2-a055852ea602',
        'flipkart_id': 'MOBFPBD6NMXDG6UM',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'Redmi 9 Activ (Coral Green, 4GB RAM, 64GB Storage)',
        'amazon_id': 'B09GFLFMPS',
        'amazon_uuid': '215833f2-427a-4b3e-a4aa-5a8c5c60fae6',
        'flipkart_id': 'MOBG7FNG6HBQCPGY',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'OPPO A31 (Mystery Black, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444S68L',
        'amazon_uuid': 'f5fea155-61f6-49a4-b156-96d68d1bd211',
        'flipkart_id': 'MOBFPBD6ZYTJUAXN',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'Samsung Galaxy M12 (Blue,4GB RAM, 64GB Storage)',
        'amazon_id': 'B08XGDN3TZ',
        'amazon_uuid': '376447ee-ef45-4b47-8329-eb06788b9309',
        'flipkart_id': 'MOBGFG8GCPEGKGF4',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'Lenovo IdeaPad 3',
        'amazon_id': 'B09MM4FPMR',
        'amazon_uuid': 'c346a8fc-4ac2-47bf-8d2d-138652456ae7',
        'flipkart_id': 'COMG72M9XXDCHEQZ',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'HP 15- AMD Ryzen 3-3250',
        'amazon_id': 'B08T6THSMQ',
        'amazon_uuid': 'baa6d2a2-5c8d-4ddc-b964-016860db456a',
        'flipkart_id': 'COMFZHFWBE7APPH2',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'APPLE iPhone 13 Pro (Graphite, 128 GB)',
        'amazon_id': 'B09G91LWTZ',
        'amazon_uuid': 'fedcad8f-a23a-41ac-9310-02798f8b84ec',
        'flipkart_id': 'MOBG6VF5FYT935T7',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'APPLE 2020 Macbook Pro M1 - 8 GB/256 GB SSD',
        'amazon_id': 'B08N5WG761',
        'amazon_uuid': '7c049bed-b2c7-4f4c-9aa8-c2bed266e111',
        'flipkart_id': 'COMFXEKMTGHAGSVX',
        'amazon_area': '',
        'flipkart_area': ''
    },
    {
        'name': 'OnePlus Nord CE 2 5G (Bahamas Blue, 8GB RAM, 128GB Storage)',
        'amazon_id': 'B09RG5R5FG',
        'amazon_uuid': 'db9d4a21-118d-4c9f-9ca5-b8c83334ad95',
        'flipkart_id': 'MOBGDBYGG6PPNFD9',
        'amazon_area': '',
        'flipkart_area': ''
    }
]

# r = redis.StrictRedis(url='redis://:root.redislabs.com@:8085/Ecommerce')
class Product(db.Model):
    id = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    amazon_id = db.Column(db.String(50), unique=True)
    flipkart_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(50), nullable=False)
    amazon_price = db.Column(db.String(10), nullable=False)
    flipkart_price = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(12), nullable=False)

class History(db.Model):
    id = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    date = db.Column(db.String(12), nullable=False)
    amazon_price = db.Column(db.String(10), nullable=False)
    flipkart_price = db.Column(db.String(10), nullable=False)

def addToSql(amazon_id, flipkart_id, name, image_url, amazon_price, flipkart_price, date):
    print('------------------------------------add')
    # Add amazon products to db
    product = Product(
        amazon_id,
        flipkart_id,
        name,
        image_url,
        amazon_price,
        flipkart_price,
        date
    )
    history = History(date, amazon_price, flipkart_price)
    
    db.session.add(product)
    db.session.add(history)
    db.session.commit()

def updateToSql(amazon_id, flipkart_id, name, image_url, amazon_price, flipkart_price, date):
    print('-----------------------------------update')
    # Add amazon products to db
    product = Product(
        amazon_id,
        flipkart_id,
        name,
        image_url,
        amazon_price,
        flipkart_price,
        date
    )
    history = History(date, amazon_price, flipkart_price)
    
    db.session.update(product)
    db.session.add(history)
    db.session.commit()

def readFromSql():
    pass

@app.route('/')
def products():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/stonex/Desktop/Training/chromedriver')

    flipkart_area_list = []
    amazon_area_list = []
    for product in PRODUCTS:
        search = product['name']

        ### ------------Scrape on amazon-------------- ###
        url = 'https://www.amazon.in/s?k='
        # replace search's space from ' ' to '+' for amazon
        # amazon_search = search.translate(str.maketrans(' ', '+'))
        # amazon_search = search.replace(' ', '%20')
        amazon_search = urllib.parse.quote_plus(search)
        """
        https://www.amazon.in/s?k=Vivo+Y21T+%28Midnight+Blue%2C+4GB+RAM%2C+128GB+ROM%29
        https://www.amazon.in/s?k=Vivo+Y21T+%28Midnight+Blue%2C+4GB+RAM%2C+128GB+ROM%29
        """
        # print('--------amazon search-----------', amazon_search)
        # print('---------amazon search--------------', url+amazon_search)
        browserdriver.get(url+amazon_search)
        content = browserdriver.page_source
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        search_area = soup.findAll('div', 's-result-item')
        # print('search area 0 i', search_area[2])
        # print('---area find----', search_area[2].attrs['data-asin'])
        # print('---------search area------------', search_area, '\n')
        for area in search_area:
            # print('------area, id------------', area, product['amazon_id'], '\n')
            if (area.attrs['data-asin'] == product['amazon_id']):
            # if ("B08XGDN3TZ" in area):
            # if (product['amazon_id'] in area):
                # print("++++++++++++++++++++++++")
                amazon_area_list.append(area)
                product.update({'amazon_area': amazon_area_list})
                break

        ### ------------Scrape on flipkart-------------- ###
        url = 'https://www.flipkart.com/search?q='
        # replace search's space from ' ' to '%20' for amazon
        # flipkart_search = search.translate(str.maketrans(' ', '%20'))
        # flipkart_search = search.replace(' ', '%20')
        flipkart_search = search
        browserdriver.get(url+flipkart_search)
        content = browserdriver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        search_area = soup.findAll('div', '_13oc-S')
        for area in search_area:
            if (area.find('div', {'data-id': product['flipkart_id']})):
            # if (product['flipkart_id'] in area):
                # print('------------------area---------------', area)
                flipkart_area_list.append(area)
                product.update({'flipkart_area': flipkart_area_list})
                break

        print('------------------------- before product exists')
        productExists = db.session.query(exists().where(Product.amazon_id==product['amazon_id'])).scalar()
        prodCount = db.session.query(Product).filter(Product.amazon_id==product['amazon_id']).count()
        print('product exists: ', prodCount)
        if (not productExists):
            # Add amazon products to db
            addToSql(product['amazon_id'], product['flipkart_id'], product['name'], product['amazon_area'].find('img','s-image'), product['amazon_area'].find('span', 'a-offscreen'), product['flipkart_area'].find('div', '_30jeq3 _1_WHN1'), datetime.datetime.utcnow())
        else:
            # update if date is new
            dateIsNew = db.session.query(exists().where(Product.date.date()==datetime.datetime.utcnow().date())).scalar()
            print('date is new: ', dateIsNew)
            if (dateIsNew):
                updateToSql(product['amazon_id'], product['flipkart_id'], product['name'], product['amazon_area'].find('img','s-image'), product['amazon_area'].find('span', 'a-offscreen'), product['flipkart_area'].find('div', '_30jeq3 _1_WHN1'), datetime.datetime.utcnow())

        redis_client.set("data", json.dumps(product))
        redisData = redis_client.get("data")
        print('redis data: ', redisData)
        # print('---------area list-----------', flipkart_area_list)        


    # search = 'smartphone'
    
    # ### ------------ Scrape on amazon -------------- ###
    # url = 'https://www.amazon.com/s?k='
    # browserdriver.get(url+search)
    # content = browserdriver.page_source
    # soup = BeautifulSoup(content, 'html.parser')
    # amazon_search_area = soup.findAll('div', 's-result-item')
    # print('--------------------------------------area------------------------------------------: ', amazon_search_area)


    # ### -----------Scrape on flipkart------------- ###
    # url = 'https://www.flipkart.com/search?q='
    # browserdriver.get(url+search)
    # content = browserdriver.page_source
    # soup = BeautifulSoup(content, 'html.parser')
    # flipkart_search_area = soup.findAll('div', '_13oc-S')
    # print('--------------------------------------area------------------------------------------: ', flipkart_search_area)
    # print('products: ', PRODUCTS)
    return render_template("products.html", flipkart_area = product['flipkart_area'], amazon_area = product['amazon_area'])

@app.route('/history/<product>')
def history(product):
    print('product: ', product)
    return render_template("history.html", data=product)