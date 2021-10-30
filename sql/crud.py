from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import pbkdf2_sha256


def get_user(db: Session, user_idx: int):
    """
    유저를 인덱스 넘버로 얻어오는 메서드
    :param db: DB Session
    :param user_idx: 해당 유저의 인덱스
    :return:
    """
    return db.query(models.User).filter(models.User.idx == user_idx).first()


def update_user(db: Session, user_idx: int, user: schemas.UserModify):
    """
    유저를 업데이트하는 메서드
    :param db:
    :param user_idx:
    :param user:
    :return:
    """
    try:
        value = db.query(models.User).filter(models.User.idx == user_idx).first()
        value.nickname = user.nickname
        value.phone = user.phone
        value.introduce = user.introduce
        value.photo = user.photo
        db.flush()
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_user_vaccine(db: Session, user_idx: int, user: schemas.UserVaccineModify):
    """
    유저의 백신 접종 정보를 업데이트하는 메서드
    :param db:
    :param user_idx:
    :param user:
    :return:
    """
    try:
        value = db.query(models.User).filter(models.User.idx == user_idx).first()
        value.vaccine_certified = user.vaccine_certified
        db.flush()
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_user_my_house_certified(db: Session, user_idx: int, user: schemas.UserMyHouseModify):
    """
    유저의 내 집 인증을 업데이트 하는 메서드
    :param db:
    :param user_idx:
    :param user:
    :return:
    """
    try:
        value = db.query(models.User).filter(models.User.idx == user_idx).first()
        value.my_house_certified = user.my_house_certified
        db.flush()
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_user_identification_certified(db: Session, user_idx: int, user: schemas.UserIdentificationCertifiedModify):
    """
    유저의 내 정보 인증을 업데이트하는 메서드
    :param db:
    :param user_idx:
    :param user:
    :return:
    """
    try:
        value = db.query(models.User).filter(models.User.idx == user_idx).first()
        value.identification_certified = user.identification_certified
        db.flush()
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_user_by_id(db: Session, id: str):
    """
    유저를 아이디로 얻어오는 메서드
    :param db: DB Session
    :param id: 해당 유저의 아이디
    :return:
    """
    return db.query(models.User).filter(models.User.id == id).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    유저를 생성하는 메서드
    :param db: DB Session
    :param user: 유저의 pydantic schema
    :return:
    """
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = models.User(
        id=user.id,
        password=hashed_password,
        nickname=user.nickname,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_houses_by_owner_id(
        db: Session, house_owner: int, skip: int = 0, limit: int = 100
):
    """
    특정 유저의 집을 얻어오는 메서드
    :param db:
    :param house_owner:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.House).filter(models.House.house_owner == house_owner).offset(skip).limit(limit).all()


def get_houses(db: Session, skip: int = 0, limit: int = 100):
    """
    모든 집을 얻어오는 메서드
    :param db: DB Session
    :param skip: 가져올 개수
    :param limit: 제한된 개수
    :return:
    """
    return db.query(models.House).offset(skip).limit(limit).all()


def create_user_house(db: Session, house: schemas.HouseCreate, user_idx: int):
    """
    유저의 집을 생성하는 메서드
    :param db: DB Session
    :param house: 집 객체
    :param user_idx: 유저의 idx
    :return:
    """
    db_house = models.House(**house.dict(), house_owner=user_idx)
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


def read_chat_room(db: Session, user_idx: int):
    """
    특정 유저의 모든 채팅방을 읽는 메서드
    :param db:
    :param user_idx:
    :return:
    """
    db_my_chat_room = db.query(models.ChatRoom).filter(models.ChatRoom.initiator_idx == user_idx).all()
    db_other_chat_room = db.query(models.ChatRoom).filter(models.ChatRoom.opponent_idx == user_idx).all()

    my_chat_room_list = [my_chat_room for my_chat_room in db_my_chat_room]
    other_chat_room_list = [other_chat_room for other_chat_room in db_other_chat_room]

    all_chat_room_list = list(set(my_chat_room_list + other_chat_room_list))
    return all_chat_room_list


def create_chat_room(db: Session, my_idx: int, chat_room: schemas.ChatRoomCreate):
    """
    채팅방을 만드는 메서드
    :param db:
    :param my_idx:
    :param chat_room:
    :return:
    """
    try:
        db_chatroom = models.ChatRoom(
            initiator_idx=my_idx,
            opponent_idx=chat_room.opponent_idx,
            trade_sort=chat_room.trade_sort
        )

        db.add(db_chatroom)
        db.commit()
        db.refresh(db_chatroom)

        db_message = models.Message(
            owner_chat_room=db_chatroom.idx,
            sender_idx=my_idx,
            content="대화 시작",
            sort=7,
        )

        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return db_chatroom
    except Exception as e:
        print(e)
        return None

