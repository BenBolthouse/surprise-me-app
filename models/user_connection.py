from .db import db


class UserConnection(db.Model):
    __tablename__ = "user_connections"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    requestor_user_id = db.Column(db.Integer,
                                  db.ForeignKey('users.id'),
                                  nullable=False)
    connection_user_id = db.Column(db.Integer,
                                   db.ForeignKey('users.id'),
                                   nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    established_at = db.Column(db.DateTime, nullable=True, default=None)

    # Scopes
    def to_json_on_create(self):
        return {
            "id": self.id,
            "requestorId": self.requestor_user_id,
            "connectionId": self.connection_user_id,
            "createdAt": self.created_at,
        }

    def to_json_messages_quantity(self):
        # TODO implement messages quantity scope
        pass
