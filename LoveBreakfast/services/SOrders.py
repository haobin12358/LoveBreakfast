# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
import uuid
from models.model import Ordermain, Orderpart
from services.SBase import SBase, close_session


class SOrders(SBase):
    @close_session
    def add_order_item(self, Oid, Pid, OPamount):
        new_order_item = Orderpart()
        OPid = str(uuid.uuid4())
        new_order_item.OPid = OPid
        new_order_item.OMid = Oid
        new_order_item.Pid = Pid
        new_order_item.OPamount = OPamount
        self.session.add(new_order_item)
        self.session.commit()
        self.session.close()
        return True

    @close_session
    def update_price_by_oid(self, oid, main_order):
        self.session.query(Ordermain).filter_by(OMid=oid).update(main_order)
        return True

    @close_session
    def update_status_by_oid(self, oid, order_status):
        self.session.query(Ordermain).filter_by(OMid=oid).update(order_status)
        return True

    @close_session
    def get_all_order_by_uid(self, uid):
        return self.session.query(Ordermain.OMid, Ordermain.OMtime, Ordermain.OMstatus,
                                  Ordermain.OMtotal, Ordermain.OMimage).filter_by(Uid=uid).all()

    @close_session
    def get_order_item_by_oid(self, oid):
        return self.session.query(Orderpart.PRnum, Orderpart.PRid).filter_by(OMid=oid).all()

    @close_session
    def get_order_abo_by_oid(self, oid):
        return self.session.query(Ordermain.OMtime, Ordermain.OMstatus, Ordermain.OMtotal,
                                  Ordermain.LOid, Ordermain.OMabo, Ordermain.OMimage,
                                  Ordermain.OMmealTimeMax, Ordermain.OMmealTimeMin) \
            .filter_by(OMid=oid).first()

    @close_session
    def update_ordermain_by_omid(self, omid, ordermain):
        self.session.query(Ordermain).filter_by(OMid=omid).update(ordermain)
        return True

    @close_session
    def get_omstatus_by_omid(self, omid):
        return self.session.query(Ordermain.OMstatus).filter_by(OMid=omid).scalar()

    @close_session
    def get_omprice_by_omid(self, omid):
        return self.session.query(Ordermain.OMprice).filter_by(OMid=omid).scalar()

    @close_session
    def update_omstatus_by_omid(self, omid, order_main):
        self.session.query(Ordermain).filter_by(OMid=omid).update(order_main)
        return True

    @close_session
    def get_order_main_by_code(self, omcode):
        return self.session.query(Ordermain.OMid, Ordermain.OMcode)\
            .filter(Ordermain.OMcode == omcode, Ordermain.OMstatus < 42).first()


if __name__ == "__main__":
    sorder = SOrders()
