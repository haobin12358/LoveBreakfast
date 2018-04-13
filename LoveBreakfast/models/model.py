# *- coding:utf-8 *-

import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Text, Float
from config import dbconfig as cfg
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy.dialects.mysql import INTEGER

DB_PARAMS = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
    cfg.sqlenginename, cfg.username, cfg.password, cfg.host, cfg.database, cfg.charset)
mysql_engine = create_engine(DB_PARAMS, echo=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"
    Uid = Column(String(64), primary_key=True)
    Utel = Column(String(14), nullable=False)
    Upwd = Column(String(32), nullable=False)
    Uname = Column(String(64))
    Usex = Column(Integer)
    Ucoin = Column(Float)
    Uinvate = Column(String(64))

class Locations(Base):
    __tablename__ = "Locations"
    Lid = Column(String(64), primary_key=True)
    Litem = Column(Integer, nullable=False)
    Lname = Column(String(64), nullable=False)
    Lno = Column(Integer, nullable=False)
    Lstatus = Column(Integer, nullable=False)
    Lboxno = Column(Integer, nullable=False)

class Products(Base):
    __tablename__ = "Products"
    Pid = Column(String(64), primary_key=True)
    Pname = Column(String(64), nullable=False)
    Pprice = Column(Float, nullable=False)
    Sid = Column(String(64), nullable=True, default="0")
    Cid = Column(String(64), nullable=True, default="0")
    Pstatus = Column(String(64), nullable=False)  # 商品状态，分为on_sale和off_sale
    Pimage = Column(String(64), nullable=False)
    Pinfo = Column(Text)  # 商品介绍
    P_sales_volume = Column(Integer, nullable=False)  # 商品销量
    Pscore = Column(Integer, nullable=True)  # 商品评分

class Review(Base):
    __tablename__ = "Review"
    Rid = Column(String(64), primary_key=True)
    Oid = Column(String(64), primary_key=True)  # 对应的订单编号
    Pid = Column(String(64), primary_key=True)  # 对应的商品编号
    Rscore = Column(Integer, nullable=True)  # 对应的商品评分
    Rcontent = Column(Text)  # 评价内容

class Category(Base):
    __tablename__ = "Category"
    Cid = Column(String(64), primary_key=True)
    Cname = Column(String(64), nullable=False)
    Cstatus = Column(String(64), nullable=False)

class Shops(Base):
    __tablename__ = "Shops"
    Sid = Column(String(64), primary_key=True)
    Sname = Column(String(64), nullable=False)
    Sreview = Column(Integer, nullable=True)
    Sdetail = Column(Text, nullable=True)
    Simage = Column(String(64), nullable=False)
    Stel = Column(String(14))

class Ordermain(Base):
    __tablename__ = "OrderMain"
    Oid = Column(String(64), primary_key=True)
    Otime = Column(String(14), nullable=False)
    Otruetimemin = Column(String(14), nullable=False)
    Otruetimemax = Column(String(14), nullable=False)
    Ostatus = Column(Integer, nullable=False)
    Oprice = Column(Float)
    Uid = Column(String(64))
    Lid = Column(String(64))
    Oabo = Column(Text)

class Orderpart(Base):
    __tablename__ = "OrderPart"
    OPid = Column(String(64), primary_key=True)
    Oid = Column(String(64), nullable=False)
    Pid = Column(String(64), nullable=False)
    Pnum = Column(Integer, nullable=False)

class Cart(Base):
    __tablename__ = "Cart"
    Cid = Column(String(64), primary_key=True)
    Uid = Column(String(64), nullable=False)
    Pid = Column(String(64), nullable=False)
    Pnum = Column(Integer)
    Cstatus = Column(Integer, default=1)  # 商品在购物车状态，1 在购物车， 2 已从购物车移除


class databse_deal():
    def __init__(self):
        self.conn = pymysql.connect(host=cfg.host, user=cfg.username, passwd=cfg.password, charset=cfg.charset)
        self.cursor = self.conn.cursor()

    def create_database(self):
        sql = "create database if not exists {0} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;".format(
            cfg.database)
        print sql
        try:
            self.cursor.execute(sql)
        except Exception, e:
            print(e)
        finally:
            self.conn_close()

    def drop_database(self):
        sql = "drop database if exists {0} ;".format(
            cfg.database)
        print sql
        try:
            self.cursor.execute(sql)
        except Exception, e:
            print(e)

        finally:
            self.conn_close()

    def conn_close(self):
        self.conn.close()


def create():
    databse_deal().create_database()
    Base.metadata.create_all(mysql_engine)


def drop():
    databse_deal().drop_database()



if __name__ == "__main__":
    '''
    运行该文件就可以在对应的数据库里生成本文件声明的所有table
    如果需要清除数据库，输入drop
    如果需要创建数据库 输入任意不包含drop的字符
    '''
    action = raw_input("create database?")
    if "drop" in action:
        drop()

    else:
        create()
