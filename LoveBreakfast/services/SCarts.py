# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models.models import Cart
from common.TransformToList import trans_params
from SBase import SBase


class SCarts(SBase):
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)

    @SBase.close_session
    def get_carts_by_Uid(self, uid):
        return self.session.query(Cart.Cid, Cart.Pid, Cart.Pnum).filter(Cart.Uid == uid, Cart.Cstatus == 1).all()

    def add_carts(self, carts):
        try:
            for cart_params in carts:
                cart = Cart()
                for key in cart.__table__.columns.keys():
                    if key in cart_params:
                        setattr(cart, key, cart_params.get(key))
                self.session.add(cart)
            self.session.commit()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()

    def del_carts(self, cid):
        try:
            self.session.query(Cart).filter(Cart.Cid == cid).update({"Cstatus": 2})
            self.session.commit()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()

    def update_num_cart(self, pnum, cid):
        try:
            self.session.query(Cart).filter(Cart.Cid == cid).update({"Pnum": pnum})
            self.session.commit()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()