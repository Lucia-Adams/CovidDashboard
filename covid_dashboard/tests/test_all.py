"""Testing of scheduling and additional functionality

Functions:
test_data_schedule_update, test_news_schedule_update, test_cut_article, test_completed_alarms
"""

import sched
import time
from covid_data_handler import schedule_covid_updates
from covid_news_handling import update_news
from covid_news_handling import cut_article

from update_and_alarm_handler import completed_alarms

def test_data_schedule_update() -> None:
    """Test: schedules a data update. Expected result is that an update is scheduled
    and displayed in the log.
    """
    test_sched = sched.scheduler(time.time, time.sleep)
    schedule_covid_updates(update_interval=10, update_name=test_sched)
    test_sched.run(blocking=False)

def test_news_schedule_update() -> None:
    """Test: schedules a news update. Expected result is that an update is scheduled
    and displayed in the log. """
    test_sched = sched.scheduler(time.time, time.sleep)
    update_news(update_interval=10, update_name=test_sched)
    test_sched.run(blocking=False)

def test_cut_article() -> None:
    """Test: checks whether the function cut_article takes the first 25 words of a string """

    test_content = "This is a test article to check if it will cut off the article at " \
    "25 words or not. It should cut off at the end of this sentence."
    expected_content = "This is a test article to check if it will cut off the article at " \
    "25 words or not. It should cut off at the"
    assert cut_article(test_content) == expected_content

def test_completed_alarms() -> None:
    """Test: Tests that if no event in update list, completed_alarms returns (None,None)"""
    test_data_sched = sched.scheduler(time.time, time.sleep)
    test_news_sched = sched.scheduler(time.time, time.sleep)
    test_event_list = []
    assert completed_alarms(test_event_list, test_data_sched, test_news_sched) == (None,None)
