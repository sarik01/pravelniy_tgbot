from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import Column, String, Integer, Text, ForeignKey, select, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from sqlalchemy.orm import declarative_base, relationship

from loader import bot, _

Base = declarative_base()

engine = create_async_engine(
    "postgresql+asyncpg://postgres:123456@localhost:5432/tgbot",
    echo=True,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = Session()

from dataclasses import dataclass


#
@dataclass
class User_test:
    id: int
    username: str
    email: str
    full_name: str


class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    fio = Column('fio', String)
    phone = Column('phone', String)
    lang = Column('lang', String)
    tg_user_id = Column('tg_user_id', BigInteger)
    application = relationship("Application", backref='users')

    def __init__(self, fio, phone, tg_user_id, lang):
        self.fio = fio
        self.phone = phone
        self.tg_user_id = tg_user_id
        self.lang = lang

    def __repr__(self):
        return f"{self.id}"


class Category(Base):
    __tablename__ = 'category'
    id = Column('id', Integer, primary_key=True)
    name_uz = Column('name_uz', String, unique=True)
    name_ru = Column('name_ru', String, unique=True)
    name_uz_kir = Column('name_uz_kir', String, unique=True)
    application = relationship("Application", backref='categories')

    def __init__(self, name_uz, name_ru, name_uz_kir):
        self.name_uz = name_uz
        self.name_ru = name_ru
        self.name_uz_kir = name_uz_kir


class Application(Base):
    __tablename__ = 'application'
    id = Column('id', Integer, primary_key=True)
    status = Column('status', String, default='pending')
    application = Column('application', Text, default='pending')
    answer = Column('answer', String)
    sent = Column('sent', String)
    lang = Column('lang', String)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    def __int__(self, status, application, answer, user_id, category_id, sent):
        self.status = status
        self.application = application
        self.answer = answer
        self.user_id = user_id
        self.category_id = category_id
        self.sent = sent


class Text(Base):
    __tablename__ = 'text'
    id = Column('id', Integer, primary_key=True)
    greeting = Column('greeting', Text)
    step1 = Column('step1', String)
    step2 = Column('step2', String)
    step3 = Column('step3', Text)
    step4 = Column('step4', Text)
    lang = Column('lang', Text)

    def __int__(self, id, greeting, step1, step2, step3, step4, lang):
        self.id = id
        self.greeting = greeting
        self.step1 = step1
        self.step2 = step2
        self.step3 = step3
        self.step4 = step4
        self.lang = lang


async def get_lang(user_id) -> str:
    try:
        user = await session.execute(select(User).filter_by(tg_user_id=int(user_id)))
        user = user.scalar()

        return user.lang
    except:
        return 'uz_kir'

