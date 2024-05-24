from typing import TypeVar, Generic
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class Success(Generic[T]):
    value: T

    @property
    def message(self):
        pass

    @property
    def is_success(self):
        return True


@dataclass
class Failure:
    message: str

    @property
    def value(self):
        pass

    @property
    def is_success(self):
        return False


Result = Success[T] | Failure


def success(value: T) -> Result[T]:
    return Success(value)


def failure(message: str) -> Result[None]:
    return Failure(message)
