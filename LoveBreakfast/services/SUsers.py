# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
import uuid
from models import model
from common.TransformToList import trans_params
from services.SBase import SBase, closesession


class SUsers(SBase):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SUsers, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @closesession
    def login_users(self, utel, upwd, usinvatecode):
        new_user = model.Users()
        new_user.USid = str(uuid.uuid1())
        new_user.UStelphone = utel
        new_user.USpassword = upwd
        new_user.USname = None
        new_user.USsex = None
        new_user.UScoin = 0
        new_user.USinvatecode = usinvatecode
        self.session.add(new_user)
        self.session.commit()
        self.session.close()
        return True

    @closesession
    def get_upwd_by_utel(self, utel):
        return self.session.query(model.Users.USpassword).filter_by(UStelphone=utel).scalar()

    @closesession
    def update_users_by_uid(self, uid, users):
        self.session.query(model.Users).filter_by(USid=uid).update(users)
        self.session.commit()
        self.session.close()
        return True

    @closesession
    def get_all_users_info(self, usid):
        return self.session.query(model.Users.USname, model.Users.UStelphone, model.Users.USsex, model.Users.UScoin,
                                  model.Users.USinvatecode) \
            .filter_by(USid=usid).first()

    @closesession
    def get_uname_utel_by_uid(self, uid):
        return self.session.query(model.Users.USname, model.Users.UStelphone).filter_by(USid=uid).first()

    @closesession
    def get_uptime_by_utel(self, utel):
        return self.session.query(model.IdentifyingCode.ICtime).filter_by(ICtelphone=utel) \
            .order_by(model.IdentifyingCode.ICtime.desc()).first()

    @closesession
    def get_code_by_utel(self, utel):
        return self.session.query(model.IdentifyingCode.ICcode).filter_by(ICtelphone=utel) \
            .order_by(model.IdentifyingCode.ICtime.desc()).first()

    @closesession
    def add_inforcode(self, utel, code, time):
        new_infocode = model.IdentifyingCode()
        new_infocode.ICid = str(uuid.uuid1())
        new_infocode.ICtelphone = utel
        new_infocode.ICcode = code
        new_infocode.ICtime = time
        self.session.add(new_infocode)
        self.session.commit()
        self.session.close()
        return True

    @closesession
    def get_user_by_utel(self, utel):
        return self.session.query(model.Users.USid).filter_by(UStelphone=utel).first()

    @trans_params
    @closesession
    def get_all_invate_code(self):
        return self.session.query(model.Users.USinvatecode).all()

    @closesession
    def get_user_by_usid(self, usid):
        return self.session.query(model.Users.USid, model.Users.UStelphone, model.Users.USinvatecode) \
            .filter_by(USid=usid).all()
