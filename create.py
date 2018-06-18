#!/usr/bin/env python3

"""
Title:      Host Collection Database Creator
Author:     Jason Scott
Email:      jgs85@protonmail.com
Version:    1.0
Date:       10 Jun 2018

PEP 8 COMPLIANT
"""


# IMPORTS
import csv
import pymysql

# VARIABLES
host = 'localhost'
user = 'host'
passwd = '1qazxsw2'
db = 'host_collection'
netstat_states = {'LISTENING': 'Accepting connections',
                  'ESTABLISHED': 'Connection up and passing data',
                  'SYN_SENT': 'TCP; session has been requested by us; waiting for reply from remote endpoint',
                  'SYN_RECV': 'TCP; session has been requested by a remote endpoint for a socket on which we were '
                  'listening',
                  'LAST_ACK': 'TCP; our socket is closed; remote endpoint has also shut down; we are waiting for a '
                  'final acknowledgement',
                  'CLOSE_WAIT': 'TCP; remote endpoint has shut down; the kernel is waiting for the application to '
                  'close the socket',
                  'TIME_WAIT': 'TCP; socket is waiting after closing for any packets left on the network',
                  'CLOSED': 'Socket is not being used',
                  'CLOSING': 'TCP; our socket is shut down; remote endpoint is shut down; not all data has been sent',
                  'FIN_WAIT1': 'TCP; our socket has closed; we are in the process of tearing down the connection',
                  'FIN_WAIT2': 'TCP; the connection has been closed; our socket is waiting for the remote endpoint '
                  'to shut down',
                  '': 'Null Output'
                  }


# FUNCTIONS
def create_tables():
    cur = conn.cursor()

    # Create the 'users' table
    sql_create = "CREATE TABLE computers ( computerID int(11) NOT NULL AUTO_INCREMENT, computer_name varchar(255), " \
                 "PRIMARY KEY (computerID));" \
                 "CREATE TABLE users ( userID int(11) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, account_" \
                 "type varchar(255), disabled boolean, install_date varchar(255), local_account boolean, " \
                 "password_expires boolean, password_required boolean, computerID int(11) NOT NULL, PRIMARY KEY " \
                 "(userID), CONSTRAINT fk_users_1 FOREIGN KEY (computerID) REFERENCES computers (computerID));" \
                 "CREATE TABLE shares ( shareID int(11) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, " \
                 "share_path varchar(1024), description varchar(255), status varchar(255), computerID int(11) NOT " \
                 "NULL, PRIMARY KEY (shareID), CONSTRAINT fk_shares_1 FOREIGN KEY (computerID) REFERENCES computers " \
                 "(computerID));" \
                 "CREATE TABLE processes ( processID int(11) NOT NULL AUTO_INCREMENT, process_id int(11) NOT NULL, " \
                 "name varchar(255) NOT NULL, " \
                 "exec_path varchar(255), command_line varchar(1024), creation_date varchar(255), sha1 varchar(40), " \
                 "sha256 varchar (64), sha512 varchar(128), computerID int(11) NOT NULL, PRIMARY KEY (processID), " \
                 "CONSTRAINT fk_processes_1 FOREIGN KEY (computerID) REFERENCES computers (computerID));" \
                 "CREATE TABLE child_processes ( childID int(11) NOT NULL AUTO_INCREMENT, processID int(11) NOT " \
                 "NULL, computerID int(11) NOT NULL, PRIMARY KEY (childID), CONSTRAINT fk_child_processes_1 FOREIGN " \
                 "KEY (processID) REFERENCES processes (processID) CONSTRAINT fk_child_processes_2 FOREIGN KEY " \
                 "(computerID) REFERENCES computers (computerID));" \
                 "CREATE TABLE services ( serviceID int(11) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, " \
                 "description varchar(2048), command_line varchar(1024), exec_path varchar(1024), processID int(11) " \
                 "NOT NULL, started boolean, delayed_auto_start boolean, sha1 varchar(40), sha256 varchar(64), " \
                 "sha512 varchar(128), computerID int(11) NOT NULL, PRIMARY KEY (serviceID), CONSTRAINT " \
                 "fk_services_1 FOREIGN KEY (processID) REFERENCES processes (processID), CONSTRAINT fk_services_2 " \
                 "FOREIGN KEY (computerID) REFERENCES computer (computerID));" \
                 "CREATE TABLE netstat_states ( netstat_stateID int(11) NOT NULL AUTO_INCREMENT, net_state " \
                 "varchar(100) NOT NULL, description varchar(1024), PRIMARY KEY (netstat_stateID));" \
                 "CREATE TABLE netstat ( netID int(11) NOT NULL AUTO_INCREMENT, protocol varchar(3) NOT NULL, " \
                 "local_address varchar(255), local_port int(5), remote_address varchar(255), remote_port int(5), " \
                 "netstat_stateID int(11) NOT NULL, processID int(11) NOT NULL, computerID int(11) NOT NULL, " \
                 "PRIMARY KEY (netID), CONSTRAINT fk_netstat_1 FOREIGN KEY (netstat_stateID) REFERENCES " \
                 "netstat_states (netstat_stateID), CONSTRAINT fk_netstat_2 FOREIGN KEY (processID) REFERENCES " \
                 "processes (processID), CONSTRAINT fk_netstat_3 FOREIGN KEY (computerID) REFERENCES computers " \
                 "(computerID));" \
                 "CREATE TABLE groups ( groupID int(11) NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL, " \
                 "description varchar(1024), local_account boolean, install_date varchar(255), sid varchar(255), " \
                 "status varchar(255), computerID int(11) NOT NULL, PRIMARY KEY (groupID), CONSTRAINT " \
                 "fk_groups_1 FOREIGN KEY (computerID) REFERENCES computers (computerID));" \
                 "CREATE TABLE group_membership ( group_membershipID int(11) NOT NULL AUTO_INCREMENT, groupID " \
                 "int(11) NOT NULL, userID int(11) NOT NULL, group_type varchar(255), computerID int(11) NOT NULL, " \
                 "PRIMARY KEY (group_membershipID), CONSTRAINT fk_group_membership_1 FOREIGN KEY (groupID) " \
                 "REFERENCES groups (groupID), CONSTRAINT fk_group_membership_2 FOREIGN KEY (userID) REFERENCES " \
                 "users (userID), CONSTRAINT fk_group_membership_3 FOREIGN KEY (computerID) REFERENCES computers " \
                 "(computerID));" \
                 "CREATE TABLE autoruns ( autorunID int(11) NOT NULL AUTO_INCREMENT, entry_location varchar(1024), " \
                 "entry varchar(255), enabled varchar(255), category varchar(255), profile varchar(255), " \
                 "description varchar(1024), company varchar(255), image_path varchar(255), version varchar(255), " \
                 "launch_string varchar(1024), sha1 varchar(40), sha256 varchar(64), sha512 varchar(128), " \
                 "computerID int(11) NOT NULL, PRIMARY KEY (autorunID), CONSTRAINT fk_autoruns_1 FOREIGN KEY " \
                 "(computerID) REFERENCES computers (computerID));" \
                 "CREATE TABLE dir_walk (pathID int(11) NOT NULL AUTO_INCREMENT, filepath varchar(1024) NOT NULL, " \
                 "computerID int(11), PRIMARY KEY (pathID), CONSTRAINT fk_dirwalk_1 FOREIGN KEY (computerID) " \
                 "REFERENCES computers (computerID));" \
                 "CREATE TABLE usb_keys (usbID int(11) NOT NULL AUTO_INCREMENT, name varchar(255), serial_num " \
                 "varchar(255), description varchar(255), service varchar(255), PRIMARY KEY (usbID));"

    print(sql_create)
    # cur.execute(sql_create)
    # conn.commit()


def insert_netstat_states():    # Populate the 'netstat_states' table with each type of connection state
    cur = conn.cursor()

    for i in netstat_states.keys():
        sql_insert = "INSERT INTO netstat_states (name, description) VALUES ('{}', '{}');".format(
            i, netstat_states.get(i)
        )

        cur.execute(sql_insert)
        conn.commit()


def import_csv(table, csv_path, fields, values):
    cur = conn.cursor()

    with open(csv_path) as csvfile:
        a = csv.DictReader(csvfile)
        for row in a:
            sql = 'INSERT INTO {} {} VALUES {};'.format(table, fields, values)
            print(sql)
            # cur.execute(sql)
    # conn.commit()
    cur.close()


# MAINLOOP
conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
# create_tables()
insert_netstat_states()

conn.close()