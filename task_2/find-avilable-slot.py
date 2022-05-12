import numpy as np
from time_slot import Calendar
from formatter import load_in, date_to_str
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--calendars")
    parser.add_argument("--duration-in-minutes")
    parser.add_argument("--minimum-people")
    args = parser.parse_args()
    config = vars(args)
    path_dict = str(config['calendars'])
    duration_in_minutes = int(config['duration_in_minutes'])
    minimum_people = int(config['minimum_people'])

    calendar = load_in(path_dict[1:])
    # print(calendar)

    # now = np.datetime64('now')
    now = np.datetime64('2022-07-01 09:00:00')

    solution = date_to_str(calendar.find_available_slot(duration_in_minutes, minimum_people, now))
    print(solution)

if __name__ == '__main__':
    main()