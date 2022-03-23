from tempfile import TemporaryFile
import os
import unittest
import tasks

def test_listing_tasks():

    tasks.create("Hi", filename="tests.csv")
    tasks.create("Hello World", filename="tests.csv")
    with TemporaryFile("w+") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()
    os.remove("tests.csv")

    assert contents == ["Hi\n", "Hello World\n"]


def test_raise_exception_when_completed(monkeypatch):

    tasks.create("Hi", filename="tests.csv")
    tasks.create("Hello World", filename="tests.csv")

    monkeypatch.setattr('builtins.input', lambda _: "1")

    tasks.complete(filename="tests.csv")

    with TemporaryFile("w+") as stdout:
        tasks.complete(stdout=stdout, filename="tests.csv")
        stdout.seek(0)
        contents = stdout.readlines()

    os.remove("tests.csv")

    assert contents == ["This task has been completed, please try another one"]
