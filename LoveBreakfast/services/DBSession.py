# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
sys.path.append(os.path.dirname(os.getcwd())) # 增加系统路径
# 引用python类
from sqlalchemy.orm import sessionmaker
# 引用项目类
from models import models

<<<<<<< HEAD
# 实例化session
db_session = sessionmaker(bind=models.mysql_engine)
=======

# 实例化session
db_session = sessionmaker(bind=models.mysql_engine)
#db_log_session = sessionmaker(bind=log_model.mysql_engine)
>>>>>>> 99deafebef0171883d520b6ca86040379cd2b8ce


# 获取数据库连接session
def get_session():
    try:
        session = db_session()
        status = True
    except Exception as e:
        print e.message
        session = None
        status = False
    finally:
        return session, status
