from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base

def dbCreate():
    engine = create_engine('sqlite:///test6.db')
    return engine

Base = declarative_base()
class Person(Base):

    __tablename__ = "person"
    # id = Column(String, primary_key=True)
    # name = Column(String)
    name = Column(String, primary_key=True)
    lastname = Column(String)

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

engine = dbCreate()
Base.metadata.create_all(engine)
