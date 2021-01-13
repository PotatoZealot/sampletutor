from random import randrange
import random
import namegenerator
import sqlite3

class corp:
    def __init__(self, name, rank, occupation, slave, min_work):
        self.name = name
        self.rank = rank
        self.occupation = occupation
        self.slave = slave
        self.min_work = min_work
    workres = 0

    def work(self):
        self.workres = self.workres + randrange(100)
        print( ''.join(self.name), "Worked for: " + str(self.workres) + "%")


boss = []
directors = []
managers = []
slaves = []
occupation_slaves = ['Driver', 'Cleaner', 'Carpenter', 'Spy', 'Netrunner', 'Privateer']
occupation_manager = ['Finance', 'Logistics', 'Sales', 'Innovation', 'Negotiations', 'QA', 'Counterintel']
occupation_director_avalibe = ['Finance', 'Logistics', 'Sales', 'Innovation', 'Negotiations', 'QA', 'Counterintel']
occupation_director_occupied = []

fin_mgrs = []
log_mgrs = []
sal_mgrs = []
inn_mgrs = []
neg_mgrs = []
qna_mgrs = []
cou_mgrs = []

x_slaves = 10
x_managers = 21
x_directors = 7
x_boss = 1

manager_count_fin = 0
manager_count_log = 0
manager_count_sal = 0
manager_count_inn = 0
manager_count_neg = 0
manager_count_qna = 0
manager_count_cou = 0


def gen_mgr():
    global manager_count_fin
    global manager_count_log
    global manager_count_sal
    global manager_count_inn
    global manager_count_neg
    global manager_count_qna
    global manager_count_cou
    if manager_count_fin < 3:
        manager_count_fin += 1
        return 'Finance'
    if manager_count_log < 3:
        manager_count_log += 1

        return 'Logistics'
    if manager_count_sal < 3:
        manager_count_sal += 1

        return 'Sales'
    if manager_count_inn < 3:
        manager_count_inn += 1

        return 'Innovation'
    if manager_count_neg < 3:
        manager_count_neg += 1

        return 'Negotiations'
    if manager_count_qna < 3:
        manager_count_qna += 1

        return 'QA'
    if manager_count_cou < 3:
        manager_count_cou += 1
        return 'Counterintel'


def gen_dir():
    rng = random.choice(occupation_director_avalibe)
    if rng == 'Finance':
        occupation_director_avalibe.remove('Finance')
        occupation_director_occupied.append('Finance')
        return rng
    if rng == 'Logistics':
        occupation_director_avalibe.remove('Logistics')
        occupation_director_occupied.append('Logistics')
        return rng
    if rng == 'Sales':
        occupation_director_avalibe.remove('Sales')
        occupation_director_occupied.append('Sales')
        return rng
    if rng == 'Innovation':
        occupation_director_avalibe.remove('Innovation')
        occupation_director_occupied.append('Innovation')
        return rng
    if rng == 'Negotiations':
        occupation_director_avalibe.remove('Negotiations')
        occupation_director_occupied.append('Negotiations')
        return rng
    if rng == 'QA':
        occupation_director_avalibe.remove('QA')
        occupation_director_occupied.append('QA')
        return rng
    if rng == 'Counterintel':
        occupation_director_avalibe.remove('Counterintel')
        occupation_director_occupied.append('Counterintel')
        return rng


while len(slaves) < x_slaves:
    slaves.append(corp(str((namegenerator.gen()).title().split('-')), 4, list(set(random.choices(occupation_slaves, k=3))), None, randrange(80, 100)))
while len(managers) < x_managers:
    managers.append(corp(str((namegenerator.gen()).title().split('-')), 3, gen_mgr(), random.choices(slaves, k=1), randrange(70, 100)))
while len(directors) < x_directors:
    directors.append(corp(str((namegenerator.gen()).title().split('-')), 2, gen_dir(), [], randrange(50, 100)))
while len(boss) < x_boss:
    boss.append(corp(str((namegenerator.gen()).title().split('-')), 1, 'Boss', directors, randrange(100)))

for i in directors:
    for j in managers:
        if i.occupation == j.occupation:
            i.slave.append(j)

for i in slaves:
    i.work()
for i in managers:
    i.work()
for i in directors:
    i.work()
for i in boss:
    i.work()

conn = sqlite3.connect('roster.db')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Boss;
DROP TABLE IF EXISTS Directors;
DROP TABLE IF EXISTS Managers;
DROP TABLE IF EXISTS Slaves;

CREATE TABLE Boss (
    boss_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE, 
    rank INTEGER,
    occupation TEXT,
    slave TEXT,
    min_work INTEGER,
    workres INTEGER
);

CREATE TABLE Directors (
    director_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE,
    rank INTEGER,
    occupation TEXT,
    slave TEXT,
    min_work INTEGER,
    workres INTEGER
);

CREATE TABLE Managers (
    manager_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE,
    rank INTEGER,
    occupation TEXT,
    slave TEXT,
    min_work INTEGER,
    workres INTEGER
);

CREATE TABLE Slaves (
    slave_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    rank TEXT,
    occupation TEXT,
    min_work TEXT,
    workres TEXT
)
''')




for i in slaves:
    name = i.name
    rank = i.rank
    occupation = ' '.join(i.occupation)
    slave = i.slave
    min_work = i.min_work
    workres = i.workres

    cur.execute('''INSERT INTO Slaves (name, rank, occupation, min_work, workres)
        VALUES ( ?, ?, ?, ?, ? )''', (name, rank, occupation, min_work, workres))

for i in managers:
    name = i.name
    rank = i.rank
    occupation = ' '.join(i.occupation)
    slave = str(i.slave)
    min_work = i.min_work
    workres = i.workres

    cur.execute('''INSERT INTO Managers (name, rank, occupation, slave, min_work, workres)
        VALUES ( ?, ?, ?, ?, ?, ? )''', (name, rank, occupation, slave, min_work, workres))

for i in directors:
    name = i.name
    rank = i.rank
    occupation = ' '.join(i.occupation)
    slave = str(i.slave)
    min_work = i.min_work
    workres = i.workres

    cur.execute('''INSERT INTO Directors (name, rank, occupation, slave, min_work, workres)
        VALUES ( ?, ?, ?, ?, ?, ? )''', (name, rank, occupation, slave, min_work, workres))

for i in boss:
    name = i.name
    rank = i.rank
    occupation = ' '.join(i.occupation)
    slave = str(i.slave)
    min_work = i.min_work
    workres = i.workres

    cur.execute('''INSERT INTO Boss (name, rank, occupation, slave, min_work, workres)
        VALUES ( ?, ?, ?, ?, ?, ? )''', (name, rank, occupation, slave, min_work, workres))
conn.commit()