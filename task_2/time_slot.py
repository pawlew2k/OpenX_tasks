import numpy as np

class Period:
    def __init__(self, person: str, start: np.datetime64, end: np.datetime64 = None):
        self.person = person
        self.start = np.datetime64(start, 's')
        if end is None:
            self.end = self.start + np.timedelta64(1, 'D') - np.timedelta64(1, 's')
        else:
            self.end = np.datetime64(end, 's')

    def __str__(self):
        return f'(person={self.person}, start={str(self.start)}, end={str(self.end)})'


class Calendar:
    def __init__(self):
        self.times = dict()  # {np.datetime64: int}
        self.people = set()
        self.slots = dict()  # {str: np.datetime64}

    def __str__(self):
        return f'(people={self.people}\n' \
               + ' times=' + "\n       ".join(
                [date_to_str(time) + " : " + str(self.times[time]) for time in self.times.keys()]) + '\n' \
               + ' slots=' + "\n       ".join([str(person) +
                                               ": [" + ("\n          " + ' ' * len(person))
                                              .join(['[' + date_to_str(period[0]) + ", " + date_to_str(period[1]) + ']'
                                                     for period in self.slots[person]]) + "]"
                                               for person, slot in self.slots.items()]) + ')'

    def add_period(self, period: Period):
        self.times.extend([period.start, period.end])
        self.update_slot(period)

    def update_times(self, to_be_added=None, to_be_removed=None):
        if to_be_added is not None:
            for date in to_be_added:
                if date not in self.times.keys():
                    self.times[date] = 1
                else:
                    self.times[date] += 1

        if to_be_removed is not None:
            for date in to_be_removed:
                self.times[date] -= 1
                if self.times[date] == 0:
                    del self.times[date]

        self.times = dict(sorted(self.times.items(), key=lambda item: item[0]))

    def update_slot(self, period: Period):
        person = period.person
        start_date = period.start
        end_date = period.end
        if person not in self.slots.keys():
            self.people |= {person}
            self.people = set(sorted(self.people))
            self.slots[person] = np.array([[start_date, end_date]], dtype=np.datetime64)
            self.update_times(to_be_added=[start_date, end_date])
        else:
            slots = self.slots[person]
            new_period = [None, None]

            if end_date < slots[0][0]:
                new_period = [start_date, end_date]
                self.slots[person] = np.concatenate(([new_period], slots))
                self.update_times(to_be_added=new_period)

            elif start_date < slots[0][0]:
                idx2, str2 = self.binary_search_slot(slots, 0, len(slots) - 1, end_date)

                new_period[0] = start_date
                r = idx2

                if str2 == 'in':
                    new_period[1] = slots[idx2][1]
                elif str2 == 'out':
                    new_period[1] = end_date

                self.slots[person] = np.concatenate(([new_period], slots[r + 1:]))
                self.update_times(to_be_added=new_period, to_be_removed=slots[:r + 1].flatten())
            else:
                idx1, str1 = self.binary_search_slot(slots, 0, len(slots) - 1, start_date)
                idx2, str2 = self.binary_search_slot(slots, 0, len(slots) - 1, end_date)

                if not (idx1 == idx2 and str1 == str2 == 'in'):
                    if str1 == 'in':
                        new_period[0] = slots[idx1][0]
                    elif str1 == 'out':
                        new_period[0] = start_date

                    if str2 == 'in':
                        new_period[1] = slots[idx2][1]
                    elif str2 == 'out':
                        new_period[1] = end_date

                    l = idx1
                    if str1 == 'out':
                        l += 1
                    r = idx2

                    self.slots[person] = np.concatenate((slots[:l], [new_period], slots[r + 1:]))
                    to_be_removed = slots[l + 1:r + 1].flatten()
                    self.update_times(to_be_added=new_period, to_be_removed=to_be_removed)

    @staticmethod
    def binary_search_slot(slot, left: int, right: int, date: np.datetime64) -> int:
        mid = (left + right) // 2

        if left == right:
            if date <= slot[mid][1]:
                return mid, 'in'
            else:
                return mid, 'out'

        if slot[mid][0] <= date <= slot[mid][1]:
            return mid, 'in'
        elif slot[mid][1] < date < slot[mid + 1][0]:
            return mid, 'out'
        elif date < slot[mid][0]:
            return binary_search_slot(slot, left, mid - 1, date)
        elif slot[mid + 1][0] <= date:
            return binary_search_slot(slot, mid + 1, right, date)

    def binary_search_time(self, date_list: list, left: int, right: int, time: np.datetime64) -> int:
        if time < date_list[0]: return -1

        mid = (left + right + 1) // 2
        if left == right:
            return mid

        if time < date_list[mid]:
            return self.binary_search_time(date_list, left, mid - 1, time)
        elif data_list[mid] <= time:
            return self.binary_search_time(date_list, mid, right, time)

    def find_available_slot(self, duration_in_minutes: int, minimum_people: int, now=np.datetime64('now')):
        delta_time = np.timedelta64(duration_in_minutes, 'm')
        date_list = list(self.times.keys())
        idx = self.binary_search_time(date_list, 0, len(date_list)-1, now)

        if idx == -1:
            if self.check_available_slot(now, delta_time, minimum_people):
                return str(now)
            else:
                idx += 1

        while idx < len(date_list):
            now = date_list[idx] + np.timedelta64(1, 's')
            if self.check_available_slot(now, delta_time, minimum_people):
                return now
            idx += 1
        return now

    def check_available_slot(self, now, delta_time, minimum_people):
        num_people = 0
        for person in self.people:
            if self.check_available_for_person(person, now, delta_time):
                num_people += 1
                if num_people >= minimum_people:
                    return True

    def check_available_for_person(self, person, now, delta_time):
        for slot in self.slots[person]:
            start_date, end_date = slot
            if start_date <= now and now + delta_time <= end_date:
                return False
            for date in [start_date, end_date]:
                if now < date <= now + delta_time:
                    return False
        return True

def date_to_str(date: np.datetime64):
    return str(np.datetime64(date)).replace("T", " ")