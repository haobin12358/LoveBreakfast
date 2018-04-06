# *- coding:utf8 *-
# 兼容linux系统
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
# 引用项目类
from models import models
import DBSession
from common.TransformToList import trans_params


# 操作user表的相关方法
class SProduct():
    def __init__(self):
        """
        self.session 数据库连接会话
        self.status 判断数据库是否连接无异常
        """
        self.session, self.status = DBSession.get_session()
        pass

    # 获取全部的商品id
    @trans_params
    def get_all_pid(self):
        pid_list = None
        try:
            pid_list = self.session.query(models.Products.Pid).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return pid_list

    def get_pprice_by_pid(self, pid):
        pprice = None
        try:
            pprice = self.session.query(models.Products.Pprice).filter_by(Pid=pid).scalar()
        except Exception as e:
            print(e.message)
        finally:
            self.session.close()
        return pprice

