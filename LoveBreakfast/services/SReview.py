# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from models import model
from services.SBase import SBase, closesession


class SReview(SBase):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SReview, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @closesession
    def create_review(self, review):
        self.session.add(review)
        self.session.commit()
        return True

    @closesession
    def get_review(self, oid):
        return self.session.query(model.Review.PRid, model.Review.REscore,
                                  model.Review.REcontent).filter_by(OMid=oid).all()

    @closesession
    def get_rid_by_uid(self, uid):
        return self.session.query(model.Review.REid).filter_by(USid=uid).all()
