# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
from models import model
from common.TransformToList import trans_params
from services.SBase import SBase, close_session


class SOrders(SBase):

    @close_session
    def get_loid_by_loname_loexitNumber_loboxCode(self, LOname, LOexitNumber, LOboxCode):
        return self.session.query(model.Locations.LOid)\
                .filter_by(LOname=LOname).filter_by(LOexitNumber=LOexitNumber).filter_by(LOboxCode=LOboxCode).scalar()

    @close_session
    def add_main_order(self, OMtime, OMmealTimeMin, OMmealTimeMax, OMstatus, OMtotal, Uid, LOid, OMabo):
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

    @close_session
    def add_order_item(self, Oid, Pid, OPamount):
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

    @close_session
    def update_price_by_oid(self, oid, main_order):
        self.session.query(model.Ordermain).filter_by(OMid=oid).update(main_order)
        self.session.commit()
        self.session.close()
        return True

    @close_session
    def update_status_by_oid(self, oid, order_status):
        self.session.query(model.Ordermain).filter_by(OMid=oid).update(order_status)
        self.session.commit()
        self.session.close()
        return True

    @close_session
    def get_all_order_by_uid(self, uid):
        return self.session.query(model.Ordermain.OMid, model.Ordermain.OMtime, model.Ordermain.OMstatus,
                                           model.Ordermain.OMtotal, model.Ordermain.OMimage).filter_by(Uid=uid).all()

    @close_session
    def get_order_item_by_oid(self, oid):
        return self.session.query(model.Orderpart.PRnum, model.Orderpart.PRid).filter_by(OMid=oid).all()

    @trans_params
    @close_session
    def get_prid_by_omid(self, omid):
        return self.session.query(model.Orderpart.PRid).filter_by(OMid=omid).all()

    @close_session
    def get_order_abo_by_oid(self, oid):
        return self.session.query(model.Ordermain.OMtime, model.Ordermain.OMstatus, model.Ordermain.OMtotal,
                                           model.Ordermain.LOid, model.Ordermain.OMabo, model.Ordermain.OMimage,
                                           model.Ordermain.OMmealTimeMax, model.Ordermain.OMmealTimeMin)\
                .filter_by(OMid=oid).first()

    @close_session
    def get_loname_loexitnumber_loboxcode_by_loid(self, LOid):
        return self.session.query(model.Locations.LOname, model.Locations.LOexitNumber, model.Locations.LOboxCode)\
                .filter_by(LOid=LOid).first()

    @close_session
    def update_ordermain_by_omid(self, omid, ordermain):
        self.session.query(model.Ordermain).filter_by(OMid=omid).update(ordermain)
        self.session.commit()
        self.session.close()
        return True

    @close_session
    def get_omstatus_by_omid(self, omid):
        return self.session.query(model.Ordermain.OMstatus).filter_by(OMid=omid).scalar()

if __name__ == "__main__":
    sorder = SOrders()
