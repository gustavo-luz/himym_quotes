from email.quoprimime import quote
import flask
from flask import Flask,send_file,send_from_directory
import select_quote
from jinja2.utils import markupsafe
markupsafe.Markup()
import subprocess
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time
#from flask_apscheduler import APScheduler
import datetime

# pip install flask-rest-jsonapi flask-sqlalchemy 
# pip install APScheduler==3.3.1

def get_quote():
    
    p = subprocess.check_output(['python', 'select_quote.py'])
    p = p.decode('utf-8')
    #print(p)
    
    return p

#quote = get_quote()
scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")
# Runs from Monday to Friday at 5:30 (am)
scheduler.add_job(
    func=get_quote,
    trigger="cron",
    max_instances=1,
    day_of_week='mon-fri',
    hour=15,
    minute=13,
    second=30
)

sched = BackgroundScheduler(daemon=True)
sched.add_job(get_quote,'interval',minutes=1)

#quote1 = get_quote()
app = Flask(__name__)

#app.config["CLIENT_CSV"] = "E:/AudiotoText/Flask_File_Downloads/filedownload/files/csv"



         



scheduler.start()

#print(scheduler)

@app.route('/')

def example():  

    
    #print(type(quote))
    #quote_ = list(quote.keys())[0]
    #char_ = list(quote.values())[0]
    #post_ = f'{{"{quote_}":"{char_}"}}'
    
    i = 0
    i = i + 1
    try:
        if i < 30:
            pass
        else:
            quote1 = get_quote()
        return quote1
    except:
        pass
    #t0 = time.time()
    #print(f'quote1: yayy {quote1}')
    #return quote1
    #if get_quote() == quote1:
    #    return quote1
    #else:
    
    #t1 = time.time()
    #total = t1 - t0

    #if total < 

    
    #print(get_quote())
    #return quote1
    #return post_
    #return '{"name":"Bob"}'

if __name__ == '__main__':
    #schedule.every(1).minutes.do(get_quote)
    #quote = get_quote()
    sched.start()
    time.sleep(1)
    app.run()
