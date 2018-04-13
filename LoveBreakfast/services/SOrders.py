# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models import model
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
            Lid = self.session.query(model.Locations.Lid)\
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
            new_add_order = model.Ordermain()
            Oid = str(uuid.uuid4())
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
            new_order_item = model.Orderpart()
            OPid = str(uuid.uuid4())
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
            self.session.query(model.Ordermain).filter_by(Oid=oid).update(main_order)
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
            # add 和 update 修改
            self.session.query(model.Ordermain).filter_by(Oid=oid).update(order_status)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def get_all_order_by_uid(self, uid):
        all_order = None
        try:
            all_order = self.session.query(model.Ordermain.Oid, model.Ordermain.Otime, model.Ordermain.Ostatus,
                                           model.Ordermain.Oprice).filter_by(Uid=uid).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return all_order

    def get_order_item_by_oid(self, oid):
        order_item = None
        try:
            order_item = self.session.query(model.Orderpart.Pnum, model.Orderpart.Pid).filter_by(Oid=oid).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return order_item

    def get_order_abo_by_oid(self, oid):
        order_abo = None
        try:
            order_abo = self.session.query(model.Ordermain.Otime, model.Ordermain.Ostatus, model.Ordermain.Oprice,
                                           model.Ordermain.Lid, model.Ordermain.Oabo).filter_by(Oid=oid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return order_abo

    def get_lname_lno_lboxno_by_lid(self, lid):
        location = None
        try:
            location = self.session.query(model.Locations.Lname, model.Locations.Lno, model.Locations.Lboxno)\
                .filter_by(Lid=lid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return location