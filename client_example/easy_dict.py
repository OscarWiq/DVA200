# Author: Oscar

class EasyDict(UserDict):

    def __init__(self, mapping={}, normalize=False, **kwargs):
        self._normalize = normalize
        self.update(mapping)
        self.update(kwargs)

    @property
    def data(self):
        return self.__dict__

    def normalized(self, key):
        return key.replace(' ', '_') if self._normalize else key

    def __getitem__(self, key):
        return self.__dict__[self.normalized(key)]

    def __setitem__(self, key, value):
        self.__dict__[self.normalized(key)] = value
