from playlists_functions import *
import time


def play_daily_playlist():
    play_playlist = get_daily_playlist()
    for current_song in shuffle(play_playlist):
        print(f"Now playing -> {current_song}")
        time.sleep(1)


if __name__ == '__main__':
    while True:
        try:
            play_daily_playlist()
        except Exception as e:
            logging.error(e)