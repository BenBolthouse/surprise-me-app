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

    seen_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    dismissed_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    @property
    def is_seen(self):
        '''
        Return True if the entity has been seen, False if not.
        '''
        return self.seen_at is not None

    def set_seen_at(self):
        '''
        Indicate the entity has been seen at the current datetime.
        '''
        self.seen_at = datetime.now()

    @property
    def is_dismissed(self):
        '''
        Return True if the entity has been dismissed, False if not.
        '''
        return self.dismissed_at is not None

    def dismissible_to_dict(self):
        return {
            "seen_at": self.seen_at.isoformat() if self.seen_at else None,
            "dismissed_at": self.dismissed_at.isoformat() if self.dismissed_at else None,
        }

    def set_dismissed_at(self):
        '''
        Indicate the entity has been dismissed at the current datetime.
        '''
        self.seen_at = datetime.now()
