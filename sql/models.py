from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, TIMESTAMP, DateTime, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Users(Base):
    __tablename__ = "users"  # 회원 테이블

    idx = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 인덱스
    id = Column(String, nullable=False, unique=True)  # 회원 아이디
    password = Column(String, nullable=False)  # 회원 비밀번호
    email = Column(String, nullable=False)  # 담당자 이메일
    name = Column(String, nullable=False)  # 담당자 이름
    phone = Column(String, nullable=False)  # 담당자 연락처
    status = Column(Integer, nullable=False, default=0)  # 계정 상태 (0 = 비활성(정지), 1 = 활성)
    access = Column(Integer, nullable=False, default=1)  # 회원 권한 (0 = 담당자(회원), 1 = 일반 관리자, 2 = 최고 관리자)
    status_login = Column(Integer, nullable=False, default=0)  # 로그인 여부 (0 = 비로그인, 1 = 로그인)
    preset_ip = Column(String, nullable=False)  # 접속 가능한 IP (미리 설정하는 값)
    expiry = Column(Integer)  # 만료일 (접속가능한 일자, 최고 관리자는 만료일이 적용되지 않음)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # 생성일


class UserLogs(Base):
    __tablename__ = "userLogs"  # 로그인 기록 테이블

    idx = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 인덱스
    user_idx = Column(Integer, nullable=False)  # 회원 인덱스
    login_status = Column(Integer, nullable=False, default=0)  # 로그인 여부 (0 = 로그인, 1 = 로그아웃)
    login_ip = Column(String, nullable=False, default=0)  # 접속 아이피
    user_agent = Column(String)  # 유저어젠트
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # 생성일


class Reports(Base):
    __tablename__ = "reports"  # 보고서 테이블

    idx = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 인덱스
    user_idx = Column(Integer, nullable=False)  # 회원 인덱스
    order_idx = Column(Integer)  # 주문 인덱스 (분석을 먼저 하기 때문에 분석완료 후 결제)
    type = Column(String, nullable=False)  # 보고서 유형
    status_report = Column(Integer, nullable=False, default=0)  # 분석여부 (0 = 실패, 1 = 성공)
    download_status = Column(Integer, default=0)  # 보고서 다운로드 여부 및 횟수
    download_path = Column(String)  # 보고서 다운로드 경로 (S3)
    upload_path = Column(String, nullable=False)  # 보고서 업로드 경로 (S3)
    delay_time = Column(Integer, nullable=False, default=0)  # 보고서 분석 시간 (S)
    expiry = Column(Integer)  # 보고서 다운로드 만료 시간 (S)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # 생성일


class Orders(Base):
    __tablename__ = "orders"  # 주문 테이블

    idx = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 인덱스
    order_number = Column(Integer, nullable=False)  # 주문번호
    report_idx = Column(Integer)  # 보고서 인덱스
    user_idx = Column(Integer, nullable=False)  # 회원 인덱스
    price = Column(Integer, nullable=False)  # 결제금액
    payment_status = Column(Integer, nullable=False)  # 결제여부 (0 = 미결제, 1 = 결제)
    payment_type = Column(String, nullable=False)  # 결제유형(카드, 계좌이체 ...)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # 생성일


class Questions(Base):
    __tablename__ = "questions"  # 1:1 질문 테이블

    idx = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 인덱스
    user_idx = Column(Integer, nullable=False)  # 회원 인덱스
    category = Column(Integer, nullable=False)  # 카테고리
    content = Column(Text, nullable=False)  # 내용
    answer = Column(Text)  # 답변 및 답변상태
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # 생성일
