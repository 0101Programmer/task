import random
import time
from threading import Thread
import queue


class Table:
    def __init__(self, num, guest=None):
        self.num = num
        self.guest = guest


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        random_number = random.randint(1, 3)
        time.sleep(random_number)


class Cafe:
    def __init__(self, *tables_in_func):
        self.q = queue.Queue()
        self.tables_in_func = tables_in_func

    def guest_arrival(self, *guests_in_func):
        stop_list = []
        table_list = []
        wait_list = []
        for table in self.tables_in_func:
            for guest in guests_in_func:
                if table.guest is None:
                    if guest not in stop_list and table not in table_list:
                        table.guest = guest
                        print(f'{guest.name} сел за стол номер {table.num}')
                        guest.start()
                        guest.join()
                        stop_list.append(guest)
                        table_list.append(table)
                        continue
                elif table.guest is not None and guest not in stop_list and guest not in wait_list:
                    self.q.put(guest)
                    wait_list.append(guest)
                    print(f'{guest.name} в очереди')
                    random_number = random.randint(5, 8)
                    time.sleep(random_number)

    def guests_service(self):
        dismiss_list = []
        while self.q.empty() is False:
            for table in self.tables_in_func:
                if table.guest is not None:
                    if Guest.is_alive(table.guest) is False:
                        print(f'{table.guest.name} поел(-а) и ушёл(ушла). \nСтол {table.num} свободен')
                        dismiss_list.append(table.guest)
                        table.guest = None
                        random_number = random.randint(4, 6)
                        time.sleep(random_number)
                elif table.guest is None:
                    guest = self.q.get()
                    if guest not in dismiss_list:
                        table.guest = guest
                        print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.num}')
                        guest.start()
                        guest.join()


tables = [Table(number) for number in range(1, 6)]
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.guests_service()
