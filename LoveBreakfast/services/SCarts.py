# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
# import DBsession
from models.model import Cart
# from common.TransformToList import trans_params
from SBase import SBase, close_session


class SCarts(SBase):

    def __init__(self):
        super(SCarts, self).__init__()

    @close_session
    def get_carts_by_Uid(self, uid):
        return self.session.query(Cart.Cid, Cart.Pid, Cart.Pnum).filter(Cart.Uid == uid, Cart.Cstatus == 1).all()

    def add_carts(self, carts):
        try:

            cart = Cart()
            for key in cart.__table__.columns.keys():
                if key in carts:
                    setattr(cart, key, carts.get(key))
            self.session.add(cart)
            self.session.commit()
        except Exception as e:
            print(e.message)
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def del_carts(self, cid):
        try:
            self.session.query(Cart).filter(Cart.Cid).update({"Cstatus": 2})
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

    @close_session
    def get_cart_by_uid_pid(self, uid, pid):
        return self.session.query(Cart.Cid).filter(Cart.Uid == uid and Cart.Pid == pid and Cart.Cstatus == 1).scalar()