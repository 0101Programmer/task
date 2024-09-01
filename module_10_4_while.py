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
        random_number = random.randint(0, 1)
        time.sleep(random_number)


class Cafe:
    def __init__(self, *tables_in_func):
        self.q = queue.Queue()
        self.tables_in_func = tables_in_func

    def guest_arrival(self, *guests_in_func):
        guests_list = []
        table_list = []
        stop_list = []
        wait_list = []
        g_ind = 0
        t_ind = 0
        for table in self.tables_in_func:
            table_list.append(table)
        for guest in guests_in_func:
            guests_list.append(guest)
        while table_list[t_ind].guest is None:
            table_list[t_ind].guest = guests_list[g_ind]
            stop_list.append(guests_list[g_ind])
            print(f'{guests_list[g_ind].name} сел за стол номер {table_list[t_ind].num}')
            guests_list[g_ind].start()
            guests_list[g_ind].join()
            if t_ind < len(table_list) - 1 and g_ind < len(guests_list) - 1:
                t_ind += 1
                g_ind += 1
        for table in self.tables_in_func:
            if table is not None:
                for guest in guests_in_func:
                    if guest not in stop_list and guest not in wait_list:
                        self.q.put(guest)
                        wait_list.append(guest)
                        print(f'{guest.name} в очереди')

    def guests_service(self):
        dismiss_list = []
        while self.q.empty() is False:
            for table in self.tables_in_func:
                if table.guest is not None:
                    if Guest.is_alive(table.guest) is False:
                        print(f'{table.guest.name} поел(-а) и ушёл(ушла). \nСтол {table.num} свободен')
                        dismiss_list.append(table.guest)
                        table.guest = None
                while table.guest is None:
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
