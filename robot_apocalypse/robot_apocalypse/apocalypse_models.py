# coding: utf-8
from sqlalchemy import Column, Float, Integer, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class tbl_infected(Base):
    __tablename__ = 'tbl_infected'

    ID = Column(Integer, primary_key=True)
    i_reporting_id = Column(Integer, nullable=False, server_default=text("0"))
    i_infected_id = Column(Integer, nullable=False, server_default=text("0"))
# end of tbl_infected ORM class


class tbl_inventory(Base):
    __tablename__ = 'tbl_inventory'

    ID = Column(Integer, primary_key=True)
    i_survivor_id = Column(Integer, nullable=False, server_default=text("0"))
    i_count = Column(Integer, nullable=False, server_default=text("0"))
    v_description = Column(Text, server_default=text("''"))
# end of tbl_inventory ORM class


class tbl_robots(Base):
    __tablename__ = 'tbl_robots'

    ID = Column(Integer, primary_key=True)
    v_model = Column(Text, nullable=False, unique=True)
    v_serial_number = Column(Text, nullable=False, unique=True)
    v_manufactured_date = Column(Text, nullable=False)
    v_category = Column(Text, nullable=False, server_default=text("'land'"))
# end of tbl_robots ORM class


class tbl_survivors(Base):
    __tablename__ = 'tbl_survivors'

    ID = Column(Integer, primary_key=True)
    v_name = Column(Text, nullable=False, server_default=text("''"))
    i_age = Column(Integer, server_default=text("0"))
    v_gender = Column(Text, nullable=False, server_default=text("''"))
    v_id_number = Column(Text, nullable=False, unique=True)
    r_latitude = Column(Float, server_default=text("0.0"))
    r_longitude = Column(Float, server_default=text("0.0"))
# end of tbl_survivors ORM class
