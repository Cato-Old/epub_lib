import os
import sys

from app.domain import Book
from app.settings import Settings


def main() -> None:
    input_path = sys.argv[1]
    Settings(base_path=os.path.dirname(__file__))
    Book(input_path).dump()
