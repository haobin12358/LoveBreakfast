# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import DBSession
from models import model


class Slocations():
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls._instance = super(Slocations, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance

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
