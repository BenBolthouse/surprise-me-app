# -*- coding: utf-8 -*-
'''
    models.mixins.entity
    ------------------
    Module contains EntityMixin class, a base class that provides functionality
    for typing and timestamping of database entities, as well as some other
    helpful functionality.
'''

from datetime import datetime


from ..db import db


class EntityMixin(object):
    '''
    Base class provides all of the basic functionality for application
    entities.
    '''
    id = db.Column(
        db.Integer,
        primary_key=True)
    type = db.Column(
        db.String(32),
        nullable=True,
        default=None)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    deleted_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    @property
    def is_deleted(self):
        '''
        Returns true if the entity is soft deleted, False if not.
        '''
        return self.deleted_at is not None

    def set_type(self, value):
        '''
        Set the type of the entity. Type must be a string member of the set
        attribute types.
        '''
        try:
            # The following checks if types is implemented, which is
            # required if set_type is invoked.
            if not isinstance(self.types, set):
                raise AttributeError(
                    "Inheritance classes of BaseMixin using type properties and methods must implement set attribute types.")

            # Below the _types attribute is looped to check if all members
            # are strings, since an entity type is represented by a string.
            for x in self.types:
                if not isinstance(x, str):
                    raise AttributeError("Members of set attribute types can only be strings.")

            if value not in self.types:
                raise AttributeError("Value not a member of set attribute _types.")

        except Exception as exception:
            raise Exception(exception.args)

    def set_updated_at(self):
        '''
        Update the datetime attribute updated_at to the current application
        datetime.
        '''
        self.updated_at = datetime.now()

    def set_deleted_at(self):
        '''
        Update the datetime attribute updated_at to the current application
        datetime.
        '''
        self.deleted_at = datetime.now()

    def unset_deleted_at(self):
        '''
        Nullify the datetime attribute deleted_at.
        '''
        self.deleted_at = None

    def update(self, **kwargs):
        '''
        Updates the entity. Kwargs must match the entity's property key and be
        assigned a value that is compatible with the database schema.
        '''
        for k, v in kwargs.items():
            # Skip any kwargs with None values: ...
            if v is None:
                continue

            # The following will try to get the property of the entity
            # object from the kwargs used. If the property doesn't exist it
            # skips the loop. If it does exist then the object property
            # will be updated with the kwarg value. This allows for any
            # property anywhere to be updated to a new value, which is nice
            # and dry :)
            try:
                attr = setattr(self, k, v)
            except Exception:
                pass

        self.updated_at = datetime.now()

    def entity_to_dict(self):
        '''
        Returns a dictionary of the entity's state.
        '''
        return {
            "id": self.id,
            "type": self.type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
