# *- coding:utf8 *-
import DBSession


# service 基础类
class SBase(object):
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            print(e.message)


def close_session(fn):
    def inner(self, *args, **kwargs):
        try:
            result = fn(self, *args, **kwargs)
            self.session.commit()
            return result
        except Exception as e:
            print(e.message)
            self.session.rollback()
        finally:
            self.session.close()
    return inner
