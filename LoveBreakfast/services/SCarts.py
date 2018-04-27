# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
# import DBsession
from models.model import Cart

from SBase import SBase, close_session


class SCarts(SBase):

    def __init__(self):
        super(SCarts, self).__init__()

    @close_session
    def get_carts_by_Uid(self, uid):
        return self.session.query(Cart.CAid, Cart.PRid, Cart.CAnumber, Cart.CAstatus).filter(Cart.USid == uid).all()

    # @close_session
    # def add_carts(self, **kwargs):
    #     cart = Cart()
    #     for key in cart.__table__.columns.keys():
    #         if key in kwargs:
    #             setattr(cart, key, kwargs.get(key))
    #     self.session.add(cart)

    @close_session
    def del_carts(self, caid):
        self.session.query(Cart).filter(Cart.CAid == caid).delete()

    @close_session
    def update_num_cart(self, pnum, caid):
        self.session.query(Cart).filter(Cart.CAid == caid).update({"CAnumber": pnum, "CAstatus": 1})

    @close_session
    def get_cart_by_uid_pid(self, uid, pid):
        return self.session.query(Cart.CAid, Cart.CAnumber, Cart.CAstatus).filter(Cart.USid == uid, Cart.PRid == pid).first()