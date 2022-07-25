# Ecommerce Price Comparison

## Overview

**Made with Flask and Bootstrap, used to compare prices of given products web scraped from Amazon and Flipkart with beautiful soup and selenium, implemented cron job to fetch daily and read/write from redis cache, price history was stored in mysql db**

### Setup Environment
- Navigate to ```flaskr``` directory
- Run ```pip install -r requirements.txt``` to install all required packages.
- Download chromedriver according to system's chrome version from [here](https://chromedriver.chromium.org/downloads)
- Copy chromedriver to ```flaskr``` directory

### Setup MySql
- Run ```mysql -u root -p``` and enter password as ```password``` if root user is logged in for first time. Else login by your own password.
- Create user with command ```CREATE USER 'username'@'localhost' IDENTIFIED BY 'Password1!';``` where ```username``` is username and ```Password1!``` is password which can be custom but must of have minimum 8 characters length, include both cases alphabets, at least one number and special character.
- Grant privileges with ```GRANT ALL PRIVILEGES ON  *.*  TO 'username'@'localhost'; ```
- Exit root user from mysql with ```exit```
- Relaunch mysql with newly created user by ```mysql -u username -p``` and password ```Password1!```
- Create database with command ```CREATE DATABASE Ecommerce;```
- Select database with ```use Ecommerce;```
- Create table ```product``` with below query-
```
CREATE TABLE product (
amazon_id varchar(50) PRIMARY KEY UNIQUE NOT NULL,
flipkart_id varchar(100) UNIQUE NOT NULL,
name varchar(100) NOT NULL,
image_url varchar(100) NOT NULL,
amazon_price varchar(10) NOT NULL,
flipkart_price varchar(10) NOT NULL
);
```
- Create table ```history``` with below query -
```
CREATE TABLE history (
id int UNIQUE PRIMARY KEY AUTO_INCREMENT,
product_id varchar(50) NOT NULL FOREIGN KEY REFERENCES product(amazon_id),
date varchar(12) NOT NULL,
amazon_price varchar(10) NOT NULL,
flipkart_price varchar(10) NOT NULL,
);
```

### Add a CRON job
Add a cron job to start mysql service, fetch data to redis db on daily basis and store the logs in scheduled.log file located in ```flaskr``` directory
- Execute ```crontab -e``` in terminal to open CRON script
- Add ```systemctl start mysql && fetchtoredis >>scheduled.log 2>&1``` in CRON script

### Launch app
- Launch app with ```flask run``` in ```flaskr``` directory

### Working Samples
[b735e646-6c97-4a6c-93fb-dfddf6b01430.webm](https://user-images.githubusercontent.com/52576282/180850093-b5b261dd-bd68-486a-82b7-17c82bd3eda7.webm)
