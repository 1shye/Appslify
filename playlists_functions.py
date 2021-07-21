import requests
import config
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.DEBUG, filename=config.FILE_NAME, format=config.LOGS_FORMAT, )


def fetch_playlists_data(retry=1):
    """
    returns playlists dictionary from configs url. Performs 3 attempts
    :param retry: The number of attempts to receive a response
    :return: playlists json received from API
    """
    try:
        response = requests.get(config.PLAYLISTS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"playlists fetching failed, error: {e}")
        logging.info(f"trying to fetch playlists again (attempt #{retry + 1})")
        if retry < config.MAX_RETRIES:
            time.sleep(5)
            return fetch_playlists_data(retry + 1)
        else:
            logging.error("max retries of playlists fetching - connection refused")


def parse_playlists_dates(playlists_data_json):
    """
    the function parses the dates from the playlists
    :param playlists_data_json: a dictionary that contains dates as keys (string) and playlist values (array)
    :return: parsed dates of playlists to a datetime config's format
    """
    parsed_dates = []
    for key in playlists_data_json:
        try:
            parsed_dates.append(parse_string_to_date(key))
        except ValueError as e:
            logging.error(e)
            pass

    return parsed_dates


def parse_string_to_date(date):
    """
    Desc: the function parses date in string form and turns it into a datetime object
    :param date: string that present date in config's format
    :return: parsed date to a datetime format
    """
    return datetime.strptime(date, config.DATE_FORMAT)


# Desc: the function returns the daily playlist by searching for the current date on the playlist
# if today's date cannot be found, the closest date will be returned
def get_daily_playlist():
    """

    :return: daily playlist by searching for the current date on the playlist
    if today's date cannot be found, the closest date will be returned as a array
    """
    playlists_data = fetch_playlists_data()
    now = datetime.now().strftime(config.DATE_FORMAT)
    playlists_dates = playlists_data.keys()
    for date in playlists_dates:
        if now == date:
            return playlists_data[date]

    logging.info("there is no playlist today")
    latest_playlist = get_latest_date_string(playlists_data)
    return playlists_data[latest_playlist]


# Desc: the function shuffles the playlist
# Input: playlist
# Output: shuffled playlist
def shuffle(original_playlist):
    """
    the function shuffles the playlist
    :param original_playlist: playlists array
    :return: shuffled playlist array
    """
    temp_playlist = original_playlist.copy()
    shuffled_playlist = []

    while len(temp_playlist) > 0:
        random_number = int(datetime.now().timestamp() * 1000000)
        index_to_pop = random_number % len(temp_playlist)
        shuffled_playlist.append(temp_playlist.pop(index_to_pop))

    return shuffled_playlist


# Desc: the functions gets a playlist's date and finds the latest date
# Input : playlists
# Output : closest dated playlist
def get_latest_date_string(playlists_data):
    """
    Desc: the functions gets a playlist's date and finds the latest date
    :param playlists_data: gets dictionary that contains dates keys (string) and playlists values (array)
    :return:  closest dated playlist as string
    """
    if playlists_data == {}:
        raise Exception("function get_latest_date_string received empty dict")
    now = datetime.now()
    latest_dates = [date for date in parse_playlists_dates(playlists_data) if date <= now]
    latest_date = max(latest_dates)

    return latest_date.strftime(config.DATE_FORMAT)

