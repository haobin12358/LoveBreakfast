# *- coding:utf8 *-
# 兼容linux系统
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
# 引用项目类
from models.model import Products
from services.SBase import SBase, closesession


# 操作user表的相关方法
class SProduct(SBase):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SProduct, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # 获取所有商品信息
    @closesession
    def get_all(self):
        return self.session.query(
                Products.PRid, Products.PRname,
                Products.PRprice, Products.PRimage,
                Products.PRsalesvolume, Products.PRscore
            ).filter_by(PRstatus=1).all()

    # 根据商品id获取商品详情
    @closesession
    def get_pro_info_by_pid(self, pid):
        return self.session.query(Products.PRname, Products.PRprice,
                                  Products.PRimage, Products.PRinfo).filter_by(PRid=pid).first()

    # 根据分类id获取全部商品信息
    # def get_pro_id_by_cid(self, cid):
    #     proid_list = None
    #     try:
    #         proid_list = self.session.query(Products.Pname, Products.Pprice, Products.Pimage
    #                                         ).filter_by(Cid=cid).all()
    #     except Exception as e:
    #         print(e.message)
    #     finally:
    #         self.session.close()
    #     return proid_list

    @closesession
    def get_pprice_by_pid(self, pid):
        return self.session.query(Products.PRprice).filter_by(PRid=pid).scalar()

    @closesession
    def get_product_all_by_pid(self, pid):
        return self.session.query(Products.PRname, Products.PRsalesvolume, Products.PRscore,
                                  Products.PRprice, Products.PRimage).filter_by(PRid=pid).first()

    @closesession
    def get_all_pro_fro_carts(self, pid):
        """
        通过pid搜索project信息
        :param pid:
        :return:
        """
        return self.session.query(
            Products.PRid, Products.PRimage,
            Products.PRname, Products.PRstatus,
            Products.PRsalesvolume, Products.PRprice,
            Products.PRscore
        ).filter_by(PRid=pid).first()

    @closesession
    def get_product_volume_by_prid(self, prid):
        return self.session.query(Products.PRsalesvolume).filter_by(PRid=prid).scalar()

    @closesession
    def get_product_score_by_prid(self, prid):
        return self.session.query(Products.PRscore).filter_by(PRid=prid).scalar()

    @closesession
    def update_product_by_prid(self, prid, product):
        self.session.query(Products).filter_by(PRid=prid).update(product)
        return True

    @closesession
    def get_product_status_by_prid(self, prid):
        return self.session.query(Products.PRstatus).filter(Products.PRid == prid).first()
