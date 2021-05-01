from sqlalchemy import and_, or_


from ..mixins.scored import ScoredMixin
from ..db import db


CONNECTION_POINTS = 10
GIFT_POINTS = 5
PROFILE_POINTS = 3
MESSAGE_POINTS = 1


class ScoredUser(db.Model, ScoredMixin):
    __tablename__ = "scored_users"

    id = db.Column(
        db.Integer,
        primary_key=True)
    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id',
                      name="user",
                      ondelete="CASCADE"),
        nullable=False)
    target_user = db.Column(
        db.Integer,
        db.ForeignKey('users.id',
                      name="target_user",
                      ondelete="CASCADE"),
        nullable=False)

    @staticmethod
    def get(user_id, target_user_id):
        return ScoredUser.query.filter(
            and_(
                ScoredUser.user == user_id,
                ScoredUser.target_user == target_user_id)).first()

    @staticmethod
    def get_bidirectional(user_a_id, user_b_id):
        return ScoredUser.query.filter(
            or_(
                and_(
                    ScoredUser.user == user_a_id,
                    ScoredUser.target_user == user_b_id),
                and_(
                    ScoredUser.user == user_b_id,
                    ScoredUser.target_user == user_a_id))).all()

    def create_connection(self, user):
        user.set_user_engagement_score(CONNECTION_POINTS)
        self.set_grade(user._user_engagement_score, CONNECTION_POINTS)

    def leave_connection(self, user):
        user.set_user_engagement_score(-CONNECTION_POINTS)
        self.set_grade(user._user_engagement_score, -CONNECTION_POINTS)

    def send_gift(self, user):
        user.set_user_engagement_score(GIFT_POINTS)
        self.set_grade(user._user_engagement_score, GIFT_POINTS)

    def view_profile(self, user):
        user.set_user_engagement_score(PROFILE_POINTS)
        self.set_grade(user._user_engagement_score, PROFILE_POINTS)

    def send_message(self, user):
        user.set_user_engagement_score(MESSAGE_POINTS)
        self.set_grade(user._user_engagement_score, MESSAGE_POINTS)

    def __init__(self, user_id, target_user_id):
        scored_user = ScoredUser.get(user_id, target_user_id)

        if scored_user is not None:
            return scored_user
        
        ScoredMixin.__init__(self)
        self.user = user_id
        self.target_user = target_user_id
