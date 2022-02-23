import os

import tasks


def test_listing_tasks():
    """
    Creating 2 tasks, then listing tasks shows the 2 created tasks.
    """

    tasks.create("Do laundry", filename="tests.csv")
    tasks.create("Clean up", filename="tests.csv")
    with open("stdout.txt", "w") as stdout:
        tasks.list(stdout=stdout, filename="tests.csv")
    with open("stdout.txt") as stdout:
        assert stdout.readlines() == ["Do laundry ✅\n", "Clean up ✅\n"]
    os.remove("tests.csv")
    os.remove("stdout.txt")