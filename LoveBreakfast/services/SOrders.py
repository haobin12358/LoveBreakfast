# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
from LoveBreakfast.models.model import Ordermain, Orderpart
from LoveBreakfast.services.SBase import SBase, close_session


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
                                  Ordermain.OMtotal, Ordermain.OMcode).filter_by(
            USid=uid).order_by(Ordermain.OMtime.desc()).all()

    @close_session
    def get_order_item_by_oid(self, oid):
        return self.session.query(Orderpart.PRnumber, Orderpart.PRid).filter_by(OMid=oid).all()

    @close_session
    def get_order_abo_by_oid(self, oid):
        return self.session.query(Ordermain.OMid, Ordermain.OMtime, Ordermain.OMtotal,
                                  Ordermain.OMdate, Ordermain.AAid,
                                  Ordermain.OMcode, Ordermain.OMabo, Ordermain.OMstatus) \
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
        return self.session.query(Ordermain.OMtotal).filter_by(OMid=omid).scalar()

    @close_session
    def update_omstatus_by_omid(self, omid, order_main):
        self.session.query(Ordermain).filter_by(OMid=omid).update(order_main)
        return True

    @close_session
    def get_order_main_by_code(self, omcode):
        return self.session.query(Ordermain.OMid, Ordermain.OMcode)\
            .filter(Ordermain.OMcode == omcode, Ordermain.OMstatus < 42).first()
    
    @close_session
    def del_order(self, omid):
        self.session.query(Ordermain).filter(Ordermain.OMid == omid).delete()


if __name__ == "__main__":
    sorder = SOrders()
