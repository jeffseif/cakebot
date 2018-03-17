import json


class JsonConfig:
    
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

    def to_dict(self):
        return {
            attr: getattr(self, attr)
            for attr in self.__slots__
        }


class Bot(JsonConfig):

    __slots__ = [
        'forwards',
        'listens',
        'nickname',
        'realname',
        'patterns',
    ]


class Swarm(JsonConfig):

    __slots__ = [
        'bots',
        'server',
        'ssl',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bots = []
        for nickname, params in kwargs['bots'].items():
            self.bots.append(Bot(nickname=nickname, **params))
