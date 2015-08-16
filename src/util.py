#!/usr/bin/python
# encoding: utf-8

def get_from_dict(dict, key, default_value):
    try: 
        return dict[key]
    except KeyError:
        dict[key] = default_value
        return default_value
        
