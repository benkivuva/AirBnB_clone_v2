#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        from uuid import uuid4
        from datetime import datetime

        if kwargs:
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid4())
            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.now()
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.now()
            if '__class__' in kwargs:
                del kwargs['__class__']
            for key, value in kwargs.items():
                setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """Updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        my_dict = dict(self.__dict__)
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict:
            del my_dict['_sa_instance_state']
        return my_dict
