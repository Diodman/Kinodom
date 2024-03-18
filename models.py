# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin
from eng import manager
import datetime



class WorkingFilms(Base):
    __tablename__ = 'WorkingFilms'
    id = Column(Integer, primary_key=True)
    fio = Column(String(100), nullable=False, default="")
    birthday = Column(Date, nullable=False)
    sex = Column(Boolean, default=False)
    role = Column(String(100), nullable=False, default="")

class Cinema(Base):
    __tablename__ = 'cinema'
    id = Column(Integer, primary_key=True)
    cinema_option = Column(Boolean, default=False) # False - фильм, True - сериал
    label = Column(String(20), unique=True)
    year = Column(Integer)
    country = Column(String(100))
    genre = Column(String(100))
    age_rating = Column(Integer)
    trailer_link = Column(String(500))
    description = Column(String(1000))
    director_id = Column(Integer, ForeignKey('WorkingFilms.id'))
    producer_id = Column(Integer, ForeignKey('WorkingFilms.id'))
    composer_id = Column(Integer, ForeignKey('WorkingFilms.id'))

    director = relationship("WorkingFilms", primaryjoin="Cinema.director_id == foreign(WorkingFilms.id)")
    producer = relationship("WorkingFilms", primaryjoin="Cinema.producer_id == foreign(WorkingFilms.id)")
    composer = relationship("WorkingFilms", primaryjoin="Cinema.composer_id == foreign(WorkingFilms.id)")

    image = Column(String(500), nullable=False, default="")
    href = Column(String(100), nullable=False, default="")
    note = Column(Text, doc="Подробнее")



class ParticationCinema(Base):
    __tablename__ = 'partication_cinema'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinema.id'), primary_key=True)
    participant_id = Column(Integer, ForeignKey('WorkingFilms.id'))
    cinema = relationship("Cinema", primaryjoin="ParticationCinema.cinema_name == foreign(Cinema.label)")
    cinema_name = Column(String)
    participant = relationship("WorkingFilms", primaryjoin="ParticationCinema.participant_fio == foreign(WorkingFilms.fio)")
    participant_fio = Column(String)



class ApplicationUser(Base):
    __tablename__ = 'application_user'
    id = Column(Integer, primary_key=True)
    fio = Column(String(100), nullable=False, default="")
    birthday = Column(Date, nullable=False)
    mail = Column(String(100), nullable=False, default="")
    password = Column(String(100), nullable=False, default="")


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, default="")
    mail_comer = Column(String(100), nullable=False, default="")
    mail_obrash = Column(String(100), nullable=False, default="")
    href1 = Column(String(100), nullable=False, default="")
    href2 = Column(String(100), nullable=False, default="")
    href3 = Column(String(100), nullable=False, default="")
    number = Column(Integer)


##class MovieReview(Base):
##    __tablename__ = 'movie_review'
##    id = Column(Integer, primary_key=True)
##    name = Column(String(100), nullable=False, default="")
##    data = Column(Date, nullable=False)
##    review_user = relationship('ApplicationUser', back_populates='id')
##    cinema_id = Column(Integer, ForeignKey('cinema.id'))
##    cinema_name = relationship('Cinema', back_populates='label')
##    cinema_year = relationship('Cinema', back_populates='year')
##    cinema_gener = relationship('Cinema', back_populates='genre')
##    cinema_country = relationship('Cinema', back_populates='country')
##    text_review = Column(String (1000), nullable=False, default="")
##    number_positive = Column(Integer)
##    number_negative = Column(Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    is_premium = db.Column(db.Boolean)

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()

def print_schema(table_class):
    from sqlalchemy.schema import CreateTable, CreateColumn
    print(str(CreateTable(table_class.__table__).compile(db_engine)))

def print_columns(table_class, *attrNames):
   from sqlalchemy.schema import CreateTable, CreateColumn
   c = table_class.__table__.c
   print( ',\r\n'.join((str( CreateColumn(getattr(c, attrName)).compile(db_engine)) \
                            for attrName in attrNames if hasattr(c, attrName)
               )))

@manager.user.loader
def loud_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    init_db()
    d=db_session.query(Cinema).filter(Cinema.id==1).first()
    print(d)
    #print_columns(Payment, "created")
    #print_schema(SoltButton)
