# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from models.model import Cardpackage
from SBase import SBase, closesession
from models.model import Coupons


class SCoupons(SBase):
    def __init__(self):
        super(SCoupons, self).__init__()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SCoupons, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @closesession
    def get_cardpackage_by_uid(self, uid):

        return self.session.query(
            Cardpackage.COid, Cardpackage.CAid,
            Cardpackage.USid, Cardpackage.CAstart,
            Cardpackage.CAend, Cardpackage.CAstatus
        ).filter(Cardpackage.USid == uid).all()

    @closesession
    def update_carbackage(self, cardid):
        self.session.query(Cardpackage).filter(Cardpackage.CAid == cardid).update({"CAstatus": 2})

    @closesession
    def get_card_by_uid_couid(self, uid, couid):
        return self.session.query(
            Cardpackage.COid, Cardpackage.CAid, Cardpackage.CAstatus,
            Cardpackage.CAend, Cardpackage.CAstart, Cardpackage.USid
        ).filter(Cardpackage.USid == uid, Cardpackage.COid == couid).first()

    @closesession
    def get_coupons_by_couid(self, couid):
        return self.session.query(
            Coupons.COid, Coupons.COamount, Coupons.COdiscount,
            Coupons.COstart, Coupons.COend, Coupons.COfilter, Coupons.COtype
        ).filter(Coupons.COid == couid).first()
