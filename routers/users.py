import logging
import os
import sys

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from sql import schemas, models
from src import dependencies
from src.dependencies import get_config, get_db, get_except_collection


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/signin", tags=["users"])
def signin(Schemas: schemas.SigninPOST, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    Description: [공통] 로그인
    :return:
    """
    try:
        users = db.query(models.Users).filter_by(id=Schemas.id).first()

        if users is not None:
            if check_password_hash(users.password, Schemas.password) is False:
                raise Exception("아이디 또는 비밀번호 잘못 입력 되었습니다.")
        else:
            raise Exception("사용자 계정을 찾을 수 없습니다.")

        access_token = Authorize.create_access_token(subject=users.idx)
        refresh_token = Authorize.create_refresh_token(subject=users.idx)

        access_token = f"Bearer {access_token}"
        refresh_token = f"Bearer {refresh_token}"

        return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
        logging.warning(error)
        return get_except_collection(value=str(e))
