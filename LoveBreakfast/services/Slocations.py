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


    def get_all(self, lline):
        all_location = None
        try:
            all_location = self.session.query(model.Locations.LOid, model.Locations.LOname, model.Locations.LOnumber)\
                .filter_by(LOnumber=lline).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return all_location

    def get_all_LOexitNumber_by_LOid(self, LOid):
        all_LOexitNumber = None
        try:
            all_LOexitNumber = self.session.query(model.Locations.LOexitNumber).filter_by(LOid=LOid).all()
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
        return all_LOexitNumber
