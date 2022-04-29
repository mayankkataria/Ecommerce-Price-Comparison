import datetime
from email.policy import default
from enum import unique
from unicodedata import category
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import redis
import json
import urllib.parse
from  selenium import webdriver
from bs4 import BeautifulSoup
from sqlalchemy import ForeignKey, Integer, exists
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import dateinfer

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Arcgate1!@localhost/Ecommerce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8080/Ecommerce'
db = SQLAlchemy(app)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

Base = declarative_base()

PRODUCTS = [
    {
        'name': 'Vivo Y21T (Midnight Blue, 4GB RAM, 128GB ROM)',
        'amazon_id': 'B09Q5Z5M9D',
        'flipkart_id': 'MOBG5VFCSKRABKAM',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'OPPO A31 (Fantasy White, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444SXZ6',
        'flipkart_id': 'MOBFPBD6NMXDG6UM',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'Redmi 9 Activ (Coral Green, 4GB RAM, 64GB Storage)',
        'amazon_id': 'B09GFLFMPS',
        'flipkart_id': 'MOBG7FNG6HBQCPGY',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'OPPO A31 (Mystery Black, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444S68L',
        'flipkart_id': 'MOBFPBD6ZYTJUAXN',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'Samsung Galaxy M12 (Blue,4GB RAM, 64GB Storage)',
        'amazon_id': 'B08XGDN3TZ',
        'flipkart_id': 'MOBGFG8GCPEGKGF4',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'Lenovo IdeaPad 3',
        'amazon_id': 'B09MM4FPMR',
        'flipkart_id': 'COMG72M9XXDCHEQZ',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'HP 15- AMD Ryzen 3-3250',
        'amazon_id': 'B08T6THSMQ',
        'flipkart_id': 'COMFZHFWBE7APPH2',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'APPLE iPhone 13 Pro (Graphite, 128 GB)',
        'amazon_id': 'B09G91LWTZ',
        'flipkart_id': 'MOBG6VF5FYT935T7',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'APPLE 2020 Macbook Pro M1 - 8 GB/256 GB SSD',
        'amazon_id': 'B08N5WG761',
        'flipkart_id': 'COMFXEKMTGHAGSVX',
        'amazon_price': '',
        'flipkart_price': ''
    },
    {
        'name': 'OnePlus Nord CE 2 5G (Bahamas Blue, 8GB RAM, 128GB Storage)',
        'amazon_id': 'B09RG5R5FG',
        'flipkart_id': 'MOBGDBYGG6PPNFD9',
        'amazon_price': '',
        'flipkart_price': ''
    }
]

# r = redis.StrictRedis(url='redis://:root.redislabs.com@:8085/Ecommerce')
class Product(db.Model):
    id = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    amazon_id = db.Column(db.String(50), unique=True)
    flipkart_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(50), nullable=False)
    amazon_price = db.Column(db.String(10), nullable=False)
    flipkart_price = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    history = relationship("History", backref="product")

class History(db.Model):
    id = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    print('-------------------------before product id')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    amazon_price = db.Column(db.String(10), nullable=False)
    flipkart_price = db.Column(db.String(10), nullable=False)

def addToSql(amazon_id, flipkart_id, name, image_url, amazon_price, flipkart_price, date):
    print('------------------------------------add')
    # Add amazon products to db
    product = Product(
        amazon_id=amazon_id,
        flipkart_id=flipkart_id,
        name=name,
        image_url=image_url,
        amazon_price=amazon_price,
        flipkart_price=flipkart_price,
        date=date
    )

    history = History(
        date=date,
        amazon_price=amazon_price,
        flipkart_price=flipkart_price,
        product=product
    )

    db.session.add(product)
    db.session.add(history)
    db.session.commit()
    print('-------------------------after product id commit')

def updateToSql(amazon_id, flipkart_id, name, image_url, amazon_price, flipkart_price, date):
    print('-----------------------------------update')
    # Add amazon products to db
    product = Product(
        amazon_id=amazon_id,
        flipkart_id=flipkart_id,
        name=name,
        image_url=image_url,
        amazon_price=amazon_price,
        flipkart_price=flipkart_price,
        date=date
    )

    history = History(
        date=date,
        amazon_price=amazon_price,
        flipkart_price=flipkart_price
    )
    
    db.session.add(json.dumps(product))
    db.session.add(json.dumps(history))
    db.session.commit()

def readFromSql():
    pass

def datetime_parser(v):
    print('------------------------dct: ', v)
    # for k, v in dct.items():
    #     # if isinstance(v, basestring) and re.search("\ UTC", v):
    #     try:
    #         dct = datetime.datetime.strptime(v, '%a, %d %b %Y %H:%M:%S UTC')
    #     except:
    #         pass
    #     return dct

@app.route('/')
def products():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/stonex/Desktop/Training/chromedriver')

    # if current date data exists in redis than fetch from it else scrape new day data from ecommerce sites
    # syncDate = redis_client.get("syncDate")
    syncDate = datetime.datetime.strptime(json.loads(redis_client.get("syncDate")), '%Y-%m-%d %I:%M:%S.%f')
    print('sync date, today', syncDate.date(), datetime.datetime.utcnow().date())
    if (syncDate.date() == datetime.datetime.utcnow().date()):
        # Fetch from redis
        products_arr = json.loads(redis_client.get("products"))
    else:
        # Fetch new day data from ecommerce sites
        # print('redis date: ', strippedDate.date())
        # print('infer date: ', dateinfer.infer([loadedDate]))


        # products_arr = redis_client.get("products")
        # print('redis data: ', json.loads(redisData))
        
        # print('date - ', datetime.datetime.utcnow().date())
        # if (redisData and redisData[0].date == datetime.datetime.utcnow()):
        #     products_arr = json.loads(redisData)
        
        # print('products arr: ', products_arr)
        # redis_client.set("products", json.dumps(products_arr))
        # redisData = redis_client.get("products")
        # print('redis data: ', json.loads(redisData))
        # products_arr = json.loads(redisData)
        # print('products arr: ', products_arr)

        products_arr = PRODUCTS

        for product in products_arr:
            search = product['name']

            ### ------------ Scrape on amazon -------------- ###
            url = 'https://www.amazon.in/s?k='
            amazon_search = urllib.parse.quote_plus(search)
            """
            https://www.amazon.in/s?k=Vivo+Y21T+%28Midnight+Blue%2C+4GB+RAM%2C+128GB+ROM%29
            https://www.amazon.in/s?k=Vivo+Y21T+%28Midnight+Blue%2C+4GB+RAM%2C+128GB+ROM%29
            """

            browserdriver.get(url+amazon_search)
            content = browserdriver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            amazon_search_area = soup.findAll('div', 's-result-item')

            ### ------------Scrape on flipkart-------------- ###
            url = 'https://www.flipkart.com/search?q='
            flipkart_search = search
            browserdriver.get(url+flipkart_search)
            content = browserdriver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            flipkart_search_area = soup.findAll('div', '_13oc-S')

            for area in amazon_search_area:
                if (area.attrs['data-asin'] == product['amazon_id']):
                    print('image url : ', area.find('img', 's-image').attrs['src'])
                    product['image_url'] = area.find('img', 's-image').attrs['src']
                    product['amazon_price'] = area.find('span', 'a-offscreen').text
                    # product['date'] = datetime.datetime.utcnow()
                    # print('utc now: ', datetime.datetime.utcnow().isoformat())
                    # dumpedData = json.dumps(datetime.datetime.utcnow(), default=str)
                    # print('json dumps: ', dumpedData)
                    # print('json loads: ', json.loads((dumpedData), object_hook=datetime_parser))
                    # amazon_area_list.append(area)
                    # product.update({'amazon_area': amazon_area_list})
                    
                    # print('------------------------- before product exists')
                    # productExists = db.session.query(exists().where(Product.amazon_id==product['amazon_id'])).scalar()
                    # # prodCount = db.session.query(Product).filter(Product.amazon_id==product['amazon_id']).count()
                    # print('------------------------- product exists: ', productExists)
                    # if (not productExists):
                    #     # Add amazon products to db
                    #     addToSql(product['amazon_id'], product['flipkart_id'], product['name'], area.find('img','s-image'), area.find('span', 'a-offscreen'), product['flipkart_area'].find('div', '_30jeq3 _1_WHN1'), datetime.datetime.utcnow())
                    # else:
                    #     # update if date is new
                    #     dateIsNew = db.session.query(exists().where(Product.date.date()==datetime.datetime.utcnow().date())).scalar()
                    #     print('date is new: ', dateIsNew)
                    #     if (dateIsNew):
                    #         updateToSql(product['amazon_id'], product['flipkart_id'], product['name'], area.find('img','s-image'), area.find('span', 'a-offscreen'), product['flipkart_area'].find('div', '_30jeq3 _1_WHN1'), datetime.datetime.utcnow())

                    # redis_client.set("data", json.dumps(product))
                    # redisData = redis_client.get("data")
                    # print('redis data: ', redisData)


                    for area in flipkart_search_area:
                        if (area.find('div', {'data-id': product['flipkart_id']})):
                            # flipkart_area_list.append(area)
                            # product.update({'flipkart_area': flipkart_area_list})
                            product['flipkart_price'] = area.find('div', '_30jeq3 _1_WHN1').text
                            print('------------------------- before product exists')
                            productExists = db.session.query(exists().where(Product.amazon_id==product['amazon_id'])).scalar()
                            # prodCount = db.session.query(Product).filter(Product.amazon_id==product['amazon_id']).count()
                            print('---------------------------- product exists: ', productExists)
                            if (not productExists):
                                # Add amazon products to db
                                addToSql(product['amazon_id'], product['flipkart_id'], product['name'], product['image_url'], product['amazon_price'], product['flipkart_price'], product['date'])
                            else:
                                # update if date is new
                                dateIsNew = db.session.query(exists().where(Product.date==datetime.datetime.utcnow().date())).scalar()
                                print('date is new: ', dateIsNew)
                                if (dateIsNew):
                                    updateToSql(product['amazon_id'], product['flipkart_id'], product['name'], product['image_url'], product['amazon_price'], product['flipkart_price'], product['date'])

                            break
                    break
        redis_client.set("products", json.dumps(products_arr))
        redis_client.set("syncDate", json.dumps(datetime.datetime.utcnow(), default=str))
        products_arr = json.loads(redis_client.get("products"))
        print('products: ', products_arr)
        syncDate = json.loads(redis_client.get("syncDate"), object_hook=datetime_parser)
        print('sync date: ', syncDate)
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
    return render_template("products.html", products = products_arr)

@app.route('/history/<product>')
def history(product):
    print('product: ', product)
    return render_template("history.html", data=product)