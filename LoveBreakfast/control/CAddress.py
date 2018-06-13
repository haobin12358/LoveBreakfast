# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import request
from common.get_model_return_list import get_model_return_dict, get_model_return_list
from common.get_str import get_str
from common.import_status import import_status


class CAddress():
    def __init__(self):
        from config.status import response_error
        from config.status_code import error_param_miss
        from config.messages import error_messages_param_miss
        self.param_miss = {}
        self.param_miss["status"] = response_error
        self.param_miss["status_code"] = error_param_miss
        self.param_miss["messages"] = error_messages_param_miss

        from config.status import response_system_error
        from config.messages import error_system_error
        self.system_error = {}
        self.system_error["status"] = response_system_error
        self.system_error["messages"] = error_system_error

        from services.SAddress import SAddress
        self.sadd = SAddress()

    def get_addfirst(self):
        """
        通过城市名称获取区域名称或者所有线路
        :return:
        """
        args = request.args.to_dict()
        print("=========args========")
        print(args)
        print("=========args========")
        if "token" not in args or "ACname" not in args or "AFtype" not in args:
            return self.param_miss

        try:
            acname = args.get("ACname")
            city = get_model_return_dict(self.sadd.get_city_by_name(acname))
            af_type = get_str(args, "AFtype")
            list_first = get_model_return_list(self.sadd.get_addfirst_by_acid_astype(city.get("ACid"), af_type))
            return_data = import_status("messages_get_area_success", "response_ok")
            return_data["data"] = list_first
            return return_data
        except Exception as e:
            print("======error========")
            print(e.message)
            print("======error========")
            return self.system_error

    def get_citys(self):
        args = request.args.to_dict()
        print("=========args========")
        print(args)
        print("=========args========")
        if "token" not in args:
            return self.param_miss
        try:
            city_list = get_model_return_list(self.sadd.get_citys())
            return_data = import_status("messages_get_area_success", "response_ok")
            return_data["data"] = city_list
            return return_data
        except Exception as e:
            print("======error========")
            print(e.message)
            print("======error========")
            return self.system_error

    def get_addsecond(self):
        args = request.args.to_dict()
        print("=========args========")
        print(args)
        print("=========args========")
        if "token" not in args or "AFid" not in args:
            return self.param_miss
        try:
            afid = get_str(args, "AFid")
            list_addsecond = get_model_return_list(self.sadd.get_addsecond_by_afid(afid))
            return_data = import_status("messages_get_area_success", "response_ok")
            return_data["data"] = list_addsecond
            return return_data
        except Exception as e:
            print("======error========")
            print(e.message)
            print("======error========")
            return self.system_error

    def get_addabo(self):
        args = request.args.to_dict()
        print("=========args========")
        print(args)
        print("=========args========")
        if "token" not in args or "ASid" not in args:
            return self.param_miss
        try:
            asid = get_str(args, "ASid")
            list_addabo = get_model_return_list(self.sadd.get_addsecond_by_afid(asid))
            return_data = import_status("messages_get_area_success", "response_ok")
            return_data["data"] = list_addabo
            return return_data
        except Exception as e:
            print("======error========")
            print(e.message)
            print("======error========")
            return self.system_error
