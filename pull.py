#!/usr/bin/env python3

"""
Title:      Host Collection Aggregator
Author:     Jason Scott
Email:      jgs85@protonmail.com
Version:    1.0
Date:       10 Jun 2018

PEP 8 COMPLIANT
"""

# IMPORTS
import csv
import sys
import os
import pymysql
import pycol as p


# VARIABLES
host = 'localhost'
user = 'host'
passwd = '1qazxsw2'
db = 'host_collection'


# FUNCTIONS

# Function: import_csv(table, csv_path)
# Usage: Used to import generic csv into host_collection database.  'table' is a table name, and 'csv_path' is the
#        path to csv file.
# Issues: Applies all values as strings, which is problematic and causes import failures
def import_csv(table, csv_path):
    cur = conn.cursor()
    file = open(csv_path, 'r')
    csv_data = csv.reader(file)

    a = [row for row in csv_data][1:]
    print(a)

    for i in range(0, len(a)):
        sql = "INSERT INTO {} {} VALUES ({});".format(
            table,
            get_fields(table),
            str(a[i]).replace('[', '').replace(']', '')
        )
        print(sql)

    # for row in csv_data:
    #     cur.execute('INSERT INTO {} {} VALUES {};'.format())

    # conn.commit()
    cur.close()
    file.close()


# Function: get_computerID(computer_name)
# Usage: Retrieves the computerID from the 'computers' table when passed a computer name.
# Issues:
def get_id(table, field, value):
    cur = conn.cursor()
    sql = "SELECT {} FROM {} WHERE name = '{}';".format(field, table, value)

    cur.execute(sql)
    a = cur.fetchone()
    conn.commit()

    return a[0]


def get_query(qry):
    cur = conn.cursor()
    cur.execute(qry)
    a = cur.fetchall()
    conn.commit()

    return a


# Function: import_all()
# Usage: Used to import each unique csv for host collection.
# Issues: This function is not flexible and imports must strictly adhere to specific csv and table formatting
def import_all():

    csv_folder = sys.argv[1]

    if sys.argv[1][-1:] != '/':
        csv_folder = sys.argv[1] + '/'

    msg = 'This script will import all CSVs from each subdirectory within {}. Are you sure you want to import from' \
          ' this folder? (y/n)  '.format(p.col('p', csv_folder))
    cur = conn.cursor()
    response = str.lower(input(msg))

    # Function: get_list(n)
    # Usage: Used to return a list object containing each record in the given CSV "n"
    # Issues: Function needs to be pointed at actual collection folder
    def get_list(n):
        file = open(csv_folder + 'collection/{}.csv'.format(n), 'r') ### NEEDS TO BE CHANGED ###
        csv_data = csv.reader(file)
        a = [row for row in csv_data][1:]   # Returns a list object of all csv rows

        return a

    # Import Adapters
    def import_adapters():
        a = get_list('Adapters')

        for i in range(0, len(a)):
            sql = "INSERT INTO adapters {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', " \
                  "{});".format(
                    get_fields('adapters'),
                    str(a[i][0]),
                    str(a[i][1]),
                    str(a[i][2]),
                    str(a[i][3]),
                    str(a[i][4]),
                    str(a[i][5]),
                    str(a[i][6]),
                    str(a[i][7]),
                    a[i][8],
                    str(a[i][9]),
                    str(a[i][10]),
                    get_id('computers', 'computerID', str(a[i][11]))
                    )
            cur.execute(sql)
            conn.commit()

    def import_autoruns():
        a = get_list('AutoRuns')

        for i in range(0, len(a)):
            sql = "INSERT INTO autoruns {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
                  "'{}', '{}', '{}', {});".format(
                    get_fields('autoruns'),
                    str(a[i][1]).replace("'", "`"),
                    str(a[i][2]).replace("'", "`"),
                    str(a[i][3]).replace("'", "`"),
                    str(a[i][4]).replace("'", "`"),
                    str(a[i][5]).replace("'", "`"),
                    str(a[i][6]).replace("'", "`"),
                    str(a[i][7]).replace("'", "`"),
                    str(a[i][8]).replace("'", "`"),
                    str(a[i][9]).replace("'", "`"),
                    str(a[i][10]).replace("'", "`"),
                    str(a[i][11]).replace("'", "`"),
                    str(a[i][12]).replace("'", "`"),
                    str(a[i][13]).replace("'", "`"),
                    get_id('computers', 'computerID', str(a[i][14]))
                    )

            cur.execute(sql)
            conn.commit()


    def import_groups():
        a = get_list('Groups')

        for i in range(0, len(a)):
            sql = "INSERT INTO groups {} VALUES ('{}', '{}', {}, '{}', '{}', '{}', {});".format(
                get_fields('groups'),
                str(a[i][0]),
                str(a[i][1]),
                a[i][2],
                str(a[i][3]),
                str(a[i][4]),
                str(a[i][5]),
                get_id('computers', 'computerID', str(a[i][6]))
            )

            cur.execute(sql)
            conn.commit()

    def import_users():
        a = get_list('Users')

        for i in range(0, len(a)):
            sql = "INSERT INTO users {} VALUES ('{}', '{}', {}, '{}', {}, {}, {}, {});".format(
                get_fields('users'),
                str(a[i][0]),
                str(a[i][1]),
                a[i][2],
                str(a[i][3]),
                a[i][4],
                a[i][5],
                a[i][6],
                get_id('computers', 'computerID', str(a[i][7]))
            )
            cur.execute(sql)
            conn.commit()

    def import_group_membership():  # Function does NOT WORK due to mismatching collections
        a = get_list('GroupMemberShip')

        for i in range(0, len(a)):
            sql = "INSERT INTO group_membership {} VALUES ({}, {}, '{}', {});".format(
                get_fields('group_membership'),
                get_id('groups', 'groupID', str(a[i][0])),
                get_id('users', 'userID', str(a[i][1])),
                str(a[i][2]),
                get_id('computers', 'computerID', str(a[i][3]))
            )
            print(a[i][1])

    def import_processes():  # Function cannot parse asterisks and therefore does not return fill results; -1 !!
        a = get_list('ProcessInformation')

        for i in range(0, len(a)):
            sql = "INSERT INTO processes {} VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', {});".format(
                get_fields('processes'),   # Process fields
                a[i][1],    # Process_id
                str(a[i][2]),   # Process name
                str(a[i][3]),   # Exec path
                str(a[i][4]),   # Cmd line
                str(a[i][5]),   # Creation date
                str(a[i][6]),   # sha1
                str(a[i][7]),   # sha256
                str(a[i][8]),   # sha512
                get_id('computers', 'computerID', str(a[i][9]))  # Computer ID
            )

            cur.execute(sql)
            conn.commit()

    def import_netstat():
        a = get_list('Netstat')
        print(a)

        for i in range(0, len(a)):
            sql = "INSERT INTO netstat {} VALUES ('{}', '{}', {}, '{}', {}, {}, {}, {});".format(
                get_fields('netstat'),   # Netstat fields
                str(a[i][0]),   # Protocol
                str(a[i][1]).replace('*', '4815162342'),   # Local Address
                a[i][2],    # Local Port
                str(a[i][3]).replace('*', '4815162342'),   # Remote Address
                a[i][4].replace('*', '4815162342'),    # Local Port
                get_id('netstat_states', 'netstat_stateID', str(a[i][5])),  # Netstat State
                get_query('SELECT processID FROM processes WHERE process_id = {} AND computerID = {};'.format(
                    a[i][6],
                    get_id('computers', 'computerID', str(a[i][7]))
                ))[0][0],  # Process ID
                get_id('computers', 'computerID', str(a[i][7]))  # Computer ID
            )

            cur.execute(sql)
            conn.commit()

    def import_services():
        a = get_list('ServiceInformation')

        for i in range(0, len(a)):
            sql = "INSERT INTO services {} VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}', '{}', {});".format(
                get_fields('services'),
                str(a[i][0]),
                str(a[i][1]).replace("'", "`"),
                str(a[i][2]),
                str(a[i][3]),
                get_query('SELECT processID FROM processes WHERE process_id = {} AND computerID = {};'.format(
                    a[i][4],
                    get_id('computers', 'computerID', str(a[i][10]))
                ))[0][0],
                a[i][5],
                a[i][6],
                str(a[i][7]),
                str(a[i][8]),
                str(a[i][9]),
                get_id('computers', 'computerID', str(a[i][10]))
            )

            cur.execute(sql)
            conn.commit()

    def import_shares():
        a = get_list('Share')

        for i in range(0, len(a)):
            sql = "INSERT INTO shares {} VALUES ('{}', '{}', '{}', '{}', {});".format(
                get_fields('shares'),
                str(a[i][0]),
                str(a[i][1]).replace("\\", "\\\\"),
                str(a[i][2]),
                str(a[i][3]),
                get_id('computers', 'computerID', str(a[i][4]))
            )

            cur.execute(sql)
            conn.commit()

    def import_usb():
        a = get_list('USBKeys')

        for i in range(0, len(a)):
            sql = "INSERT INTO usb_keys {} VALUES ('{}', '{}', '{}', '{}', {});".format(
                get_fields('usb_keys'),
                str(a[i][0]),
                str(a[i][1]),
                str(a[i][2]),
                str(a[i][3]),
                get_id('computers', 'computerID', str(a[i][4]))
            )

            print(sql)

    if response == 'n':
        quit()

    elif response == 'y':
        #import_users()
        #import_groups()
        #import_adapters()
        #import_autoruns()
        #import_group_membership()
        #import_processes()
        #import_netstat()
        #import_services()
        #import_shares()
        import_usb()

        print(p.col('g2', 'Import Complete!'))

    else:
        print('Invalid option.')
        quit()


# Function: get_fields(table)
# Usage: Used to retrieve the fields of a database table
# Issues:
def get_fields(table):
    cur = conn.cursor()
    list_fields = list()
    sql = "SELECT COLUMN_NAME FROM information_schema. columns WHERE table_schema='host_collection' " \
          "AND table_name='{}';".format(table)

    cur.execute(sql)
    a = cur.fetchall()
    conn.commit()

    for i in range(1, len(a)):
        list_fields.append(a[i][0])

    return str(list_fields).replace('[', '(').replace(']', ')').replace("'", '')


# MAINLOOP
conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
# import_csv('adapters', '/home/syntax/host-db/collection/Adapters.csv')
import_all()

conn.close()
