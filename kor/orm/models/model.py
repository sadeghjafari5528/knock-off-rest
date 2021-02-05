import attr

from ..models.manager import ManagerDescriptor, RelatedManagerDescriptor
from ..models.store import Store, ModelStoreMapping


class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        attrs['objects'] = ManagerDescriptor()
        mod = attr.s(super(ModelBase, cls).__new__(cls, name, bases, attrs))
        if 'Model' in [base.__name__ for base in bases]:
            ModelStoreMapping[mod.__name__] = Store()

        return mod


class Model(object, metaclass=ModelBase):
    def __new__(cls, *args, **kwargs):
        instance = super(Model, cls).__new__(cls)

        for field in attr.fields(cls):
            if field.metadata.get('related'):
                target = field.metadata['related']['target']

                setattr(
                    target,
                    cls.__name__.lower() + '_set',
                    RelatedManagerDescriptor(model=cls)
                )

        return cls.objects.add(instance)

    @property
    def id(self):
        return id(self)

    def delete(self):
        type(self).objects._delete(self)

    @property
    def _attrs(self):
        return set(self.__dict__.keys()) | {'id'}

    def get_attr(self, attr_name):
        getattr(self, attr_name)
