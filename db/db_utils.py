""" Contains some utility for the TaskBot database """
import db.schemas


def create_user_if_not_exists(session, user_id: int) -> None:
    """ Creates a user if it doesn't exist already """
    db_user = session.query(db.schemas.Users).filter_by(id=user_id).first()
    if db_user is None:
        session.add(db.schemas.Users(id=user_id))
        session.commit()
        db_user = session.query(db.schemas.Users).filter_by(id=user_id).first()
