from peewee import Model


class BaseModel(Model):
    class Meta:
        database = None

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"

    @classmethod
    def get_meta(cls):
        return cls._meta

    @classmethod
    def get_all(cls):
        return cls.select()

    @classmethod
    def get_all_dicts(cls, order_by: str | None = None):
        """
        Retorna uma lista de dicionários com os dados dos registros.
        - order_by: Campo de referência para ordenar. Pode ser:
            - str: nome do campo do model (ex.: "name")
            - Field do Peewee: ex.: cls.name.desc()
        """
        query = cls.select()

        if order_by:
            # Se for string, converte para Field do Model
            if isinstance(order_by, str):
                if not hasattr(cls, order_by):
                    raise AttributeError(f"Campo '{order_by}' não existe no model {cls.__name__}.")
                field = getattr(cls, order_by)
                query = query.order_by(field)
            else:
                # Assume que seja um Field/expressão do Peewee
                query = query.order_by(order_by)

        return list(query.dicts())
