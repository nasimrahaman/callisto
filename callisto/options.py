from copy import deepcopy
from contextlib import contextmanager


class Opt(object):
    PRIVATE_ATTRS = {'_scope'}

    def __init__(self):
        self.__dict__['_scope'] = ''

    def __getattr__(self, item):
        if item in Opt.PRIVATE_ATTRS:
            return object.__getattribute__(self, item)
        assert isinstance(item, str)
        item = item.lower()
        scoped_item = self._scope + '/' + item
        if scoped_item not in self.__dict__:
            raise AttributeError(f"Attribute '{item}' is not available under the "
                                 f"scope '{self._scope}'.")
        return self.__dict__[scoped_item]

    def __setattr__(self, key, value):
        if key in Opt.PRIVATE_ATTRS:
            raise KeyError("Trying to overwrite a private item. Use Opt.__dict__ if you know "
                           "what you're doing.")
        assert isinstance(key, str)
        self.__dict__[self._scope + '/' + key.lower()] = value

    def clone(self, **new_attrs):
        new = deepcopy(self)
        for key, value in new_attrs.items():
            new.__setattr__(key, value)
        return new

    def __repr__(self):
        repr_list = ['Opt(\n']
        for key, val in self.__dict__.items():
            if key in self.PRIVATE_ATTRS:
                continue
            repr_list.append(f'  {key.upper().strip("/")} = {val}\n')
        repr_list.append(')')
        return ''.join(repr_list)

    @contextmanager
    def for_function(self, name):
        # Set the scope
        current_scope = self._scope
        self.__dict__['_scope'] = name
        yield
        self.__dict__['_scope'] = current_scope


if __name__ == '__main__':
    opt = Opt()
    with opt.for_function('foo'):
        opt.POWER = 10
        opt.RANGERS = 20
    # print(opt.POWER)
    with opt.for_function('foo'):
        print(opt.POWER)
    # print(opt)
