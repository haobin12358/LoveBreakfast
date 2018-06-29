# *- coding:utf8 *-
import sys
import os
import json
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import request
from common.get_model_return_list import get_model_return_dict, get_model_return_list
from common.get_str import get_str
from common.import_status import import_status
from config.response import PARAMS_MISS, SYSTEM_ERROR
from config.cityconfig import AFTYPE


class CAddress():
    def __init__(self):
        self.title = "========={0}========="
        from services.SAddress import SAddress
        self.sadd = SAddress()

    def get_addfirst(self):
        """
        通过城市名称和类型获取区域名称或者所有线路
        :return:
        """
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "ACname" not in args or "AFtype" not in args:
            return PARAMS_MISS

        try:
            acname = args.get("ACname")
            city = get_model_return_dict(self.sadd.get_city_by_name(acname))
            if not city:
                return import_status("error_no_city", "LOVEBREAKFAST_ERROR", "error_no_city")

            print(self.title.format("city"))
            print(city)
            print(self.title.format("city"))
            af_type = get_str(args, "AFtype")
            list_first = get_model_return_list(
                self.sadd.get_addfirst_by_acid_astype(city.get("ACid"), AFTYPE.index(af_type)))
            print(self.title.format("list_first"))
            print(list_first)
            print(self.title.format("list_first"))
            return_data = import_status("messages_get_area_success", "OK")
            return_data["data"] = list_first
            return return_data
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR

    def get_citys(self):
        try:
            city_list = get_model_return_list(self.sadd.get_citys())
            if not city_list:
                return SYSTEM_ERROR
            print(self.title.format("city_list"))
            print(city_list)
            print(self.title.format("city_list"))
            for city in city_list:
                # todo 不同城市可能开通的type不同，考虑增加字段来解决
                city["AFtype"] = AFTYPE

            return_data = import_status("messages_get_area_success", "OK")
            return_data["data"] = city_list
            return return_data
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR

    def get_addsecond(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "AFid" not in args:
            return PARAMS_MISS
        try:
            afid = get_str(args, "AFid")
            list_addsecond = get_model_return_list(self.sadd.get_addsecond_by_afid(afid))
            if not list_addsecond:
                return SYSTEM_ERROR
            print(self.title.format("list_addsecond"))
            print(list_addsecond)
            print(self.title.format("list_addsecond"))
            return_data = import_status("messages_get_area_success", "OK")
            return_data["data"] = list_addsecond
            return return_data
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR

    def get_addabo(self):
        data = json.loads(request.data)
        if "CAid" not in data or "ASid" not in data:
            return PARAMS_MISS
        caid_list = data.get("CAid")
        from services.SCarts import SCarts
        from services.SMachinery import SMachinery
        scarts = SCarts()
        smach = SMachinery()
        prid_list = [scarts.get_prid_by_caid(caid) for caid in caid_list]
        aaid_mach_list = []
        for prid in prid_list:
            aaid_mach_list.extend([mach.AAid for mach in smach.get_aaid_by_prid(prid)])
        try:
            asid = get_str(data, "ASid")
            list_addabo = get_model_return_list(self.sadd.get_addabo_by_asid(asid))
            print(self.title.format("list_addabo"))
            print(list_addabo)
            print(self.title.format("list_addabo"))
            aaid_as_list = [addabo.get("AAid") for addabo in list_addabo]
            print(self.title.format("aaid_as_list"))
            print(aaid_as_list)
            print(self.title.format("aaid_as_list"))
            aaid_list = list(set(aaid_as_list).intersection(aaid_mach_list))
            print(self.title.format("aaid_list"))
            print(aaid_list)
            print(self.title.format("aaid_list"))
            if not aaid_list:
                return SYSTEM_ERROR
            import random
            index = random.randint(0, len(aaid_list) - 1)
            aaid = aaid_list[index]

            return_data = import_status("messages_get_area_success", "OK")
            return_data["data"] = list_addabo[aaid_as_list.index(aaid)]
            return return_data
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR
