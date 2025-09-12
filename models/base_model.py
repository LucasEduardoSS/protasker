from peewee import Model


class BaseModel(Model):
    class Meta:
        database = None

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"

    @classmethod
    def get_all(cls):
        return cls.select()
