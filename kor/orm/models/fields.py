import attr
import enum
import datetime


def Field(*args, default=attr.NOTHING, **kwargs):
    if callable(default):
        default = attr.Factory(default)

    return attr.ib(*args, default=default, **kwargs)


def CharFieldValidator(*args):
    if not isinstance(args[-1], str):
        raise Exception('expected class<str> but got ' + str(type(args[-1])))


def CharField(*args, default=attr.NOTHING, **kwargs):
    if callable(default):
        default = attr.Factory(default)
    if default != attr.NOTHING:
        if not isinstance(default, str):
            raise ValueError
    kwargs['validator'] = CharFieldValidator
    return attr.ib(*args, default=default, **kwargs)


def EnumFieldValidator(*args):
    if not isinstance(args[-1], enum.Enum):
        raise Exception("expected class<'Enum'> but got " + str(type(args[-1])))


def EnumField(*args, **kwargs):
    metadata = {
        'related': {
            'target': args[0],
            'type': 'EnumClass',
        }
    }

    kwargs['validator'] = EnumFieldValidator
    return attr.ib(*args, metadata=metadata, **kwargs)


def IntegerFieldValidator(*args):
    if not isinstance(args[-1], int):
        raise Exception("expected class<'int'> but got " + str(type(args[-1])))


def IntegerField(*args, default=attr.NOTHING, **kwargs):
    if callable(default):
        default = attr.Factory(default)
    if default != attr.NOTHING:
        if not isinstance(default, int):
            raise ValueError
    kwargs['validator'] = IntegerFieldValidator
    return attr.ib(*args, default=default, **kwargs)


def FloatFieldValidator(*args):
    if not isinstance(args[-1], float):
        raise Exception("expected class<'float'> but got " + str(type(args[-1])))


def FloatField(*args, default=attr.NOTHING, **kwargs):
    if callable(default):
        default = attr.Factory(default)
    if default != attr.NOTHING:
        if not isinstance(default, float):
            raise ValueError
    kwargs['validator'] = FloatFieldValidator
    return attr.ib(*args, default=default, **kwargs)


def UUIDField(*args, default=attr.NOTHING, **kwargs):
    return attr.ib(*args, default=default, **kwargs)


def ArrayField(*args, **kwargs):
    return attr.ib(*args, **kwargs)


def DateTimeFieldValidator(*args):
    if not isinstance(args[-1], datetime.date):
        raise Exception("expected class<'datetime.date'> but got " + str(type(args[-1])))


def DateTimeField(*args, **kwargs):
    kwargs['validator'] = DateTimeFieldValidator
    return attr.ib(*args, **kwargs)


def ForeignKey(*args, **kwargs):
    metadata = {
        'related': {
            'target': args[0],
            'type': 'ForeignKey',
        }
    }

    return attr.ib(*args, metadata=metadata, **kwargs)
