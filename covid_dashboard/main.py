"""This is the main module that renders the flask template and pulls the data to put in it"""

import time
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, render_template
from covid_data_handler import *
from covid_news_handling import *
from update_and_alarm_handler import *


# Logging - makes new log file every day in logs folder
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('logs/flask_server.log', when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# initialises variables and schedulers
app = Flask(__name__)

data_sched = sched.scheduler(time.time, time.sleep)
news_sched = sched.scheduler(time.time, time.sleep)

update_list = []
news_list = []
deleted_news_list = []

#fetch new data when first loaded
initial_data_fetch = schedule_covid_updates(0,data_sched)
initial_news_fetch = update_news(0,news_sched)

update_24_hours = [initial_data_fetch, initial_news_fetch]

data_sched.run(blocking=False)
news_sched.run(blocking=False)


@app.route("/index")
def run_index_page():
    """
    Runs the schedulers and pulls the covid data and news from APIs.
    It then renders the processed data in a flask template.
    Accessed at /index
    """

    logging.info('Page refreshed')

    data_sched.run(blocking=False)
    news_sched.run(blocking=False)

    r_param = request.args

    # checks if user has added an update
    update_details = update_handler(r_param,update_list,data_sched, news_sched)
    update_list.append(update_details) if update_details is not None else None

    # checks if user has removed any updates
    user_up_to_remove = user_remove_updates(r_param, update_list, data_sched, news_sched)
    update_list.remove(user_up_to_remove) if user_up_to_remove is not None else None

    # removes completed alarms and resechules repeating ones
    com_up_to_remove, repeat_parameters = completed_alarms(update_list, data_sched, news_sched)
    update_list.remove(com_up_to_remove) if com_up_to_remove is not None else None
    if repeat_parameters is not None:
        r_update_details = update_handler(repeat_parameters,update_list, data_sched, news_sched)
    else:
        r_update_details = None
    update_list.append(r_update_details) if r_update_details is not None else None

    update_dict = {'updates': update_list}

    # gets data from file covid_data.json
    with open("covid_data.json",'r', encoding="utf-8") as data_f:
        data_to_pass = json.load(data_f)

    # gets covid news and selects the first 5 that haven't been deleted.
    with open("covid_news.json",'r', encoding="utf-8") as news_f:

        news_count = 0

        news_to_delete = r_param.get('notif')
        if (news_to_delete is not None) and (news_to_delete not in deleted_news_list):
            logging.info('News article deleted')
            deleted_news_list.append(news_to_delete)

        news_list = (json.load(news_f))['news_articles']
        news_to_pass = []

        for article in news_list:
            if article['title'] not in deleted_news_list and news_count < 5:

                link_section = f"\n<a href=\'{article['link']}\'>link</a>"
                article['content'] = Markup(article['content'] + link_section)

                news_to_pass.append(article)
                news_count +=1

        news_dict_to_pass = {'news_articles': news_to_pass}

    daily_data_event, daily_news_event = daily_update(update_24_hours, data_sched, news_sched)

    if daily_data_event is not None:
        update_24_hours[0] = daily_data_event
        update_24_hours[1] = daily_news_event

    return render_template('index.html',
    title = "Covid Updates",
    image = "covid_map_logo.jpeg",
    **data_to_pass,
    **news_dict_to_pass,
    **update_dict)

if __name__ == '__main__':
    app.run()
