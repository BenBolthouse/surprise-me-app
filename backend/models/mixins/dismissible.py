# -*- coding: utf-8 -*-
'''
    models.mixin.dismissable
    ------------------
    Module contains DismissibleMixin class which provides functionality for
    marking an entity as seen and/or dismissed by a user.
'''


from datetime import datetime


from ..db import db


class DismissibleMixin(object):
    '''
    Base class provides functionality to mark an entity as seen and/or
    dismissed.
    '''

    _seen_at = db.Column(
        db.DateTime,
        name="seen_at",
        nullable=True,
        default=None)
    _dismissed_at = db.Column(
        db.DateTime,
        name="dismissed_at",
        nullable=True,
        default=None)

    @property
    def is_seen(self):
        '''
        Return True if the entity has been seen, False if not.
        '''
        return self._seen_at is not None

    def _set_seen_at(self):
        '''
        Indicate the entity has been seen at the current datetime.
        '''
        self._seen_at = datetime.now()

    @property
    def is_dismissed(self):
        '''
        Return True if the entity has been dismissed, False if not.
        '''
        return self._dismissed_at is not None

    def _dismissible_to_dict(self):
        return {
            "seen_at": self._seen_at.isoformat(),
            "dismissed_at": self._dismissed_at.isoformat(),
        }

    def _set_dismissed_at(self):
        '''
        Indicate the entity has been dismissed at the current datetime.
        '''
        self._seen_at = datetime.now()
