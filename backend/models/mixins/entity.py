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
    _type = db.Column(
        db.String(32),
        name="type",
        nullable=False,
        default="")
    _created_at = db.Column(
        db.DateTime,
        name="created_at",
        server_default=db.func.now())
    _updated_at = db.Column(
        db.DateTime,
        name="updated_at",
        nullable=True,
        default=None)
    _deleted_at = db.Column(
        db.DateTime,
        name="deleted_at",
        nullable=True,
        default=None)

    @property
    def type(self):
        '''
        Get the type of the entity or None if the type is not defined.
        '''
        if self._type == "":
            return None
        return self._type

    @property
    def created_at(self):
        '''
        Get the datetime that the entity was created in the database.
        '''
        return self._created_at

    @property
    def updated_at(self):
        '''
        Get the datetime that the entity was last updated in the application.
        '''
        return self._updated_at

    @property
    def deleted_at(self):
        '''
        Get the datetime that the entity was soft deleted in the application.
        '''
        return self._deleted_at

    @property
    def is_deleted(self):
        '''
        Returns true if the entity is soft deleted, False if not.
        '''
        return self._deleted_at is True

    def set_type(self, value):
        '''
        Set the type of the entity. Type must be a string member of the set
        attribute _types.
        '''
        try:
            # The following checks if _types is implemented, which is
            # required if set_type is invoked.
            if not isinstance(self._types, set):
                raise AttributeError(
                    "Inheritance classes of BaseMixin using type properties and methods must implement set attribute _types.")

            # Below the _types attribute is looped to check if all members
            # are strings, since an entity type is represented by a string.
            for x in self._types:
                if not isinstance(x, str):
                    raise AttributeError("Members of set attribute _types can only be strings.")

            if value not in self._types:
                raise AttributeError("Value not a member of set attribute _types.")

        except Exception as exception:
            raise Exception(exception.args)

    def set_updated_at(self):
        '''
        Update the datetime attribute _updated_at to the current application
        datetime.
        '''
        self._updated_at = datetime.now()

    def set_deleted_at(self):
        '''
        Update the datetime attribute _deleted_at to the current application
        datetime.
        '''
        self._updated_at = datetime.now()

    def unset_deleted_at(self):
        '''
        Nullify the datetime attribute _deleted_at.
        '''
        self._updated_at = datetime.now()