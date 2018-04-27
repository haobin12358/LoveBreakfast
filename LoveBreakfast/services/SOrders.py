# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models import model


class SOrders():
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)

    def get_loid_by_loname_loexitNumber_loboxCode(self, LOname, LOexitNumber, LOboxCode):
        LOid = None
        try:
            LOid = self.session.query(model.Locations.LOid)\
                .filter_by(LOname=LOname).filter_by(LOexitNumber=LOexitNumber).filter_by(LOboxCode=LOboxCode).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return LOid

    def add_main_order(self, OMtime, OMmealTimeMin, OMmealTimeMax, OMstatus, OMtotal, Uid, LOid, OMabo):
        """
        :param OMtime:
        :param OMmealTimeMin:
        :param OMmealTimeMax:
        :param OMstatus:
        :param OMtotal:
        :param Uid:
        :param LOid:
        :param OMabo:
        :return:
        """
        try:
            new_add_order = model.Ordermain()
            Oid = str(uuid.uuid4())
            new_add_order.OMid = Oid
            new_add_order.OMtime = OMtime
            new_add_order.OMmealTimeMin = OMmealTimeMin
            new_add_order.OMmealTimeMax = OMmealTimeMax
            new_add_order.OMstatus = OMstatus
            new_add_order.OMtotal = OMtotal
            new_add_order.Uid = Uid
            new_add_order.LOid = LOid
            new_add_order.OMabo = OMabo
            self.session.add(new_add_order)
            self.session.commit()
            self.session.close()
            return Oid
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def add_order_item(self, Oid, Pid, OPamount):
        """
        :param Oid:
        :param Pid:
        :param OPamount:
        :return:
        """
        try:
            new_order_item = model.Orderpart()
            OPid = str(uuid.uuid4())
            new_order_item.OPid = OPid
            new_order_item.OMid = Oid
            new_order_item.Pid = Pid
            new_order_item.OPamount = OPamount
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
            self.session.query(model.Ordermain).filter_by(OMid=oid).update(main_order)
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
            self.session.query(model.Ordermain).filter_by(OMid=oid).update(order_status)
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
            all_order = self.session.query(model.Ordermain.OMid, model.Ordermain.OMtime, model.Ordermain.OMstatus,
                                           model.Ordermain.OMtotal, model.Ordermain.OMimage).filter_by(Uid=uid).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return all_order

    def get_order_item_by_oid(self, oid):
        order_item = None
        try:
            order_item = self.session.query(model.Orderpart.OPamount, model.Orderpart.Pid).filter_by(OMid=oid).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return order_item

    def get_order_abo_by_oid(self, oid):
        order_abo = None
        try:
            order_abo = self.session.query(model.Ordermain.OMtime, model.Ordermain.OMstatus, model.Ordermain.OMtotal,
                                           model.Ordermain.LOid, model.Ordermain.OMabo, model.Ordermain.OMimage,
                                           model.Ordermain.OMmealTimeMax, model.Ordermain.OMmealTimeMin)\
                .filter_by(OMid=oid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return order_abo

    def get_loname_loexitnumber_loboxcode_by_loid(self, LOid):
        location = None
        try:
            location = self.session.query(model.Locations.LOname, model.Locations.LOexitNumber, model.Locations.LOboxCode)\
                .filter_by(LOid=LOid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return location

if __name__ == "__main__":
    sorder = SOrders()
    print sorder.get_loid_by_loname_loexitNumber_loboxCode("江陵路", 1, 555)