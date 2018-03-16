import json


class Config:
    
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    @classmethod
    def from_dict(cls, the_dict):
        return cls(**the_dict)

    @classmethod
    def from_json_path(cls, json_path):
        with open(json_path, 'rb') as f:
            return cls.from_dict(json.load(f))
