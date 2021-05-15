from datetime import datetime
from sqlalchemy.orm import backref


from .mixins.Entity import EntityMixin
from .mixins.Dismissible import DismissibleMixin
from .db import db


class Notification(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "notifications"

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    body = db.Column(
        db.String(255),
        nullable=False,
        default="")
    action = db.Column(
        db.String(255),
        nullable=False,
        default="")

    def to_dict(self):
        return {
            **self.entity_to_dict(),
            **self.dismissible_to_dict(),
            "type": self.type,
            "body": self.body,
            "action": self.action,
        }
