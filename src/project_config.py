import os


def get_postgres_uri():
    return os.getenv("DATABASE_URL")


TABLE_COUNT = int(os.getenv("TABLE_COUNT", 10))
SEAT_COUNT = int(os.getenv("SEAT_COUNT", 4))
SEAT_PRICE = int(os.getenv("SEAT_PRICE", 50))
RUNNING_TESTS = os.getenv("RUNNING_TESTS", "FALSE")
