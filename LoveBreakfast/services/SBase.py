# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import DBSession
import models.model as models
from common.Decorator import closesession

closesession = closesession


# service 基础类
class SBase(object):
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)

    @closesession
    def add_model(self, model_name, **kwargs):
        print(model_name)
        if not getattr(models, model_name):
            print("model name = {0} error ".format(model_name))
            return
        model_bean = eval(" models.{0}()".format(model_name))
        for key in model_bean.__table__.columns.keys():
            if key in kwargs:
                setattr(model_bean, key, kwargs.get(key))

        self.session.add(model_bean)

    @closesession
    def check_connection(self, index=0):
        if index > 3:
            raise Exception("mysql connection failed")
        try:
            self.session.execute("select 1")
            print("mysql connection successful")
        except Exception as e:
            print("mysql connection error:", e.message)
            self.check_connection(index+1)
