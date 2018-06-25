# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
# import DBsession
from models.model import Cart, Machinery

from SBase import SBase, closesession
from common.TransformToList import trans_params


class SCarts(SBase):

    def __init__(self):
        super(SCarts, self).__init__()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SCarts, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @closesession
    def get_carts_by_Uid(self, uid):
        return self.session.query(Cart.CAid, Cart.PRid, Cart.CAnumber, Cart.CAstatus).filter(Cart.USid == uid).all()

    # @close_session
    # def add_carts(self, **kwargs):
    #     cart = Cart()
    #     for key in cart.__table__.columns.keys():
    #         if key in kwargs:
    #             setattr(cart, key, kwargs.get(key))
    #     self.session.add(cart)

    @closesession
    def del_carts(self, caid):
        self.session.query(Cart).filter(Cart.CAid == caid).delete()

    @closesession
    def update_num_cart(self, pnum, caid):
        self.session.query(Cart).filter(Cart.CAid == caid).update({"CAnumber": pnum, "CAstatus": 1})

    @closesession
    def get_cart_by_uid_pid(self, uid, pid):
        return self.session.query(Cart.CAid, Cart.CAnumber, Cart.CAstatus).filter(Cart.USid == uid, Cart.PRid == pid).first()

    @trans_params
    @closesession
    def get_address_list_by_prid(self, prid):
        return self.session.query(Machinery.AAid).filter_by(PRid=prid).all()

    @closesession
    def get_pbnumber_by_pbid_and_usid(self, pbid, usid):
        return self.session.query(Cart.CAnumber).filter_by(PRid=pbid).filter_by(USid=usid).scalar()

    @closesession
    def get_cart_by_prid_aaid(self, prid, aaid):
        return self.session.query(Cart.CAnumber, Cart.USid)