# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok


class Clocations():
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

    def get_all_location(self):
        from services.Slocations import Slocations
        slocations = Slocations()
        args = request.args.to_dict()
        Lline = args["Lline"]
        Lline_no = self.get_lline_no_by_lline(Lline)
        if Lline_no == -1:
            return self.param_miss
        print Lline_no
        all_location = slocations.get_all(int(Lline_no + 1))
        print all_location
        data = []
        for row in all_location:
            data_item = {}
            data_item["Lid"] = row.LOid
            data_item["Lname"] = row.LOname
            data_item["Lline"] = row.LOnumber
            data.append(data_item)
        response = {}
        response["status"] = response_ok
        response["message"] = "成功获取数据"
        response["data"] = data
        return response

    def get_lno(self):
        args = request.args.to_dict()
        if "Lid" not in args:
            return self.param_miss
        LOid = args["Lid"]
        from services.Slocations import Slocations
        slocations = Slocations()
        all_LOexitNumber = slocations.get_all_LOexitNumber_by_LOid(LOid)
        data = []
        for row in all_LOexitNumber:
            data_item = {}
            data_item["Lno"] = row.LOexitNumber
            data.append(data_item)
        response = {}
        response["status"] = response_ok
        response["message"] = "获取数据成功"
        response["data"] = data

        return response

    def get_lline(self):
        data = []
        lline_list = ["一号线", "二号线", "四号线"]
        for row in lline_list:
            data_item = {}
            data_item["Lline"] = row
            data.append(data_item)
        response = {}
        response["status"] = response_ok
        response["message"] = "获取线路成功"
        response["data"] = data

        return response

    def get_lline_no_by_lline(self, lline):
        lline_list = ["一号线", "二号线", "四号线"]
        i = 0
        while i < 3:
            if lline == lline_list[i]:
                return i
            i = i + 1
        return -1
