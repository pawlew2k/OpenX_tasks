### Finding available slot in calendar

#### Script printing solution:
```
syntax:
    $ python3 find-available-slot.py --calendars <path> --duration-in-minutes <int> --minimum-people <int>

example:
    $ python3 find-available-slot.py --calendars /in --duration-in-minutes 30 --minimum-people 2
```

#### Present time:
 solution take into consideration present time as `'2022-07-01 09:00:00'`

 you can easily change it on main() find-available-slot.py to present or chosen datetime
 
#### Calendar readable format:
you can also see object calendar structure created in main() find-available-slot.py `print(calendar)`

#### Calendar structure for given example:
```
(people={'alex', 'brian'}
 times=2022-07-01 00:00:00 : 1
       2022-07-01 23:59:59 : 1
       2022-07-02 00:00:00 : 1
       2022-07-02 12:59:59 : 1
       2022-07-02 13:15:00 : 1
       2022-07-02 13:59:59 : 1
 slots=alex: [[2022-07-02 13:15:00, 2022-07-02 13:59:59]]
       brian: [[2022-07-01 00:00:00, 2022-07-01 23:59:59]
               [2022-07-02 00:00:00, 2022-07-02 12:59:59]])
```

structure clearly shows how the information about calendar is stored

this structure is easily expandable with new additional datetime slots from people

the algorithm is resistant to overlapping occupied slots of the times for individual people
