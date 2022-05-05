Cron jobs -


Root-

* /opt/lampp/lampp startmysql && /opt/lampp/lampp startapache


Normal-

* env -i bash -c 'export WORKON_HOME=~/.virtualenvs && source /usr/local/bin/virtualenvwrapper.sh && workon env && cd /home/stonex//Desktop/Training/flask_ecommerce/flaskr && flask fetchtoredis >>scheduled.log 2>&1'
