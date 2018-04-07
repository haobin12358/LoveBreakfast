# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
# 引用项目类
import models.model as models
import DBSession
from common.TransformToList import trans_params


# 操作user表的相关方法
class SShop():
    def __init__(self):
        """
        self.session 数据库连接会话
        self.status 判断数据库是否连接无异常
        """
        self.session, self.status = DBSession.get_session()
        pass

    #向数据库中插入数据，用于初始化数据
    def add_shop(self, shop):
        try:
            self.session.add(shop)
            self.session.commit()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()

    # 获取全部商品id
    # @trans_params
    def get_all_shops(self):
        shop_list = []
        try:
            shop_list = self.session.query(models.Shops.Sname, models.Shops.Simage, models.Shops.Sreview,
                                             models.Shops.Sdetail).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return shop_list

    # 获取商店详情
    def get_shop_detail(self, sid):
        pro_abo = None
        try:
            pro_abo = self.session.query(models.Shops.Sname, models.Shops.Simage, models.Shops.Stel,
                                             models.Shops.Sdetail).filter_by(Sid=sid).first()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return pro_abo

    # 获取全部shopid
    @trans_params
    def get_all_sid(self):
        shop_id_list = []
        try:
            shop_id_list = self.session.query(models.Shops.Sid).all()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return shop_id_list

    # 根据店铺id获取全部分类与商品
    def get_pro_detail_by_sid(self, sid):
        proid_list = None
        try:
            proid_list = self.session.query(models.Products.Pid).filter_by(Sid=sid).all()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return proid_list

if __name__ == "__main__":
    shop = SShop()
    print shop.get_homepage_products()