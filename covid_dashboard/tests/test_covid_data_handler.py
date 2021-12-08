"""Testing of data handling

Functions:
test_parse_csv_data, test_process_covid_csv_data, test_covid_API_request, test_schedule_covid_updates
"""

from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates

def test_parse_csv_data() -> None:
    """Checks function parse_csv_data interprets the correct number of lines from
    set file nation_2021-10-28.csv"""

    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data() -> None:
    """Checks function test_process_covid_csv_data calculates correct data from
    set file nation_2021-10-28.csv"""

    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request() -> None:
    """Checks if the data returned by covid_API_request is a dictionary"""

    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates() -> None:
    """Runs the schedule_covid_updates with parameters update_interval=10
     and update_name='update test' to check result """
    schedule_covid_updates(update_interval=10, update_name='update test')
