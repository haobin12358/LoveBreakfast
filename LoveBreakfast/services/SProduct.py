# *- coding:utf8 *-
# 兼容linux系统
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
# 引用项目类
from models import model
import DBSession
from common.TransformToList import trans_params


# 操作user表的相关方法
class SProduct():
    def __init__(self):
        """
        self.session 数据库连接会话
        self.status 判断数据库是否连接无异常
        """
        self.session, self.status = DBSession.get_session()
        pass

    # 获取所有商品信息
    def get_all(self):
        pro_list_of_service = None
        try:
            pro_list_of_service = self.session.query(model.Products.PRid, model.Products.PRname,
                                                     model.Products.PRprice,model.Products.PRimage,
                                                     model.Products.PRsalesvolume,model.Products.PRscore
                                                     ).filter_by(PRstatus=1).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        print(pro_list_of_service)
        return pro_list_of_service

    # 根据商品id获取商品详情
    def get_pro_info_by_pid(self, pid):
        pro_abo = None
        try:
            pro_abo = self.session.query(model.Products.PRname, model.Products.PRprice,
                                         model.Products.PRimage, model.Products.PRinfo).filter_by(PRid=pid).first()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return pro_abo
    # 获取所有商品id

    @trans_params
    def get_all_pid(self):
        pid_list = None
        try:
            pid_list = self.session.query(model.Products.PRid).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return pid_list

    # 根据分类id获取全部商品信息
    # def get_pro_id_by_cid(self, cid):
    #     proid_list = None
    #     try:
    #         proid_list = self.session.query(model.Products.Pname, model.Products.Pprice, model.Products.Pimage
    #                                         ).filter_by(Cid=cid).all()
    #     except Exception as e:
    #         print(e.message)
    #     finally:
    #         self.session.close()
    #     return proid_list

    #向数据库中插入数据，用于初始化数据
    def add_product(self, product):
        try:
            self.session.add(product)
            self.session.commit()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()

    def get_pprice_by_pid(self, pid):
        pprice = None
        try:
            pprice = self.session.query(model.Products.PRprice).filter_by(PRid=pid).scalar()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return pprice

    def get_product_all_by_pid(self, pid):
        product = None
        try:
            product = self.session.query(model.Products.PRname, model.Products.PRsalesvolume, model.Products.PRscore,
                                         model.Products.PRprice, model.Products.PRimage).filter_by(PRid=pid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return product

    def get_all_pro_fro_carts(self, pid):
        """
        通过pid搜索project信息
        :param pid:
        :return:
        """
        try:
            res = self.session.query(
                model.Products.PRid, model.Products.PRimage,
                model.Products.PRname, model.Products.PRstatus,
                model.Products.PRsalesvolume, model.Products.PRprice,
                model.Products.PRscore
            ).filter_by(PRid=pid).all()
            return res
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
