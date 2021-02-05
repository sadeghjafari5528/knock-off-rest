from datetime import datetime

from ..models.store import ModelStoreMapping
from ..query import QuerySet, EmptyQuerySet


class ManagerDescriptor(object):
    def __init__(self):
        self.manager = None

    def __get__(self, instance, owner):
        if instance:
            raise AttributeError
        self.manager = Manager(model=owner)
        return self.manager


class RelatedManagerDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError

        class RelatedManager(Manager):
            def get_queryset(related_manager_self):
                cls_name = type(instance).__name__.lower()
                return super(RelatedManager, related_manager_self).get_queryset().\
                    filter(**{'{}__pk'.format(cls_name): instance.pk})

        return RelatedManager(model=self.model)


class Manager(object):
    def __init__(self, model):
        self.model = model

    @property
    def store(self):
        return ModelStoreMapping.get(self.model.__name__)

    def get_queryset(self):
        return QuerySet(
            self.store,
            model=self.model
        )

    def add(self, instance):
        if not isinstance(instance, self.model):
            raise TypeError(
                '{model} instance expected, got {obj}'.format(
                    model=self.model.__name__,
                    obj=instance
                )
            )

        instance.created = instance.updated = datetime.utcnow()
        self.store.append(instance)
        return instance

    def _delete(self, obj):
        self.store.remove(obj)

    def all(self):
        return self.get_queryset()

    def count(self):
        return self.all().count()

    def earliest(self, field_name: str = 'created'):
        return self.all().earliest(field_name)

    def exclude(self, *args, **kwargs):
        return self.all().exclude(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.all().filter(*args, **kwargs)

    def first(self):
        return self.all().earliest()

    def get(self, **kwargs):
        return self.all().get(**kwargs)

    def last(self):
        return self.all().latest()

    def latest(self, field_name: str = 'created'):
        return self.all().latest(field_name)

    def none(self):
        return EmptyQuerySet(model=self.model)

    def __repr__(self):
        return '<{manager}: {model}>'.format(
            manager=type(self).__name__, model=self.model.__name__
        )
