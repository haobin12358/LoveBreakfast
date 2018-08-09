# *- coding:utf-8 *-

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, Integer, String, Text, Float
from LoveBreakfast.config import dbconfig as cfg

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
    LOboxnumber = Column(Integer, nullable=False)      # 箱码，具体等待业务方提供


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
    REscore = Column(Float, nullable=False)  # 对应的商品评分
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
    PRnumber = Column(Integer, nullable=False)       # 商品数量


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
    COfilter = Column(Float)      # 优惠券优惠条件，到达金额
    COdiscount = Column(Float)    # 折扣，值为0-1，其中0为免单
    COamount = Column(Float)      # 优惠金额，减免金额，限制最大数目
    COstart = Column(String(14))  # 优惠券的开始时间
    COend = Column(String(14))    # 优惠券的结束时间
    COtype = Column(Integer)      # 优惠券的类型 {801 满减， 802 满折， 803 商品类目限制， 804 无限制， 805 用户类型限制}


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
    AAmessage = Column(Text)
    AAimage = Column(Text)
    ASid = Column(String(64))


class Machinery(Base):
    __tablename__ = "Machinery"
    MAid = Column(String(64), primary_key=True)
    AAid = Column(String(64))      # 机器地址
    PRid = Column(String(64))      # 机器里有的商品

#
# class Votes(Base):
#     __tablename__ = "Votes"
#     VOid = Column(String(64), primary_key=True)
#     VOtext = Column(Text, nullable=False)
#     VOchoice = Column(Integer, nullable=False)
#     VOno = Column(String(2), nullable=False)
#     VOisnull = Column(Integer, nullable=False)
#
#
# class Voteitems(Base):
#     __tablename__ = "Voteitems"
#     VIid = Column(String(64), primary_key=True)
#     VOid = Column(String(64), nullable=False)
#     VItext = Column(String(64), nullable=False)
#     VIno = Column(String(2), nullable=False)
#
#
# class Votenotes(Base):
#     __tablename__ = "Votenotes"
#     VNid = Column(String(64), primary_key=True)
#     VOno = Column(String(2), nullable=False)
#     VNtext = Column(Text)
#     VNtelphone = Column(String(14), nullable=False)


class Votes(Base):
    __tablename__ = "Votes"
    VSid = Column(String(64), primary_key=True)
    VSname = Column(Text, nullable=False)  # 问卷名称
    VScontent = Column(Text)               # 问卷描述
    VSstartTime = Column(String(14))       # 起始时间
    VSendTime = Column(String(14))         # 结束时间
    VSurl = Column(Text)                   # 前端路由
    VShead = Column(Text)                  # 问卷icon
    VSbannel = Column(Text)                # 问卷宣传banner


class Vote(Base):
    __tablename__ = "Vote"
    VOid = Column(String(64), primary_key=True)
    VOtext = Column(Text, nullable=False)
    VOtype = Column(Integer, nullable=False)    # 问题类型 {1001：单选题，1002： 多选题， 1003： 填空题}
    VOno = Column(String(2), nullable=False)    # 问题编号
    VOisnull = Column(Integer, nullable=False)  # 是否可空 {1100： 不可空， 1101：可空}
    VOunit = Column(Integer)                    # 填空题后可能涉及的单位 {1300: 站}
    VOappend = Column(Text)                     # 如果是填空题，后面的补充内容
    VSid = Column(String(64), nullable=False)   # 问卷id
    VObackgroud = Column(Text)                  # 背景图


class VoteChoice(Base):
    __tablename__ = "VoteChoice"
    VCid = Column(String(64), primary_key=True)
    VCno = Column(String(2), nullable=False)   # 选项编号
    VCtext = Column(Text, nullable=False)      # 选项描述
    VCnext = Column(String(2))                 # 选项对应下一题，可空，默认为VOid对应VOno+1
    VCtype = Column(Integer)                   # 选项类型 是否需要增加文本框{1200: 不需要，1201：需要}
    VOid = Column(String(64))                  # 问题id


class Votenotes(Base):
    __tablename__ = "Votenotes"
    VNid = Column(String(64), primary_key=True)
    VSid = Column(String(64))
    USid = Column(String(64))    # 用户ID
    VNtime = Column(String(14))  # 答题时间


class VoteResult(Base):
    __tablename__ = "VoteResult"
    VRid = Column(String(64), primary_key=True)
    VNid = Column(String(64))     # 答题记录id
    VOid = Column(String(64))     # 问题id
    VRchoice = Column(String(16))  # 选项
    VRabo = Column(Text)          # 详情： 填空和其他用
