# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
import models.model as model
from common.ErrorManager import dberror
import sqlalchemy.util._collections.result


# 装饰器，用来解析数据库获取的内容，将获取到的对象转置为dict，将获取到的单个数据的tuple里的数据解析出来
def transmodel(func):
    def inner(*args, **kwargs):
        params = func(*args, **kwargs)
        result = []
        if params:
            for param in params:
                if isinstance(param, (list, tuple)):
                    data = param[0]
                    # 如果发现解析的数据是Unicode 转置为utf-8
                    if isinstance(data, unicode):
                        data = data.encode("utf8")
                    result.append(data)
                elif isinstance(param, model.Base):
                    param_dict = param.__dict__
                    for param_key in param_dict:
                        # 所有的model的dict里都有这个不需要的参数，所以删除掉
                        if param_key == "_sa_instance_state":
                            continue
                        # 如果发现解析到的数据是Unicode 转置为utf-8
                        if isinstance(param_dict.get(param_key), unicode):
                            param_dict[param_key] = param_dict.get(param_key).encode("utf8")

                    result.append(param_dict)
                else:
                    result = params
        return result

    return inner


def closesession(fn):

    def transresulttodict(model_params):
        item_dict = model_params.keys()
        model_item = {}
        for index, key in enumerate(item_dict):
            model_item[key] = model_params[index]
        return model_item

    def resultmanager(result):
        if isinstance(result, list):
            returnlist = []
            for params in result:
                if isinstance(params, (list, tuple)):
                    returnlist.append(params[0])
                else:
                    returnlist.append(transresulttodict(params))
            return returnlist
        elif isinstance(result, result):
            return transresulttodict(result)

        return result

    def sessionmanager(self, *args, **kwargs):
        try:
            result = fn(self, *args, **kwargs)
            self.session.commit()
            return result
        except Exception as e:
            print("DBERROR" + e.message)
            self.session.rollback()
            raise dberror(e.message)
        finally:
            self.session.close()

    return sessionmanager

