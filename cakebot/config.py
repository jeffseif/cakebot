import json


class Config:

    __slots__ = [
        'forwards',
        'listens',
        'nick',
        'realname',
        'patterns',
        'server',
        'ssl',
    ]
    
    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs[attr])

    @classmethod
    def from_dict(cls, the_dict):
        return cls(**the_dict)

    @classmethod
    def from_json_path(cls, json_path):
        with open(json_path, 'rb') as f:
            return cls.from_dict(json.load(f))
