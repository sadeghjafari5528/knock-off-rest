import random
from collections import OrderedDict
from itertools import chain
from typing import Tuple, Optional as Maybe, Dict, Any, Iterable

from ..exceptions import DoesNotExist, MultipleObjectsReturned
from ..query.parser import Q
from ..utils import cmp, flatmap

from ..types import LookupParams, Fields


class QuerySet(list):
    def __init__(self, *args, model, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)
        self.model = model

    @property
    def _attrs(self):
        return self[0]._attrs if self.exists() else set()

    def __or__(self, other):
        return type(self)(chain(self, other), model=self.model).distinct('id')

    def count(self):
        return len(self)

    def delete(self):
        _len = self.count()
        _type = self.model.__name__

        for item in self:
            item.delete()

        return _len, {_type: _len}

    def reverse(self):
        return type(self)(
            reversed(self),
            model=self.model
        )

    def distinct(self, *fields: Fields):
        if not fields:
            fields = self._attrs - {'created', 'updated'}

        meta = [
            (cmp(*fields)(obj), obj)
            for obj in self.reverse()
        ]

        return type(self)(
            OrderedDict(meta).values(),
            model=self.model
        ).reverse()

    def earliest(self, field_name='created'):
        try:
            obj = self.filter(
                **{field_name + '__isnone': False}
            ).order_by(
                field_name
            )[0]
        except IndexError:
            return None
        else:
            return obj

    def exclude(self, *args, **kwargs):
        q = ~(Q.from_Qs(*args) & Q(**kwargs))

        return type(self)(
            filter(q.comparator, self),
            model=self.model
        )

    def exists(self):
        return bool(self)

    def filter(self, *args, **kwargs):
        q = Q.from_Qs(*args) & Q(**kwargs)

        return type(self)(
            filter(q.comparator, self),
            model=self.model
        )

    def first(self):
        try:
            obj = self[0]
        except IndexError:
            return None
        else:
            return obj

    def get(self, *args, **kwargs):
        result_set = self.filter(*args, **kwargs)

        if len(result_set) == 0:
            raise DoesNotExist(
                '{model} object matching query does not exist.'.format(
                    model=self.model.__name__
                )
            )

        elif len(result_set) == 1:
            return result_set[0]
        else:
            raise MultipleObjectsReturned(
                'get() returned more than one {model} object '
                '-- it returned {num}!'.format(
                    model=self.model.__name__, num=len(result_set)
                )
            )

    def last(self):
        try:
            obj = self[-1]
        except IndexError:
            return None
        else:
            return obj

    def latest(self, field_name: str = 'created'):
        try:
            obj = self.filter(
                **{field_name + '__isnone': False}
            ).order_by(
                field_name
            )[-1]
        except IndexError:
            return None
        else:
            return obj

    def none(self):
        return EmptyQuerySet(model=self.model)

    def order_by(self, *fields: Fields):
        if not fields:
            raise AttributeError

        return type(self)(
            sorted(self, key=cmp(*fields)),
            model=self.model
        )


class EmptyQuerySet(QuerySet):
    def __init__(self, model, *args, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)
        self.model = model
