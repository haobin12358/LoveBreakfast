# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models import model
from common.TransformToList import trans_params

class SUsers():
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)

    @trans_params
    def get_all_user_tel(self):
        all_tel = None
        try:
            all_tel = self.session.query(model.Users.Utel).all()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()

        return all_tel

    def login_users(self, utel, upwd):
        """
        :param utel:
        :param uname:
        :return:
        """
        try:
            new_user = model.Users()
            new_user.Uid = str(uuid.uuid4())
            new_user.Utel = utel
            new_user.Upwd = upwd
            new_user.Uname = None
            new_user.Usex = None
            new_user.Ucoin = 0
            new_user.Uinvate = str(uuid.uuid4())  # 待设计
            self.session.add(new_user)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def get_upwd_by_utel(self, utel):
        upwd = None
        try:
            upwd = self.session.query(model.Users.Upwd).filter_by(Utel=utel).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return upwd

    def get_uid_by_utel(self, utel):
        uid = None
        try:
            uid = self.session.query(model.Users.Uid).filter_by(Utel=utel).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return uid

    def update_users_by_uid(self, uid, users):
        try:
            self.session.query(model.Users).filter_by(Uid=uid).update(users)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def get_all_users_info(self, uid):
        users_info = None
        try:
            users_info = self.session.query(model.Users.Uname, model.Users.Utel, model.Users.Usex, model.Users.Ucoin,
                                            model.Users.Uinvate)\
                .filter_by(Uid=uid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return users_info

    def get_uname_utel_by_uid(self, uid):
        users = None
        try:
            users = self.session.query(model.Users.Uname, model.Users.Utel).filter_by(Uid=uid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return users
