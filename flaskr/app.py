import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import redis
import json
import urllib.parse
from  selenium import webdriver
from bs4 import BeautifulSoup
from sqlalchemy import exists
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import dateinfer
app = Flask(__name__)

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
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'OPPO A31 (Fantasy White, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444SXZ6',
        'flipkart_id': 'MOBFPBD6NMXDG6UM',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'Redmi 9 Activ (Coral Green, 4GB RAM, 64GB Storage)',
        'amazon_id': 'B09GFLFMPS',
        'flipkart_id': 'MOBG7FNG6HBQCPGY',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'OPPO A31 (Mystery Black, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444S68L',
        'flipkart_id': 'MOBFPBD6ZYTJUAXN',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'Samsung Galaxy M12 (Blue,4GB RAM, 64GB Storage)',
        'amazon_id': 'B08XGDN3TZ',
        'flipkart_id': 'MOBGFG8GCPEGKGF4',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'Lenovo IdeaPad 3',
        'amazon_id': 'B09MM4FPMR',
        'flipkart_id': 'COMG72M9XXDCHEQZ',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'HP 15- AMD Ryzen 3-3250',
        'amazon_id': 'B08T6THSMQ',
        'flipkart_id': 'COMFZHFWBE7APPH2',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'APPLE iPhone 13 Pro (Graphite, 128 GB)',
        'amazon_id': 'B09G91LWTZ',
        'flipkart_id': 'MOBG6VF5FYT935T7',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'APPLE 2020 Macbook Pro M1 - 8 GB/256 GB SSD',
        'amazon_id': 'B08N5WG761',
        'flipkart_id': 'COMFXEKMTGHAGSVX',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    },
    {
        'name': 'OnePlus Nord CE 2 5G (Bahamas Blue, 8GB RAM, 128GB Storage)',
        'amazon_id': 'B09RG5R5FG',
        'flipkart_id': 'MOBGDBYGG6PPNFD9',
        'amazon_price': '',
        'flipkart_price': '',
        'date': ''
    }
]

class Product(db.Model):
    amazon_id = db.Column(db.String(50), unique=True, primary_key=True, nullable=False)
    flipkart_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(50), nullable=False)
    amazon_price = db.Column(db.String(10), nullable=False)
    flipkart_price = db.Column(db.String(10), nullable=False)
    history = relationship("History", backref="product")

class History(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.amazon_id'), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    amazon_price = db.Column(db.String(10), nullable=False)
    flipkart_price = db.Column(db.String(10), nullable=False)

def addToSql(amazon_id, flipkart_id, name, image_url, amazon_price, flipkart_price):
    print('Adding data to sql...')
    product = db.session.query(Product).get(amazon_id) # will give you either Parent or None
    if (not product):
        print('Adding product: ', name)
        product = Product(
            amazon_id=amazon_id,
            flipkart_id=flipkart_id,
            name=name,
            image_url=image_url,
            amazon_price=amazon_price,
            flipkart_price=flipkart_price,
        )
        db.session.add(product)
    dateExists = db.session.query(History) \
    .filter(History.product_id == amazon_id) \
    .filter(db.extract('month', History.date) == datetime.datetime.today().month,
            db.extract('year', History.date) == datetime.datetime.today().year,
            db.extract('day', History.date) == datetime.datetime.today().day).first()
    
    if (not dateExists):
        print('Adding new date history for product: ', name)
        history = History(
            date=datetime.datetime.utcnow(),
            amazon_price=amazon_price,
            flipkart_price=flipkart_price,
            product=product
        )
        product.history.append(history)
        db.session.commit()

def readFromSql():
    pass

@app.cli.command()
def fetchToRedis():
    print('Cron job time - ', datetime.datetime.utcnow())
    # CRON jon function
    # If there's new day then fetch data from ecommerce websites to redis

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/stonex/Desktop/Training/chromedriver')

    # if current date data exists in redis than fetch from it else scrape new day data from ecommerce sites
    # syncDate = redis_client.get("syncDate")
    print('sync date: ', redis_client.get("syncDate").decode("utf-8"))
    print('format', dateinfer.infer([redis_client.get("syncDate").decode("utf-8")]))
    syncDate = datetime.datetime.strptime(json.loads(redis_client.get("syncDate")), '%Y-%m-%d %H:%M:%S.%f')
    print('Redis sync date: ', syncDate.date())
    print('Today: ', datetime.datetime.now())
    if (syncDate.date() != datetime.datetime.utcnow().date()):
        print('Fetching new day data to redis...')
        # Fetch data to redis
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
            url = 'https://www.fldatetime.datetime todayipkart.com/search?q='
            flipkart_search = search
            browserdriver.get(url+flipkart_search)
            content = browserdriver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            flipkart_search_area = soup.findAll('div', '_13oc-S')

            for area in amazon_search_area:
                if (area.attrs['data-asin'] == product['amazon_id']):
                    product['image_url'] = area.find('img', 's-image').attrs['src']
                    product['amazon_price'] = area.find('span', 'a-offscreen').text

                    for area in flipkart_search_area:
                        if (area.find('div', {'data-id': product['flipkart_id']})):
                            product['flipkart_price'] = area.find('div', '_30jeq3 _1_WHN1').text
                            productExists = db.session.query(exists().where(Product.amazon_id==product['amazon_id'])).scalar()

                            addToSql(product['amazon_id'], product['flipkart_id'], product['name'], product['image_url'], product['amazon_price'], product['flipkart_price'])

                            break
                    break
        redis_client.set("products", json.dumps(products_arr))
        redis_client.set("syncDate", json.dumps(datetime.datetime.utcnow(), default=str))
        products_arr = json.loads(redis_client.get("products"))
        syncDate = json.loads(redis_client.get("syncDate"))

@app.route('/')
def products():
    # Fetch from redis
    products_arr = json.loads(redis_client.get("products"))
    return render_template("products.html", products = products_arr)

@app.route('/history/<product_id>')
def history(product_id):
    product=None
    amazonProduct = False
    if (len(product_id) == 10):
        # its amazon id
        product = db.session.query(Product).where(Product.amazon_id == product_id).first().__dict__
        amazonProduct = True
    else:
        # its flipkart id
        # get amazon_id
        product = db.session.query(Product).where(Product.flipkart_id == product_id).first().__dict__
        product_id = product['amazon_id']
        print('flipkart product: ', product)
        amazonProduct = False
        
    # get product data from sql with amazon_id as product_id
    history_rows = db.session.query(History).filter(History.product_id == product_id).all()
    history = list(map(lambda row: row.__dict__, history_rows))
    return render_template("history.html", product=product, history=history, fromAmazon=amazonProduct)

    