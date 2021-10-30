import os
import sys
import logging

from fastapi import FastAPI, Response, HTTPException, Depends, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.openapi.utils import get_openapi
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import users

from typing import Optional
from sqlalchemy.orm import Session
from starlette import status
from werkzeug.security import generate_password_hash, check_password_hash

from sql import database
from sql import models
from sql import schemas
from src.dependencies import get_config, get_db, get_except_collection


app = FastAPI()

database.Base.metadata.create_all(database.engine)

app.include_router(users.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_open_api():
    if app.openapi_schema:
        return app.openapi_schema
    open_api_schema = get_openapi(
        title="TALOS(병원모듈)",
        version="0.0.1",
        description="TALOS(병원모듈)의 백엔드 어플리케이션 스키마 설계입니다.",
        routes=app.routes
    )
    app.openapi_schema = open_api_schema
    return app.openapi_schema


# AUTH JWT에 대한 예외 처리
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get("/ping")
async def read():
    """
    Description: [공통] 헬스체크
    :return:
    """

    try:
        raise Exception("서버 오류가 발생했습니다.")

        return {"status": 200, "result": "pong"}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
        logging.warning(error)
        return dependencies.get_except_collection(value=str(e))


@app.post("/generator/password")
async def generator_password(res: schemas.GeneratorPasswordPOST):
    """
    Description: [공통] 비밀번호 해시 변환
    :return:
    """

    try:
        return {"generator_password": generate_password_hash(res.password)}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
        logging.warning(error)
        return get_except_collection(value=str(e))


app.openapi = custom_open_api


# @app.post("/signup")
# async def signup(Schemas: schemas.SignUpPOST, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Title: [관리자] 계정생성
#     Description: 관리자만 계정을 생성 할 수 있습니다.
#     :return:
#     """
#     try:
#         Authorize.jwt_required()
#         current_user = Authorize.get_jwt_subject()
#
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             if users.access == 2:
#                 users = db.query(models.Users).filter_by(id=Schemas.id).first()
#
#                 if users is not None:
#                     raise Exception("이미 가입된 정보가 있습니다.")
#
#                 users = models.Users(id=Schemas.id, password=generate_password_hash(Schemas.password), email=Schemas.email, name=Schemas.name, phone=Schemas.phone, status=Schemas.status, access=Schemas.access, preset_ip=Schemas.preset_ip)
#                 db.add(users)
#                 db.commit()
#                 db.refresh(users)
#                 db.close()
#             else:
#                 raise Exception("권한이 없습니다.")
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#
#         return {"status": 200}
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.post("/refresh")
# def refresh(Authorize: AuthJWT = Depends()):
#     """
#     Description: [공통]
#                 jwt_refresh_token_required() 함수는 유효한 새로 고침을 보장합니다.
#                 토큰은 해당 함수 아래의 코드를 실행하기 전에 요청에 있습니다.
#                 get_jwt_subject() 함수를 사용하여 새로 고침의 주제를 얻을 수 있습니다.
#                 토큰을 만들고 create_access_token() 함수를 다시 사용하여 새 액세스 토큰을 만듭니다.
#     :return:
#     """
#     try:
#         Authorize.jwt_refresh_token_required()
#
#         current_user = Authorize.get_jwt_subject()
#         new_access_token = Authorize.create_access_token(subject=current_user)
#         return {"access_token": new_access_token}
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.get('/user')
# def user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: [공통] 회원 정보
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         return users
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.get('/user/{user_idx}')
# def user(user_idx, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: [관리자] 특정 회원 정보
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             if users.access != 2:
#                 raise Exception("권한이 없습니다.")
#             else:
#                 return db.query(models.Users).filter_by(idx=user_idx).first()
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.delete('/user/{user_idx}')
# def user(user_idx, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: [관리자] 특정 회원 정보
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             if users.access != 2:
#                 raise Exception("권한이 없습니다.")
#             else:
#                 return db.query(models.Users).filter_by(idx=user_idx).first()
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.post('/questions')
# def user(Schemas: schemas.QuestionPOST, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: 1:1 질문 추가
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             questions = db.query(models.Questions).filter(models.Questions.user_idx == current_user, models.Questions.category == Schemas.category,
#                                                           models.Questions.answer is not None).all()
#
#             if users.access == 2:
#                 raise Exception("최고 관리자는 질문 할 수 없습니다.")
#
#             if len(questions) > 0:
#                 raise Exception("이미 동일한 요청이 있습니다.")
#
#             questions = models.Questions(user_idx=current_user, category=Schemas.category, content=Schemas.content)
#             db.add(questions)
#             db.commit()
#             db.refresh(questions)
#             db.close()
#
#             return {"status": 200}
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.get('/questions')
# def user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: 질문 리스트 조회
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             questions = db.query(models.Questions).filter_by(user_idx=current_user).all()
#             db.close()
#
#             return questions
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.get('/questions/detail/{question_idx}')
# def user(question_idx, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: 질문 상세정보 조회
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             questions = db.query(models.Questions).filter_by(idx=question_idx, user_idx=current_user).first()
#             db.close()
#
#             return questions
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.put('/questions/{question_idx}')
# def user(question_idx, Schemas: schemas.QuestionPUT, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: 질문 수정
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             questions = db.query(models.Questions).filter_by(idx=question_idx, user_idx=current_user).first()
#
#             if questions is not None:
#                 setattr(questions, "category", Schemas.category)
#                 setattr(questions, "content", Schemas.content)
#                 db.commit()
#                 db.refresh(questions)
#                 db.close()
#             else:
#                 raise Exception("잘못된 요청 입니다.")
#
#             return {"status": 200}
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))
#
#
# @app.delete('/questions/{question_idx}')
# def user(question_idx, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     Description: 1:1 질문 삭제
#     :return:
#     """
#
#     try:
#         Authorize.jwt_required()
#
#         current_user = Authorize.get_jwt_subject()
#         users = db.query(models.Users).filter_by(idx=current_user).first()
#
#         if users is not None:
#             if users.access == 2:
#                 questions = models.Questions(idx=question_idx, user_idx=current_user)
#
#                 if questions is not None:
#                     db.delete(questions)
#                     db.commit()
#                     db.close()
#                 else:
#                     raise Exception("잘못된 요청 입니다.")
#             else:
#                 raise Exception("권한이 없습니다.")
#
#             return {"status": 200}
#         else:
#             raise Exception("사용자 계정을 찾을 수 없습니다.")
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         error = f"{e} {exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno}"
#         logging.warning(error)
#         return get_except_collection(value=str(e))




# # 스키마 모델을 쓸때
# @app.post("/blog")
# async def create(req: schemas.Blog, db: Session = Depends(dependencies.get_db)):
#     try:
#         new_blog = models.Blog(title=req.title, body=req.body, phone=req.phone, address=req.address)
#         db.add(new_blog)  # DB 추가
#         db.commit()  # DB 저장(이것을 안하면 저장이 안됨)
#         db.refresh(new_blog)  # DB 새로고침
#         db.close()  # DB 닫기
#
#         return new_blog
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno)
#
#         return {"result": "오류"}
#
#
# @app.get("/blog")
# async def read(search: str, page: int, db: Session = Depends(dependencies.get_db)):
#     try:
#         print(search)
#         print(page)
#         # 전체 가져올때
#         # database = db.query(models.Blog).all()
#         # return database
#
#         # 일부분만 가져올때(특정하여)
#         database = db.query(models.Blog).filter(models.Blog.title.contains(search)).all()
#         return database
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno)
#
#         return {"result": "오류"}
#
#
# @app.put("/blog")
# async def update(req: schemas.Blog, db: Session = Depends(dependencies.get_db)):
#     try:
#         print(req)
#         new_blog = db.query(models.Blog).filter_by(phone=req.phone).first()
#         setattr(new_blog, "phone", req.new_phone)
#         db.commit()
#         db.refresh(new_blog)
#         db.close()
#
#         return new_blog
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno)
#
#         return {"result": "오류"}
#
#
# # 스키마를 통한 삭제는 완료
# # 하지만, 삭제를 할때 본인확인의 경우는 JWT 유저 인덱스 값 받아서 체크하면 되고
# # 삭제를 하기 위한 해당 데이터 index만 리퀘스트로 받아서 처리하면 될일...
# @app.delete("/blog")
# async def delete(req: schemas.Blog, db: Session = Depends(dependencies.get_db)):
#     try:
#         print(req.idx)
#         new_blog = db.query(models.Blog).filter_by(idx=req.idx).first()
#         db.delete(new_blog)
#         db.commit()
#         db.close()
#
#         return {"result": "삭제 성공"}
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno)
#
#         return {"result": "오류"}
#
#
# # 리퀘스트로 필요한 값만 받아서 삭제
# # 사실 user_idx(jwt), blog_idx 이거 두개만 받으면됨
# # 내일 리퀘스트로 받아서 처리하는 방식을 찾아야함
# @app.delete("/blog4")
# async def delete4(req: Request, db: Session = Depends(dependencies.get_db)):
#     try:
#         # test = {
#         #     "test_idx": "테스트다"
#         # }
#         # print(test.test_idx)
#         # object(객체)의 경우에는 "."(점)으로 접근하여 가져올 수 있다.
#
#         # print(req.idx)
#         json_data = await req.json()
#         blog_idx = json_data["idx"]
#         # blog_title = json_data["title"]
#         print(json_data["idx"])
#         new_blog = db.query(models.Blog).filter_by(idx=blog_idx).first()
#         db.delete(new_blog)
#         db.commit()
#         db.close()
#
#         return {"result": "삭제 성공"}
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         print(exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno)
#
#         return {"result": "오류"}
