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
            all_tel = self.session.query(model.Users.UStelphone).all()
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
            new_user.USid = str(uuid.uuid4())
            new_user.UStelphone = utel
            new_user.USpassword = upwd
            new_user.USname = None
            new_user.USsex = None
            new_user.UScoin = 0
            new_user.USinvatecode = str(uuid.uuid4())  # 待设计
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
            upwd = self.session.query(model.Users.USpassword).filter_by(UStelphone=utel).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return upwd

    def get_uid_by_utel(self, utel):
        uid = None
        try:
            uid = self.session.query(model.Users.USid).filter_by(UStelphone=utel).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return uid

    def update_users_by_uid(self, uid, users):
        try:
            self.session.query(model.Users).filter_by(USid=uid).update(users)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e.message)
            self.session.rollback()
            self.session.close()
            return False

    def get_all_users_info(self, usid):
        users_info = None
        try:
            users_info = self.session.query(model.Users.USname, model.Users.UStelphone, model.Users.USsex, model.Users.UScoin,
                                            model.Users.USinvatecode)\
                .filter_by(USid=usid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return users_info

    def get_uname_utel_by_uid(self, uid):
        users = None
        try:
            users = self.session.query(model.Users.USname, model.Users.UStelphone).filter_by(USid=uid).first()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return users

    def add_users(self, **kwargs):
        try:
            user = model.Users()
            for key in user.__table__.columns.keys():
                if key in kwargs:
                    setattr(user, key, kwargs.get(key))
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            print e.message
            self.session.rollback()
        finally:
            self.session.close()
