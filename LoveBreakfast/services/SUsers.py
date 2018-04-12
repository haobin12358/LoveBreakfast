# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
import models
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
            all_tel = self.session.query(models.Users.Utel).all()
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
            new_user = models.Users()
            new_user.Uid = uuid.uuid4()
            new_user.Utel = utel
            new_user.Upwd = upwd
            new_user.Uname = None
            new_user.Usex = None
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
            upwd = self.session.query(models.Users.Upwd).filter_by(Utel=utel).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return upwd

    def get_uid_by_utel(self, utel):
        uid = None
        try:
            uid = self.session.query(models.Users.Uid).filter_by(Utel=utel).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return uid

    def update_users_by_uid(self, uid, users):
        try:
            self.session.query(models.Users).filter_by(Uid=uid).update(users)
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
            users_info = self.session.query(models.Users.Uname, models.Users.Utel, models.Users.Usex)\
                .filter_by(Uid=uid).first()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return users_info
