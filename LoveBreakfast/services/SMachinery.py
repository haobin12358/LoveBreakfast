# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
from services.SBase import SBase, closesession
from models.model import Machinery


class SMachinery(SBase):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SMachinery, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @closesession
    def get_pro_by_aaid(self, aaid):
        return self.session.query(Machinery.PRid).filter(Machinery.AAid == aaid).all()

    @closesession
    def get_aaid_by_prid(self, prid):
        return self.session.query(Machinery.AAid).filter(Machinery.PRid == prid).all()

    @closesession
    def get_maid_by_aaid_prid(self, aaid, prid):
        return self.session.query(Machinery.MAid).filter(Machinery.PRid == prid, Machinery.AAid == aaid).scalar()
