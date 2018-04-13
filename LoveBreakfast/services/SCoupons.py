# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from models.model import Cardpackage
from SBase import SBase, close_session
from models.model import Coupons


class SCoupons(SBase):
    def __init__(self):
        super(SCoupons, self).__init__()

    @close_session
    def get_cardpackage_by_uid(self, uid):
        return self.session.query(Cardpackage).filter(Cardpackage.Uid == uid).all()

    @close_session
    def add_coupons(self, **kwargs):
        coupons = Coupons()
        for key in coupons.__table__.columns.keys():
            if key in kwargs:
                setattr(coupons, key, kwargs.get(key))
        self.session.add()

    @close_session
    def add_cardpackage(self, **kwargs):
        cardpackage = Cardpackage()
        for key in cardpackage.__table__.columns.keys():
            if key in kwargs:
                setattr(cardpackage, key, kwargs.get(key))
        self.session.add()

    @close_session
    def update_carbackage(self, cardid):
        self.session.query(Cardpackage).filter(Cardpackage.Carid == cardid).update({"Carstatus": 2})

    @close_session
    def get_coupons_by_couid(self, couid):
        self.session.query(Coupons).filter(Coupons.Couid == couid).first()
