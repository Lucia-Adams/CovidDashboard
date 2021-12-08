""" Update and Alarm Handler Module contains functions that process the alarms and updates

Functions:
update_handler, user_remove_updates, completed_alarms, daily_update

"""
import logging
import sched
from typing import Optional
from covid_data_handler import *
from covid_news_handling import *


def update_handler(r_parameters, u_list: list, d_sched , n_sched) -> Optional[dict]:
    """
    Takes in arguments from url and returns details to add to an update list
    details. Includes the title, content parameters , whether it repeats and the event
    Schedules these updates.

    Keyword arguments:
    r_parameters (ImmutableMultiDict) : parameters from url as returned by request.args
    u_list (list) : current update list to check if there is an alarm with that name already.
    d_sched (sched.scheduler) : the scheduler instance corresponding to the data updates
    n_sched (sched.scheduler) : the scheduler instance corresponding to the news updates

    Returns:
    update_detail (dict) : dictionary with details of the update
    or None

    """

    url_update_time = r_parameters.get("update")
    url_update_name = r_parameters.get("two")
    url_update_repeat = r_parameters.get("repeat")
    url_update_data = r_parameters.get("covid-data")
    url_update_news = r_parameters.get("news")
    url_update_repeat = r_parameters.get("repeat")

    boolean_repeat = False
    if url_update_repeat:
        boolean_repeat = True

    # create dictionary to return
    # pass in paramaters so we have them if we need to reschedule the event
    update_detail = {
    'title':url_update_name,
    'parameters':r_parameters,
    'repeat':boolean_repeat,
    }

    if url_update_time:

        for alarm in u_list:
            if alarm['title'] == url_update_name:
                logging.info('Attempt to add alarm with same name')
                return None

        logging.info('Alarm added')

        alarm_content = ""

        delay_time = update_delay(url_update_time)

        if url_update_data:
            data_event = schedule_covid_updates(delay_time,d_sched)
            alarm_content = f"Update data | {url_update_time}"
            update_detail['data-event'] = data_event

        if url_update_news:
            news_event = update_news(delay_time,n_sched)
            alarm_content = f"Update news | {url_update_time}"
            update_detail['news-event'] = news_event

        if url_update_data and url_update_news:
            alarm_content = f"Update news and data | {url_update_time}"
            update_detail['data-event'] = data_event
            update_detail['news-event'] = news_event

        # if not said whether to update news or data cancel update - invalid
        if alarm_content == "":
            return None

        if boolean_repeat:
            alarm_content += " | repeat"

        #adds content to dictionary
        update_detail['content'] = alarm_content

        return update_detail

def user_remove_updates(r_parameters , u_list: list, d_sched, n_sched) -> Optional[dict]:
    """
    Checks if there is a user request to delete an alarm. Removes the alarm from the
    scheduler queues. Returns the update dictionary to be removed.


    Keyword arguments:
    r_parameters (ImmutableMultiDict) : parameters from url as returned by request.args
    u_list (list) : current update list to check if there is an alarm with that name already.
    d_sched (sched.scheduler) : the scheduler instance corresponding to the data updates
    n_sched (sched.scheduler) : the scheduler instance corresponding to the news updates

    Returns:
    update_to_remove (dict) : the update dictionary to delete / remove from update list
    or None

    """

    update_to_remove = None

    update_delete = r_parameters.get("update_item")
    if update_delete:

        # stores events to be deleted
        d_event_remove = None
        n_event_remove = None

        # go through update list and remove update with that title
        for update in u_list:
            if update['title'] == update_delete:
                # get event to remove from scheduler

                if 'data-event' in list(update.keys()):
                    d_event_remove = update['data-event']

                if 'news-event' in list(update.keys()):
                    n_event_remove = update['news-event']

                update_to_remove = update

        if d_event_remove:
            try:
                d_sched.cancel(d_event_remove)
                logging.info('Cancelled data update')
            except:
                logging.warning('Value error. Tried to remove non existent event')
        if n_event_remove:
            try:
                n_sched.cancel(n_event_remove)
                logging.info('Cancelled news update')
            except:
                logging.warning('Value error. Tried to remove non existent event')

    return update_to_remove

def completed_alarms(u_list : list, d_sched, n_sched) -> tuple[Optional[dict],Optional[any]]:

    """
    Checks if any alrams have elapsed. If it repeats, return the original paramters (so it can be
    rescheduled)
    Returns the update dictionary to be removed if an alarm has elapsed.

    Keyword arguments:
    u_list (list) : current update list to check if there is an alarm with that name already.
    d_sched (sched.scheduler) : the scheduler instance corresponding to the data updates
    n_sched (sched.scheduler) : the scheduler instance corresponding to the news updates

    Returns:
    event_to_remove (dict) : the update dictionary to delete / remove from update list
    repeat_params (ImmutableMultiDict) : original parameters of alarm to repeat from url as returned by request.args

    """

    event_to_remove = None
    repeat_params = None
    data_queue = d_sched.queue
    news_queue = n_sched.queue

    for update in u_list:
        repeat = update['repeat']

        #  for data events:
        if 'data-event' in list(update.keys()):

            data_event = update['data-event']
            # if event not in queue ie completed
            if data_event not in data_queue:
                # remove the update from sidebar/update list
                event_to_remove = update
                logging.info('Data update complete')

                if repeat:
                    repeat_params = update['parameters']
                    logging.info('Repeating alarm')

        # for news events. If both news and data it will be caught only in top conditional
        elif 'news-event' in list(update.keys()):

            news_event = update['news-event']
            # if event not in queue ie completed
            if news_event not in news_queue:
                # remove the update from sidebar/update list
                event_to_remove = update
                logging.info('News update complete')

                if repeat:
                    repeat_params = update['parameters']
                    logging.info('Repeating alarm')

    return event_to_remove, repeat_params

def daily_update(daily_event_list: list, d_sched, n_sched):
    """
    Takes list holding 24 hour update events.
    If the data event is no longer in the queue, reschedule news and data events and return the events
    (to be added to list outside of function)
    If events still in queue ie haven't elapsed, the function returns None as no new event

    Keyword arguments:
    daily_event_list (list) : list containing event instance corresponding to 24 hour updates
    d_sched (sched.scheduler) : the scheduler instance corresponding to the data updates
    n_sched (sched.scheduler) : the scheduler instance corresponding to the news updates

    Returns:
    daily_data_update (sched.scheduler) : the new data event instance for the 24 hour update
    daily_news_update (sched.scheduler) : the new news event instance for the 24 hour update

    """
    data_queue = d_sched.queue

    if daily_event_list[0] not in data_queue :
        # then also won't have one in news queue
        daily_data_update = schedule_covid_updates(24*60*60,d_sched)
        daily_news_update = update_news(24*60*60,n_sched)

        logging.info('Added alarm for 24 hours time')

    else:
        return None, None

    return daily_data_update, daily_news_update
