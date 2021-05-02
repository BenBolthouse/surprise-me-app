# -*- coding: utf-8 -*-
'''
    models.mixin.scored
    ------------------
    Module contains ScoredMixin class which provides functionality for
    attributing a score based on engagement.
'''


from ..db import db


class ScoredMixin(object):
    '''
    Base class provides functionality for attributing a score based on
    engagement.
    '''

    _score = db.Column(
        db.BigInteger,
        name="score",
        nullable=True,
        default=0)
    _grade = db.Column(
        db.Float(precision=2),
        name="grade",
        nullable=True,
        default=0.00)

    @property
    def score(self):
        return self._score

    @property
    def grade(self):
        return self._grade

    def set_grade(self, user_score, points):
        '''
        Sets the grade of the user interaction based on user's total categorical
        interaction averaged with the total score for the scored entity. The result
        is a percentage grade of engagement weighted against the user's total
        engagement for the specific category.
        '''
        if self._score + points < 1:
            self._score = 0
            self._grade = 0

        else:
            self._score += points
            self._grade = user_score / self._score * 100

    def __init__(self):
        self._score = 0
        self._grade = 0.00
