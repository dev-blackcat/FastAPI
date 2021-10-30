import logging
import os
import sys

from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.responses import JSONResponse

from src.settings import Settings
from sql import database


@AuthJWT.load_config
def get_config():
    return Settings()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_except_collection(value: str):
    status_code = status.HTTP_200_OK
    error = None

    try:
        if value == "아이디 또는 비밀번호 잘못 입력 되었습니다.":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif value == "사용자 계정을 찾을 수 없습니다.":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif value == "권한이 없습니다.":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif value == "최고 관리자는 질문 할 수 없습니다.":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif value == "최고 관리자는 탈퇴 요청을 할 수 없습니다.":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif value == "이미 가입된 정보가 있습니다.":
            status_code = status.HTTP_409_CONFLICT
        elif value == "이미 동일한 요청이 있습니다.":
            status_code = status.HTTP_409_CONFLICT
        elif value == "잘못된 요청 입니다.":
            status_code = status.HTTP_400_BAD_REQUEST
        elif value == "서버 오류가 발생했습니다.":
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
        logging.warning(error)
    finally:
        json_response = jsonable_encoder({
            "status": status_code,
            "detail": value,
            "error": error
        })

        return JSONResponse(content=json_response, status_code=status_code)
