# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from models import model
from services.SBase import SBase, close_session

class SReview(SBase):

    @close_session
    def create_review(self, review):
        self.session.add(review)
        self.session.commit()
        return True

    @close_session
    def get_review(self, oid):
        return  self.session.query(model.Review.PRid, model.Review.REscore,
                                             model.Review.REcontent).filter_by(OMid=oid).all()

    @close_session
    def get_rid_by_uid(self, uid):
        return self.session.query(model.Review.REid).filter_by(USid=uid).all()
