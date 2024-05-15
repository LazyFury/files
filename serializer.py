import datetime
from django.db import models


class Serializer(object):
    data: models.Model
    with_relations: bool = False

    def __init__(self, data, with_relations=True):
        self.data = data
        self.with_relations = with_relations

    def convert(self, value):
        if isinstance(value, models.Model):
            return Serializer(value).serialize()
        if isinstance(value,datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value

    def serialize(self, fields=[],hidden=[]):
        data =  {k: v for k, v in self._serialize(fields)}
        for k in hidden:
            data.pop(k)
        return data

    def _serialize(self, fields=[]):
        if fields and len(fields) > 0:
            for f in fields:
                yield f, self.convert(getattr(self.data, f)) if hasattr(self.data, f) else None
            return

        for f in self.fields():
            yield (
                f.name,
                self.convert(getattr(self.data, f.name)) if hasattr(self.data, f.name) else None,
            )

        if self.with_relations:
            for r in self.relations():
                relate_name = r.name
                manager = (
                    getattr(self.data, relate_name)
                    if hasattr(self.data, relate_name)
                    else None
                )
                if manager:
                    if r.many_to_many or r.one_to_many:
                        yield (
                            relate_name,
                            [Serializer(i, False).serialize() for i in manager.all()],
                        )
                        yield f"{relate_name}_count", manager.count()
                    else:
                        yield relate_name, Serializer(manager, False).serialize()
                        yield (
                            f"{relate_name}_id",
                            getattr(self.data, f"{relate_name}_id")
                            if hasattr(self.data, f"{relate_name}_id")
                            else None,
                        )
                else:
                    yield relate_name, None

    def fields(self):
        return [f for f in self.data._meta.get_fields() if not f.is_relation]

    def relations(self):
        return [f for f in self.data._meta.get_fields() if f.is_relation]
