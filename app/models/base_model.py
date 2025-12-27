from sqlalchemy.orm import declared_attr, as_declarative

@as_declarative()
class Base:
    __abstract__ = True
    __name__: str

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class BaseModel(Base):
    __abstract__ = True
