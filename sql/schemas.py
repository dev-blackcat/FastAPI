import datetime
from typing import List, Optional
from pydantic import BaseModel

"""
orm_mode : Form 타입으로 받던 상관없이 JSON 형태로 변환(pydantic 제공, 반환 모델)
"""

"""
Name: SigninPOST
Description: [공통] 로그인 스키마
:return:
"""
class SigninPOST(BaseModel):
    id: str  # 아이디
    password: str  # 비밀번호

    class Config:
        orm_mode = True


"""
Name: GeneratorPasswordPOST
Description: [공통] 비밀번호 생성
:return:
"""
class GeneratorPasswordPOST(BaseModel):
    password: str  # 비밀번호

    class Config:
        orm_mode = True

"""
Name: SignUpPOST
Description: [관리자] 계정 생성
:return:
"""
class SignUpPOST(BaseModel):
    id: str  # 아이디
    password: str  # 비밀번호
    email: str  # 담당자 이메일
    name: str  # 담당자 성함
    phone: str  # 담당자 연락처
    status: int  # 상태
    access: int  # 권한
    preset_ip: str  # 로그인 아이피 지정

    class Config:
        orm_mode = True


"""
Name: QuestionPOST
Description: [사용자] 질문 추가
:return:
"""
class QuestionPOST(BaseModel):
    category: str  # 카테고리
    content: str  # 질문내용

    class Config:
        orm_mode = True


"""
Name: QuestionPUT
Description: [사용자] 질문 수정
:return:
"""
class QuestionPUT(BaseModel):
    category: str  # 카테고리
    content: str  # 질문내용

    class Config:
        orm_mode = True




# class ReviewPhotoBase(BaseModel):
#     photo_owner: int
#     url: str
#
#
# class ReviewPhotoCreate(ReviewPhotoBase):
#     pass
#
#
# class ReviewPhoto(ReviewPhotoBase):
#     idx: int
#
#     class Config:
#         orm_mode = True
#
#
# class ReviewBase(BaseModel):
#     rating: float
#     started_date: datetime.datetime
#     end_date: datetime.datetime
#     content: str
#     review_owner: int
#     review_photos: List[ReviewPhoto] = []
#
#
# class Review(ReviewBase):
#     idx: int
#
#     class Config:
#         orm_mode = True
#
#
# class ReviewCreate(ReviewBase):
#     pass
#
#
# class WishListsBase(BaseModel):
#     house_idx: int
#     wishlist_owner: int
#
#
# class WishListsCreate(WishListsBase):
#     pass
#
#
# class WishLists(WishListsBase):
#     idx: int
#
#     class Config:
#         orm_mode = True
#
#
# class HousePhotoBase(BaseModel):
#     url: str
#     photo_owner: int
#
#
# class HousePhoto(HousePhotoBase):
#     idx: int
#
#
# class HousePhotoCreate(HousePhotoBase):
#     pass
#
#
# class HouseBase(BaseModel):
#     name: str
#     address: str
#     lat: float
#     lon: float
#     available_date_start: datetime.datetime
#     available_date_end: datetime.datetime
#     require_point_per_day: int
#     introduce_title: str
#     introduce_content: str
#     house_photos: List[HousePhoto] = []
#
#
# class House(HouseBase):
#     idx: int
#     house_owner: int
#
#     class Config:
#         orm_mode = True
#
#
# class HouseCreate(HouseBase):
#     pass
#
#
# class UserBase(BaseModel):
#     pass
#
#
# class User(UserBase):
#     idx: int
#     id: str
#     social_id: Optional[str]
#     nickname: str
#     phone: str
#     photo: str
#     introduce: str
#     identification_certified: bool
#     my_house_certified: bool
#     vaccine_certified: bool
#     houses: List[House] = []
#     wishlists: List[WishLists] = []
#     reviews: List[Review] = []
#
#     class Config:
#         orm_mode = True
#
#
# class UserSignIn(UserBase):
#     id: str
#     password: str
#
#
# class UserSocialCreate(BaseModel):
#     social_id: str
#     nickname: str
#     phone: str
#
#
# class UserCreate(UserBase):
#     id: str
#     password: str
#     phone: str
#     nickname: str
#     phone: str
#
#
# class UserModify(UserBase):
#     nickname: str
#     phone: str
#     photo: str
#     introduce: str
#
#
# class UserVaccineModify(UserBase):
#     vaccine_certified: bool
#
#
# class UserMyHouseModify(UserBase):
#     my_house_certified: bool
#
#
# class UserIdentificationCertifiedModify(UserBase):
#     identification_certified: bool
#
#
# class ChatRoomCreate(BaseModel):
#     opponent_idx: int
#     trade_sort: int
#
#
# class SendNormalMessage(BaseModel):
#     message: str
#
