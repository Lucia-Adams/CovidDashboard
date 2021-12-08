"""Covid Data Handler Module contains functions that process data from the Covid19 API

Functions:
parse_csv_data, parse_json_data, process_covid_csv_data, covid_API_request, read_config
fetch_data, schedule_covid_updates, update_delay
"""
import sched
import json
import time
import logging
from uk_covid19 import Cov19API
import os

def parse_csv_data(csv_filename: str) -> list[str]:
    """
    Takes in covid data csv file and returns list of each row as a string
    Note: Returns the same data format as the parse_json_data function

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing covid data

    Returns:
    content (list) : Content of csv file as a list of strings for the rows in the file

    """

    with open(csv_filename,'r', encoding="utf-8") as file:
        content = file.read().splitlines()

    # removes any blank lines
    for row in content:
        if row == "":
            content.remove("")

    return content

def parse_json_data(covid_json: dict) -> list[str] :
    """
    Takes in covid data json file and returns list of each row as a string
    Note: Returns same data format as the parse_csv_data function

    Keyword arguments:
    covid_json (file.json) : Title of json file containing covid data

    Returns:
    data_list (list) : Content of json file as a list of strings for the rows in the file

    """

    data_list = []
    json_data = covid_json['data']
    for dict_item in json_data:
        row_list = list(dict_item.values())
        row_string = ",".join(str(x) for x in row_list)
        data_list.append(row_string)

    return data_list

def process_covid_csv_data(covid_csv_data: list[str]) -> tuple[int,int,int]:
    """
    Takes a list of covid data and returns the number of cases in the last 7 days,
    the current number of hospital cases and the cumulative number of deaths.

    Keyword arguments:
    covid_csv_data (list) : List of covid data as returned by parse_csv_data or parse_json_data

    Returns:
    last_7_days (int) : The number of cases in the last 7 days
    current_hospital_cases (int) : The current hospital cases in the last 7 days
    cumulative_deaths (int) : The cumulative number of deaths overall

    """

    days = 0
    last_7_days = 0
    current_hospital_cases = None
    cumulative_deaths = None

    # stores first entry of new deaths which is incomplete
    most_recent_hospital = None

    for item in covid_csv_data:
        item_list = item.split(',')

        # gets the first value of cumulative deaths in file
        if (item_list[5]).isnumeric() and current_hospital_cases is None:
            current_hospital_cases = int(item_list[5])

        # goes through each row until it finds a number in cummulaive deaths row
        if (item_list[4]).isnumeric() and cumulative_deaths is None:
            cumulative_deaths = int(item_list[4])

        # finds numeric entries for new cases and adds them up for 8 days
        if (item_list[6]).isnumeric() and days < 8:

            if most_recent_hospital is None:
                most_recent_hospital = int(item_list[6])

            last_7_days += int(item_list[6])
            days += 1

    # removes first incomplete entry from total
    if last_7_days is not None and most_recent_hospital is not None:
        last_7_days -= most_recent_hospital

    return last_7_days, current_hospital_cases, cumulative_deaths

def covid_API_request(location: str ="Exeter", location_type: str="ltla") -> dict :
    """
    Returns up to date Covid data from API as a json dictionary

    Keyword arguments:
    location (str) : Local region or country eg/ Exeter, London, England. Default at 'Exeter'
    location_type (str) : Area type eg/ nation, region, ltla. Default at 'ltla'

    Returns:
    d_dict (dictionary) : Returns dictionary of covid data as returned by the Cov19API (in json format)

    """

    filter_list = [ f"areaType={location_type}", f"areaName={location}"]

    cases_and_deaths_metrics = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate":"cumDailyNsoDeathsByDeathDate",
    "hospitalCases":"hospitalCases",
    "newCasesBySpecimenDate":"newCasesBySpecimenDate"
    }

    api = Cov19API(filters=filter_list, structure=cases_and_deaths_metrics)
    data = api.get_json(as_string=True)
    d_dict = json.loads(data)

    if d_dict['data'] == []:
        logging.warning(f"No data available for '{location}'. Try another name. ")

    return d_dict

def read_config(json_file: str) -> tuple[str,str,str,str]:
    """
    Reads data from a given json configuration file

    Keyword arguments:
    json_file (file.json) : Name of config file

    Returns:
    nation (str) : Nation as contained in config file
    local (str) : Local region as contained in config file
    api_key (str) : API key for news as contained in config file
    search_terms (str) : Words to search for in the News API

    """

    this_directory = os.path.dirname(__file__)
    path = this_directory + '/'+ json_file

    with open(path,'r',encoding="utf-8") as data_f:
        config_data = json.load(data_f)

        nation = config_data["NATION"]
        local = config_data["LOCAL"]
        api_key = config_data["NEWS_API_KEY"]
        search_terms = config_data["SEARCH_TERMS"]

    return nation, local, api_key, search_terms

def fetch_data(nation: str="England",local: str="Exeter") -> None:
    """
    Fetches covid data from covid19 API for both national and local region.
    Writes the relevent data to a covid_data.json file.
    The data contains the local region, local 7 day infection rate, the national region,
    the national 7 day infection rate, the national hospital cases and the national
    death total.

    Keyword arguments:
    nation (str) : Nation to fetch data for. Default at 'England'
    local (str) : Local region to fetch data for. Default at 'Exeter'

    Returns:
    None

    """

    national_json = covid_API_request(nation,"nation")
    national_json_list= parse_json_data(national_json)
    national_7_days,national_h_cases,national_t_deaths = process_covid_csv_data(national_json_list)

    local_json = covid_API_request(local)
    local_json_list = parse_json_data(local_json)
    local_7_days = process_covid_csv_data(local_json_list)[0]

    with open("covid_data.json","w",encoding="utf-8") as data_f:
        data_dict = {
        'location' : local,
        'local_7day_infections': local_7_days,
        'nation_location': nation,
        'national_7day_infections': national_7_days,
        'hospital_cases': ("Hospital cases: " + str(national_h_cases)),
        'deaths_total': ("Death total: " + str(national_t_deaths)),
        }
        json.dump(data_dict,data_f)

    logging.info('Updated the covid data json')

def schedule_covid_updates(update_interval: int, update_name: sched.scheduler) -> sched.Event:
    """
    Reads config file and updates covid_data.json with covid data after a given
    time interval. Queues event to a given scheduler instance.
    (Schedules fetch_data to occur after a given time interval)

    Keyword arguments:
    update_interval (int) : interval time until update in seconds
    update_name (sched.scheduler) : scheduler name as in sched.scheduler

    Returns:
    data_event (sched.Event) : Event as returned by scheduler module

    """
    nation = read_config("config.json")[0]
    local = read_config("config.json")[1]

    try:
        data_event = update_name.enter(update_interval,1,fetch_data,(nation,local))
        logging.info("Event added to data scheduler")
        return data_event

    except:
        logging.debug("Incorrect parameters. Update name takes scheduler instance")

def update_delay(alarm_time: str) -> int:
    """
    Take an alarm time and calculates the time interval between the current time and
    the alarm time

    Keyword arguments:
    alarm_time (string) : Time of alarm in hh:mm as fetched from parameters in url

    Returns:
    delay (int) : time in seconds between current time and time of alarm

    """

    alarm_seconds = (int(alarm_time[0:2]) *60*60) + (int(alarm_time[3:5])*60)
    ct_seconds = ((time.gmtime().tm_hour)*60*60)+((time.gmtime().tm_min)*60)+ time.gmtime().tm_sec

    if ct_seconds > alarm_seconds :
        delay = (24*60*60) - ct_seconds + alarm_seconds
    else:
        delay = alarm_seconds - ct_seconds

    return delay
