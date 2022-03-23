#!/usr/bin/env python3
"""
A simple task manager.
For the purposes of our exercise we store tasks in a file which we'll
call tasks.csv (a CSV file). We'll talk more later about other ways to
store state which are more robust.
"""
from tempfile import NamedTemporaryFile
import datetime
import csv
import os
import sys
import pandas as pd

import collections

try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections

DONE = " ✅"


def list(stdout=sys.stdout, filename="tasks.csv"):
    """
    List the current known tasks.
    """

    with open(filename) as tasks_file:
        reader = csv.reader(tasks_file)
        for name,format_date,completed in reader:
            stdout.write(f"{name,format_date}{DONE if eval(completed) else ''}\n")


def create(name, filename="tasks.csv"):
    """
    Create a new task.
    """

    with open(filename, "a", newline="") as tasks_file:
        writer = csv.writer(tasks_file)
        print('Task successfully created. Please enter a date in the MM-DD-YY format:')
        strdate = input()
        format_date = datetime.datetime.strptime(strdate,'%m-%d-%Y')
        writer.writerow([name, format_date, False])


def complete(stdout=sys.stdout,filename="tasks.csv"):
    """
    Mark an existing task as completed.
    """

    with (
        open("tasks.csv") as tasks_file,
        NamedTemporaryFile("w", delete=False) as new,
    ):
        reader = csv.reader(tasks_file)
        print("Current tasks:")
        for id, (name, format_date, completed) in enumerate(reader):
            print(id+1, name, format_date, DONE if eval(completed) else '')

        to_complete = int(input("task ID?> "))
        writer = csv.writer(new,lineterminator="\n")
        tasks_file.seek(0)
        for id, (name, format_date, completed) in enumerate(reader):

            if id+1 == to_complete and eval(completed) == True:
                raise Exception("This task has been completed, please try another one")

            elif id+1 == to_complete:
                writer.writerow([name, format_date,True])
            else:
                writer.writerow([name, format_date,completed])

    os.remove(filename)
    os.rename(new.name, filename)


operations = dict(
    create=create,
    complete=complete,
    list=list,
)


def main():
    print("Enter a command [create, list, complete].")
    while True:
        line = input("-> ").strip()
        if not line:
            return

        operation, *args = line.split()
        fn = operations.get(operation)
        
        if operation == 'create':
            arg = " ".join([*args])
            fn(arg)
        else:
            fn(*args)


if __name__ == "__main__":
    main()