# *- coding:utf8 *-
# 兼容linux系统
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
# 引用项目类
from models import model
import DBSession


# 操作user表的相关方法
class SReview():
    def __init__(self):
        """
        self.session 数据库连接会话
        self.status 判断数据库是否连接无异常
        """
        self.session, self.status = DBSession.get_session()
        pass

    # 创建评论
    def create_review(self, review):
        try:
            print(1)
            self.session.add(review)
            self.session.commit()
            return True
        except Exception as e:
            print e.message
            self.session.rollback()
        finally:
            self.session.close()

    # 根据oid获取评论信息
    def get_review(self, oid):
        review_list = None
        try:
            review_list = self.session.query(model.Review.PRid, model.Review.REscore,
                                             model.Review.REcontent).filter_by(OMid=oid).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return review_list

    # 根据用户id获取评论信息
    # def get_user_review(self, uid):
    #     try:
    #         review_of_service = self.session.query(model.Review.REid, model.Review.REscore, model.Review.Rpname, model.Review.Rpimage,
    #                                                model.Review.Rcontent).filter_by(Uid=uid, Rstatus="on").all()
    #     except Exception as e:
    #         print e.message
    #     finally:
    #         self.session.close()
    #     return review_of_service

    # 根据用户id获取评论id列表
    def get_rid_by_uid(self, uid):
        review_list = None
        try:
            review_list = self.session.query(model.Review.REid).filter_by(USid=uid).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return review_list

    def delete_user_review(self, rid):
        try:
            self.session.query(model.Review).filter_by(Rid=rid).update(Rstatus="off")
        except Exception as e:
            print e.message
        finally:
            self.session.close()
