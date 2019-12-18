from __future__ import annotations

from typing import Type


def raise_exception(ex: Exception) -> None:
    raise ex


class Settings:
    _instance = None

    def __new__(cls: Type[Settings], *args, **kwargs) -> Settings:
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        for name, value in kwargs.items():
            ex = TypeError(f'{name} attribute cannot be assigned')
            setattr(self, f'_{name}', value)
            setattr(self.__class__, name, property(
                lambda obj: getattr(obj, f'_{name}'),
                lambda obj, val: raise_exception(ex),
            ))

    @classmethod
    def clear(cls):
        cls._instance = None
        props = {k: v for k, v in vars(cls).items() if isinstance(v, property)}
        for name, value in props.items():
            delattr(cls, name)
