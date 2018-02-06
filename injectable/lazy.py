from injectable import util


class Lazy:
    attributes = {}

    def __init__(self, reference, func_module):
        Lazy.attributes[self] = {
            '__lazy_reference__': reference,
            '__lazy_module__': func_module,
            '__lazy_instance__': None,
        }

    def __getattribute__(self, item):
        lazy_self = Lazy.attributes[self]
        Lazy.attributes_list = [
            '__lazy_reference__',
            '__lazy_module__',
            '__lazy_instance__',
        ]

        if item in Lazy.attributes_list:
            return lazy_self[item]

        if lazy_self['__lazy_instance__'] is None:
            class_reference = util.get_class(
                lazy_self['__lazy_reference__'], lazy_self['__lazy_module__'])
            lazy_self['__lazy_instance__'] = class_reference()

        instance = lazy_self['__lazy_instance__']
        return instance.__getattribute__(item)
