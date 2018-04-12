# *- coding:utf8 *-
import DBSession
global session


# service 基础类
class SBase():
    def __init__(self):
        try:
            session = DBSession.db_session()
        except Exception as e:
            print(e.message)


def close_session(fn):
    def inner(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            print(e.message)
            session.rollback()
        finally:
            session.close()
    return inner
