import importlib


def get_cls_name(cls: type) -> str:
    return cls.__module__ + '.' + cls.__qualname__


def get_cls_from_name(cls_name: str) -> type:
    try:
        mod_path, name = cls_name.rsplit('.', 1)
        return getattr(importlib.import_module(mod_path), name)
    except ValueError:
        return getattr(importlib.import_module('__main__'), cls_name)
