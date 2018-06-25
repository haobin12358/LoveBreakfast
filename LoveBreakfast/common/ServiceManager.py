# *- coding:utf8 *-


class ServiceManager(object):
    def __init__(self):
        from services.SBase import SBase
        self.sbase = SBase()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ServiceManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_model_return_list(self, model_list):
        """
        从数据库中获取到的list(列表)中每一个是一个数据库查询结果对象，
        在这里将每一个结果对象转置为dict(字典)
        :param model_list: 从数据库中直接获取到的list
        :return: 转置后的list
        """
        model_return_list = []
        for item in model_list:
            model_item = self.get_model_return_dict(item)
            model_return_list.append(model_item)
        return model_return_list

    def get_model_return_dict(self, model_params):
        """
        专门处理first数据
        :param model_params:
        :return:
        """

        item_dict = model_params.keys()
        model_item = {}
        for index, key in enumerate(item_dict):
            model_item[key] = model_params[index]
        return model_item
