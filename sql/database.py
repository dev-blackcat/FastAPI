from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# "mysql+pymysql://root:디비비밀번호@서버아이피주소:3306/디비테이블명"
# 데이터베이스 안에 테이블
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:비밀번호@아이피:3306/데이터베이스명"  # mysql

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # sqlalchemy engine 생성

# 서버에서 DB에 요청을 보내기 위한 통로 역할
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # 이 Base클래스를 상속해 각 데이터베이스 모델 or 클래스 생성
