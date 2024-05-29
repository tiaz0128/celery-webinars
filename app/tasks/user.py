import logging
from sqlalchemy.orm import Session

from app.domain.models.user import UserMst
from app.schemas.user import User
from app.utils.db import make_session
from run import app


import random
import string

from run import app


@app.task(queue="db_queue")
def schedule_user_add_task():
    parent_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    user_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    logging.info(f"parent_id: {parent_id}, user_id: {user_id}")
    app.send_task("app.tasks.user.user_add", args=[parent_id, user_id])


@app.task(queue="db_queue")
def user_add(parent_id: str, user_id: str):
    session: Session = make_session()
    user = User(parent_id=parent_id, user_id=user_id)

    logging.info(user)
    logging.info(user.model_dump())

    session.add(UserMst(**user.model_dump()))
    session.commit()

    return "success"
