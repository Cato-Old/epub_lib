import sys

from app.domain import Book


def main() -> None:
    input_path = sys.argv[1]
    Book(input_path).dump()
