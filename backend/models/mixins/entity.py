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
    _id = db.Column(
        db.Integer,
        name="id",
        primary_key=True)
    _type = db.Column(
        db.String(32),
        name="type",
        nullable=True,
        default=None)
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
    def id(self):
        '''
        Get the database id of the entity.
        '''
        return self._id

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
        return self._deleted_at is not None

    def _set_type(self, value):
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

    def _set_updated_at(self):
        '''
        Update the datetime attribute _updated_at to the current application
        datetime.
        '''
        self._updated_at = datetime.now()

    def _set_deleted_at(self):
        '''
        Update the datetime attribute _deleted_at to the current application
        datetime.
        '''
        self._updated_at = datetime.now()

    def _unset_deleted_at(self):
        '''
        Nullify the datetime attribute _deleted_at.
        '''
        self._deleted_at = None

    def _update(self, **kwargs):
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
                attr = getattr(self, k)
                attr = v
            except Exception:
                pass

        self._updated_at = datetime.now()

    def _entity_to_dict(self):
        '''
        Returns a dictionary of the entity's state.
        '''
        return {
            "id": self._id,
            "type": self._type,
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "updated_at": self._updated_at.isoformat() if self._updated_at else None,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
        }
