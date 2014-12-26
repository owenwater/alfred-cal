#!/usr/bin/python
# encoding: utf-8

def get_default(d, key, default):
    if key not in d:
        d[key] = default
        return default
    else:
        return d[key]


