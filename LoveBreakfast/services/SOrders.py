# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models import models
from common.TransformToList import trans_params

class SOrders():
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)

    def get_lid_by_lname_lno_lboxno(self, lname, lno, lboxno):
        Lid = None
        try:
            Lid = self.session.query(models.Locations.Lid)\
                .filter_by(Lname=lname).filter_by(Lno=lno).filter_by(Lboxno=lboxno).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return Lid

    def add_main_order(self, Otime, Otruetimemin, Otruetimemax, Ostatus, Oprice, Uid, Lid, Oabo):
        """
        :param Otime:
        :param Otruetimemin:
        :param Otruetimemax:
        :param Ostatus:
        :param Oprice:
        :param Uid:
        :param Lid:
        :param Oabo:
        :return:
        """
        try:
            new_add_order = models.Ordermain()
            Oid = uuid.uuid4()
            new_add_order.Oid = Oid
            new_add_order.Otime = Otime
            new_add_order.Otruetimemin = Otruetimemin
            new_add_order.Otruetimemax = Otruetimemax
            new_add_order.Ostatus = Ostatus
            new_add_order.Oprice = Oprice
            new_add_order.Uid = Uid
            new_add_order.Lid = Lid
            new_add_order.Oabo = Oabo
            self.session.add(new_add_order)
            self.session.commit()
            self.session.close()
            return Oid
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def add_order_item(self, Oid, Pid, Pnum):
        """
        :param Oid:
        :param Pid:
        :param Pnum:
        :return:
        """
        try:
            new_order_item = models.Orderpart()
            OPid = uuid.uuid4()
            new_order_item.OPid = OPid
            new_order_item.Oid = Oid
            new_order_item.Pid = Pid
            new_order_item.Pnum = Pnum
            self.session.add(new_order_item)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def update_price_by_oid(self, oid, main_order):
        try:
            self.session.query(models.Ordermain).filter_by(Oid=oid).update(main_order)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def update_status_by_oid(self, oid, order_status):
        try:
            self.session.query(models.Ordermain).filter_by(Oid=oid).update(order_status)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False