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
        random_number = random.randint(3, 10)
        time.sleep(random_number)


class Cafe:
    def __init__(self, *tables_in_func):
        self.q = queue.Queue()
        self.tables_in_func = tables_in_func

    def guest_arrival(self, *guests_in_func):
        for guest in guests_in_func:
            for table in self.tables_in_func:
                if table.guest is None:
                    table.guest = guest
                    print(f'{guest.name} занял стол номер {table.num}')
                    guest.start()
                    random_number = random.randint(1, 2)
                    time.sleep(random_number)
                    break
            else:
                self.q.put(guest)
                print(f'{guest.name} в очереди')
                random_number = random.randint(2, 3)
                time.sleep(random_number)

    def guests_service(self):
        while self.q.empty() is False or any(table.guest for table in self.tables_in_func):
            for table in self.tables_in_func:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} поел(-а) и ушёл(ушла). \nСтол {table.num} свободен')
                    table.guest = None
                    random_number = random.randint(2, 4)
                    time.sleep(random_number)
                if not self.q.empty() and table.guest is None:
                    table.guest = self.q.get()
                    table.guest.start()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.num}')
                    random_number = random.randint(1, 2)
                    time.sleep(random_number)


tables = [Table(number) for number in range(1, 6)]
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.guests_service()
