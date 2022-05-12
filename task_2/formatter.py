import numpy as np
from glob import glob
import os
from time_slot import Calendar, Period


def load_in(filename: str):
    directory_path = filename + '/*.txt'
    file_paths = glob(directory_path)
    calendar = Calendar()
    for file in file_paths:
        load_person(file, calendar)
    return calendar

def load_person(file_path: str, calendar: Calendar):
    person = os.path.split(file_path)[1][:-4]
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            times = line.split(' - ')
            match len(times):
                case 1:
                    start = np.datetime64(times[0][:-1], 's')
                    period = Period(person, start)
                    calendar.update_slot(period)
                case 2:
                    start = np.datetime64(times[0], 's')
                    end = np.datetime64(times[1], 's')
                    period = Period(person, start, end)
                    calendar.update_slot(period)

def date_to_str(date: np.datetime64):
    return str(np.datetime64(date)).replace("T", " ")
