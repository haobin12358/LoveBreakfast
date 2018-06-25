# *- coding:utf-8 *-

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Text, Float
from config import dbconfig as cfg

DB_PARAMS = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
    cfg.sqlenginename, cfg.username, cfg.password, cfg.host, cfg.database, cfg.charset)
mysql_engine = create_engine(DB_PARAMS, echo=False)
Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"
    USid = Column(String(64), primary_key=True)
    UStelphone = Column(String(14), nullable=False)  # 用户联系方式
    USpassword = Column(String(32), nullable=False)  # 用户密码
    USname = Column(String(64))  # 用户昵称
    USsex = Column(Integer)  # 用户性别 {101男， 102女}
    UScoin = Column(Float)  # 用户积分，根据用户购买商品生成
    USinvatecode = Column(String(64))  # 用户邀请码，算法生成待设计


class Locations(Base):
    __tablename__ = "Locations"
    LOid = Column(String(64), primary_key=True)      # 区域id
    LOparantId = Column(String(64), nullable=False)  # 父id
    LOnumber = Column(Integer, nullable=False)       # 地铁线路编号
    LOname = Column(String(64), nullable=False)      # 地铁站点名称
    LOexitNumber = Column(Integer, nullable=False)   # 地铁站点出站口编号
    LOboxnumber = Column(Integer, nullable=False)    # 箱码，具体等待业务方提供


class Products(Base):
    __tablename__ = "Products"
    PRid = Column(String(64), primary_key=True)      # 商品id
    PRname = Column(String(64), nullable=False)      # 商品名称
    PRprice = Column(Float, nullable=False)          # 商品价格
    PRstatus = Column(Integer, default=1)            # 商品状态 {1:在售状态 2:下架状态}
    PRimage = Column(String(64), nullable=False)     # 商品图片存放地址
    PRinfo = Column(Text)                            # 商品介绍
    PRsalesvolume = Column(Integer, nullable=False)  # 商品销量
    PRscore = Column(Float, nullable=True)           # 商品评分


class Review(Base):
    __tablename__ = "Review"
    REid = Column(String(64), primary_key=True)  # 评论id
    OMid = Column(String(64), nullable=False)  # 对应的订单编号
    PRid = Column(String(64), nullable=False)  # 对应的商品编号
    USid = Column(String(64), nullable=False)  # 用户id
    REscore = Column(Integer, nullable=False)  # 对应的商品评分
    REcontent = Column(Text)  # 评价内容
    REstatus = Column(Integer, default=1)  # 对应的评价状态 {1:有效评价 2:无效状态}


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
    OMid = Column(String(64), primary_key=True)         # 主订单id
    OMtime = Column(String(14), nullable=False)         # 下单时间
    OMtotal = Column(Float)                             # 订单总额
    OMdate = Column(String(14))                         # 取餐日期
    USid = Column(String(64))                           # 用户id
    AAid = Column(String(64))                           # 机器详情id
    OMcode = Column(Integer)                            # 订单取货码
    OMabo = Column(Text)                                # 订单备注
    OMstatus = Column(Integer, nullable=False)          # 订单状态 具体状态如下：
    # {0 : 已取消, 7 : 未支付, 14 : 已支付, 21 : 已接单, 28 : 已配送, 35 : 已装箱, 42 : 已完成,  49 : 已评价}
    # OMmealTimeMin = Column(String(14), nullable=False)  # 取餐时间段-起始时间
    # OMmealTimeMax = Column(String(14), nullable=False)  # 取餐时间段-最晚时间
    # LOid = Column(String(64))                           # 站点id
    # OMimage = Column(String(64))                        # 订单二维码


class Orderpart(Base):
    __tablename__ = "OrderPart"
    OPid = Column(String(64), primary_key=True)  # 分订单id
    OMid = Column(String(64), nullable=False)    # 主订单id
    PRid = Column(String(64), nullable=False)     # 商品id
    PRnum = Column(Integer, nullable=False)       # 商品数量


class Cart(Base):
    __tablename__ = "Cart"
    CAid = Column(String(64), primary_key=True)  # 购物车id
    USid = Column(String(64), nullable=False)  # 用户id
    PRid = Column(String(64), nullable=False)  # 产品id
    CAnumber = Column(Integer)  # 商品在购物车中的数量
    CAstatus = Column(Integer, default=1)  # 商品在购物车状态，1 在购物车， 2 已从购物车移除 目前直接从数据库中移除


class Coupons(Base):
    __tablename__ = "Coupon"
    COid = Column(String(64), primary_key=True)
    COfilter = Column(Float)  # 优惠券优惠条件，到达金额
    COdiscount = Column(Float)  # 折扣，值为0-1，其中0为免单
    COamount = Column(Float)  # 优惠金额，减免金额，限制最大数目
    COstart = Column(String(14))  # 优惠券的开始时间
    COend = Column(String(14))  # 优惠券的结束时间


class Cardpackage(Base):
    __tablename__ = "Cardpackage"
    CAid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False)
    CAstatus = Column(Integer, default=1)  # 卡包中优惠券的状态 {1:可使用，2: 不可使用}
    CAstart = Column(String(14))  # 卡包中优惠券的开始时间
    CAend = Column(String(14))  # 卡包中的优惠券结束时间
    COid = Column(String(64), nullable=False)


class IdentifyingCode(Base):
    __tablename__ = "IdentifyingCode"
    ICid = Column(String(64), primary_key=True)
    ICtelphone = Column(String(14), nullable=False)  # 获取验证码的手机号
    ICcode = Column(String(8), nullable=False)    # 获取到的验证码
    ICtime = Column(String(14), nullable=False)    # 获取的时间，格式为20180503100322


class BlackUsers(Base):
    __tablename__ = "BlackUsers"
    BUid = Column(String(64), primary_key=True)
    BUtelphone = Column(String(14), nullable=False)   # 黑名单电话
    BUreason = Column(Text)   # 加入黑名单的原因


class AddCity(Base):
    __tablename__ = "AddCity"
    ACid = Column(String(64), primary_key=True)
    ACname = Column(String(255))


class AddressFirst(Base):
    __tablename__ = "AddressFirst"
    AFid = Column(String(64), primary_key=True)
    AFtype = Column(Integer)  # 判断是地铁还是其他园区 {0: "地铁", 1: "生活/办公园区"}
    AFname = Column(String(64))  # 区域名称/地铁线路
    ACid = Column(String(64))  # 市id


class AddressSecond(Base):
    __tablename__ = "AddressSecond"
    ASid = Column(String(64), primary_key=True)
    ASname = Column(String(255))   # 园区名称/站点名称
    AFid = Column(String(64))


class AddressAbo(Base):
    __tablename__ = "AddressAbo"
    AAid = Column(String(64), primary_key=True)
    AAmessage = Column(Text)  # 机器地址详情
    AAimage = Column(Text)    # 机器位置示意图
    ASid = Column(String(64))


class Machinery(Base):
    __tablename__ = "Machinery"
    MAid = Column(String(64), primary_key=True)
    AAid = Column(String(64))      # 机器地址
    PRid = Column(String(64))      # 机器里有的商品
