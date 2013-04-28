from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, PickleType
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///passwords.db", echo = False)
session = scoped_session(sessionmaker(bind = engine, autocommit = False, autoflush = False)) # scoped_session is being used to guarantee thread-safety for multiple users accessing this same app

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User (Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(PickleType, nullable = True) # Holds Python objects, which are serialized using pickle


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__": # calls main function if we were to run this model.py file directly (vs. importing into another Python file)
    main()