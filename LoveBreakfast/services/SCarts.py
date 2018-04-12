# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models.model import Cart
from common.TransformToList import trans_params
from SBase import SBase, session, close_session


class SCarts(SBase):

    def __init__(self):
        super(SCarts, self).__init__()

    @close_session
    def get_carts_by_Uid(self, uid):
        return session.query(Cart.Cid, Cart.Pid, Cart.Pnum).filter(Cart.Uid == uid, Cart.Cstatus == 1).all()

    def add_carts(self, carts):
        try:
            for cart_params in carts:
                cart = Cart()
                for key in cart.__table__.columns.keys():
                    if key in cart_params:
                        setattr(cart, key, cart_params.get(key))
                session.add(cart)
            session.commit()
        except Exception as e:
            print(e.message)
            session.rollback()
        finally:
            session.close()

    def del_carts(self, cid):
        try:
            session.query(Cart).filter(Cart.Cid).update({"Cstatus": 2})
            session.commit()
        except Exception as e:
            print(e.message)
            session.rollback()
        finally:
            session.close()

    def update_num_cart(self, pnum, cid):
        try:
            session.query(Cart).filter(Cart.Cid == cid).update({"Pnum": pnum})
            session.commit()
        except Exception as e:
            print(e.message)
            session.rollback()
        finally:
            session.close()

    def get_cart_by_uid_pid(self, uid, pid):
        return session.query(Cart.Cid).filter(Cart.Uid == uid, Cart.Pid == pid, Cart.Cstatus == 1).scalar()