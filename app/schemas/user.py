from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    parent_id: str
    user_id: str

    ins_dt: datetime = datetime.now()
    ins_user: str | None = "MASTER"
    upd_dt: datetime = datetime.now()
    upd_user: str | None = "MASTER"
