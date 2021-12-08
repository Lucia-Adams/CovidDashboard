""" Covid News Handler Module contains functions that process news from the news API

Functions:
news_API_request, update_news, cut_article

"""
import json
import logging
import sched
import requests
from flask import Markup
from covid_data_handler import read_config


def news_API_request(covid_terms:str ="Covid COVID-19 coronavirus") -> list[dict]:
    """
    Fetches news from a news API using API key specified in the config file.
    Each article is processed as a dictionary containing its title, content and link.
    The article dictionaries are added to a list and the list is written to
    a json file covid_news.json with key news_articles.

    Keyword arguments:
    covid_terms (string) : Terms to search for. Default at 'Covid COVID-19 coronavirus'

    Returns:
    article_list (list) : A list of dictionaries with each dictionary being a news article.

    """
    key = read_config("config.json")[2]

    url = ('https://newsapi.org/v2/everything?'
       f'q={covid_terms}&'
       'from=2021-11-07&'
       'sortBy=popularity&'
       f'apiKey={key}')

    response = requests.get(url)
    response_json = response.json()
    articles = response_json['articles']
    article_list = []

    status = response_json['status']
    if status != 'ok':
        logging.warning(f'Response form news API is : {status}')

    for article in articles:

        a_url = article['url']
        content = cut_article(article['content']) + "..."
        content_with_link = content + "\n" + a_url

        a_dict = {
            'title': article['title'],
            'content': content,
            'link': a_url,
        }
        article_list.append(a_dict)

    # write news to a news file so it can be updated
    with open("covid_news.json","w", encoding="utf-8") as news_f:
        news_dict = {
        'news_articles' : article_list,
        }
        json.dump(news_dict,news_f)

    logging.info('Updated the covid news json')

    return article_list

def update_news(update_interval:int, update_name: sched.scheduler) -> sched.Event:
    """
    Updates covid_news.json with news after a given time interval.
    Queues event to a given scheduler instance.
    (Schedules news_API_request to occur after a given time interval)

    Keyword arguments:
    update_interval (int) : interval time until update in seconds
    update_name (sched.scheduler) : scheduler name as in sched.scheduler

    Returns:
    news_event (sched.Event) : Event as returned by scheduler module
    
    """
    search_terms = read_config("config.json")[3]

    try:
        news_event = update_name.enter(update_interval,1,news_API_request,(search_terms,))
        logging.info("Event added to news scheduler")
        return news_event

    except:
        logging.debug("Incorrect parameters. Update name takes scheduler instance")

def cut_article(article: str) -> str:
    """
    Takes an article and returns the first 25 words. If the article is less than 25
    words it returns the full original article.

    Keyword arguments:
    article (string) : The article to take in

    Returns:
    new_art (string) : The first 25 words of the article
    or article : Unmodified article

    """
    words = article.split(' ')
    if len(words) > 25:
        cut_art = words[0:25]
        new_art = " ".join(cut_art)
        return new_art
    else:
        return article
