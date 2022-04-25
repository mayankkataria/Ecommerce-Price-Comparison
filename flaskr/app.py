from unicodedata import category
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# import redis
from  selenium import webdriver
from bs4 import BeautifulSoup
import datetime
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Arcgate1!@localhost/Ecommerce'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8080/Ecommerce'
db = SQLAlchemy(app)

PRODUCTS = [
    {
        'name': 'Vivo Y21T (Midnight Blue, 4GB RAM, 128GB ROM)',
        'amazon_id': 'B09Q5Z5M9D',
        'flipkart_id': 'MOBG5VFCSKRABKAM'
    },
    {
        'name': 'OPPO A31 (Fantasy White, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444SXZ6',
        'flipkart_id': 'MOBFPBD6NMXDG6UM'
    },
    {
        'name': 'Redmi 9 Activ (Coral Green, 4GB RAM, 64GB Storage)',
        'amazon_id': 'B09GFLFMPS',
        'flipkart_id': 'MOBG7FNG6HBQCPGY'
    },
    {
        'name': 'OPPO A31 (Mystery Black, 6GB RAM, 128GB Storage)',
        'amazon_id': 'B08444S68L',
        'flipkart_id': 'MOBFPBD6ZYTJUAXN'
    },
    {
        'name': 'Samsung Galaxy M12 (Blue,4GB RAM, 64GB Storage)',
        'amazon_id': 'B08XGDN3TZ',
        'flipkart_id': 'MOBGFG8GCPEGKGF4'
    },
    {
        'name': 'Lenovo IdeaPad 3',
        'amazon_id': 'B09MM4FPMR',
        'flipkart_id': 'COMG72M9XXDCHEQZ'
    },
    {
        'name': 'HP 15- AMD Ryzen 3-3250',
        'amazon_id': 'B08T6THSMQ',
        'flipkart_id': 'COMFZHFWBE7APPH2'
    },
    {
        'name': 'APPLE iPhone 13 Pro (Graphite, 128 GB)',
        'amazon_id': 'B09G91LWTZ',
        'flipkart_id': 'MOBG6VF5FYT935T7'
    },
    {
        'name': 'APPLE 2020 Macbook Pro M1 - 8 GB/256 GB SSD',
        'amazon_id': 'B08N5WG761',
        'flipkart_id': 'COMFXEKMTGHAGSVX'
    },
    {
        'name': 'OnePlus Nord CE 2 5G (Bahamas Blue, 8GB RAM, 128GB Storage)',
        'amazon_id': 'B09RG5R5FG',
        'flipkart_id': 'MOBGDBYGG6PPNFD9'
    },
]

# r = redis.StrictRedis(url='redis://:root.redislabs.com@:8085/Ecommerce')
class Product(db.Model):
    id = db.Column(db.String(50), unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(12), nullable=False)

@app.route('/')
def products():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/stonex/Desktop/Training/chromedriver')
    search = 'smartphone'
    
    ### ------------Scrape on amazon-------------- ###
    url = 'https://www.amazon.com/s?k='
    browserdriver.get(url+search)
    content = browserdriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    amazon_search_area = soup.findAll('div', 's-result-item')
    print('--------------------------------------area------------------------------------------: ', amazon_search_area)

    # Add amazon products to db
    product = Product(id="ID", name="Sample Product", image_url="sample_image_url", price="100", category='amazon', date=datetime.datetime.utcnow())
    db.session.add(product)
    db.session.commit()

    ### -----------Scrape on flipkart------------- ###
    url = 'https://www.flipkart.com/search?q='
    browserdriver.get(url+search)
    content = browserdriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    flipkart_search_area = soup.findAll('div', '_13oc-S')
    print('--------------------------------------area------------------------------------------: ', flipkart_search_area)

    return render_template("products.html", amazon_area=amazon_search_area, flipkart_area=flipkart_search_area)

@app.route('/history/<product>')
def history(product):
    print('product: ', product)
    return render_template("history.html", data=product)