import os
import uuid
import argparse
import sys
import paramiko
import time
import getpass
import subprocess
import argparse
import configparser
import sqlite3
from sqlite3 import Error

config = configparser.ConfigParser()
config.read('config.ini')

user = config['connection']['user']
passw = config['connection']['password']

IPsave = "iptables-save > /root/dsl.fw" #IPsave
IPflush = "iptables -F" #IPflush
#IPme = "iptables -A INPUT -p tcp -s 104.192.81.103 -j ACCEPT"
#IPme1 = "iptables -A OUTPUT -p tcp -d  104.192.81.103 -j ACCEPT" 
IPme = "iptables -A OUTPUT -p tcp -d  184.145.41.139 -j ACCEPT" #IPme
IPme1 = "iptables -A INPUT -p tcp -s 184.145.41.139 -j ACCEPT" #IPme1
IPallowSSH = "iptables -A INPUT  -p tcp -s 192.168.89.4 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT" #IPallowSSH
IPallowSSH1 = "iptables -A OUTPUT -p tcp -d 192.168.89.4 --sport 22 -m state --state ESTABLISHED -j ACCEPT" #IPallowSSH1
IPdropicmp = "iptables -A OUTPUT -p ICMP -j DROP" 
IPdropicmp1 = "iptables -A INPUT -p ICMP -j DROP"
IPrestore = "iptables -F \n ls -l \n sleep 5 \n  /sbin/iptables-restore < /root/dsl.fw " #IPrestore
NotificationCMD = "wall -n \"HOST QUARANTINED,  Contact IT, DO NOT REBOOT\""
IPdrop = "iptables -A INPUT -j DROP"
IPforward = "iptables -A FORWARD -j DROP"
IPdrop1 = "iptables -A OUTPUT -j DROP"


# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)

#     return conn
# def create_table(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)

def contain(victim):
        print(victim)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(victim, port=port, username=user, password=passw)
        stdin, stdout, stderr = ssh.exec_command(IPsave)
        stdin, stdout, stderr = ssh.exec_command(IPflush)
        stdin, stdout, stderr = ssh.exec_command(IPme1)
        stdin, stdout, stderr = ssh.exec_command(IPme)
        stdin, stdout, stderr = ssh.exec_command(IPallowSSH)
        stdin, stdout, stderr = ssh.exec_command(IPallowSSH1)
        stdin, stdout, stderr = ssh.exec_command(NotificationCMD)
        stdin, stdout, stderr = ssh.exec_command(IPdrop)
        stdin, stdout, stderr = ssh.exec_command(IPdrop1)
        ssh.close()

def uncontain(victim):
        print(victim)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(victim, port=port, username=user, password=passw)
        stdin, stdout, stderr = ssh.exec_command("IPtables -F")
        stdin, stdout, stderr = ssh.exec_command(IPrestore)
        ssh.close()

# def main():
#     database = r"data.db" 
#     sql_create_table = """ CREATE TABLE IF NOT EXISTS incident (
#                                         id int,
#                                         incident_open boolean default 0,
#                                         IP text,
#                                         mac text,
#                                         source text,
#                                         contained boolean default 0,
#                                         time_contained text,
#                                         forensic text,
#                                         foresnic_timestamp text,
#                                         closed_notes text,
#                                         first_seen_year text,
#                                         allowed boolean default 0,
#                                         fp_notes text
#                                     ); """
#     conn = create_connection(database)
#     if conn is not None:
#         create_table(conn, sql_create_table)
#     else:
#         cursor = conn.cursor()
#     dp = conn.cursor()
#     dp.execute("SELECT * FROM incident where id= 96") #Hard coded a value for testing, this will be fed by a different tool later
#     rows = dp.fetchone()
#     status = rows[6]
#     if status == 0:
#         victim = rows[3]
#         contain(victim)
#         conn.execute("""Update incident set contained = ? where id = ?""", ["1",96])
#         conn.commit()
#     else:
#         victim = rows[3]
#         uncontain(victim)
#         conn.execute("""Update incident set contained = ? where id = ?""", ["0",96])
#         conn.commit()
# main()





