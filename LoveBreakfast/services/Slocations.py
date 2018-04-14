# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import uuid
import DBSession
from models import model
from common.TransformToList import trans_params

class Slocations():
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)


    def get_all(self):
        all_location = None
        try:
            all_location = self.session.query(model.Locations.Lid, model.Locations.Lname, model.Locations.Litem).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return all_location

    def get_all_lno_by_lid(self, lid):
        all_lno = None
        try:
            all_lno = self.session.query(model.Locations.Lno).filter_by(Lid=lid).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return all_lno
