# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.response import SYSTEM_ERROR, PARAMS_MISS
from common.import_status import import_status

class CUsers():
    def __init__(self):
        from services.SUsers import SUsers
        self.susers = SUsers()
        self.title = '============{0}============'

    def register(self):
        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "Utel" not in data or "Upwd" not in data or "UScode" not in data:
            return PARAMS_MISS

        list_utel = self.susers.get_user_by_utel(data["Utel"])
        print(self.title.format("list_utel"))
        print(list_utel)
        print(self.title.format("list_utel"))
        if not list_utel:
            return SYSTEM_ERROR

        if data["Utel"] in list_utel:
            return import_status("ERROR_MESSAGE_REPEAT_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_TELPHONE")

        UScode_dict = self.susers.get_code_by_utel(data["Utel"])
        print(self.title.format("UScode"))
        print(UScode_dict)
        print(self.title.format("UScode"))
        if not UScode_dict:
            return import_status("ERROR_MESSAGE_NONE_ICCODE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_ICCODE")
        UScode = UScode_dict.ICcode
        if UScode != data["UScode"]:
            return import_status("ERROR_MESSAGE_WRONG_ICCODE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_ICCODE")

        if "Uinvate" in data:
            Uinvate = data["Uinvate"]
            # TODO 创建优惠券

        USinvatecode = self.make_invate_code()
        is_register = self.susers.login_users(data["Utel"], data["Upwd"], USinvatecode)
        print(self.title.format("is_register"))
        print(is_register)
        print(self.title.format("is_register"))
        if not is_register:
            return SYSTEM_ERROR

        back_response = import_status("SUCCESS_MESSAGE_REGISTER_OK", "OK")
        return back_response

    def make_invate_code(self):
        USinvate = self.susers.get_all_invate_code()
        while True:
            invate_code = self.make_random_code()
            if invate_code not in USinvate:
                break
        return invate_code

    def make_random_code(self):
        import random
        random_code = ""
        while len(random_code) < 2:
            a = random.randint(97, 122)
            a = chr(a)
            random_code = random_code + a
        while len(random_code) < 6:
            a = random.randint(0, 9)
            random_code = random_code + str(a)
        return random_code

    def login(self):
        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "Utel" not in data or "Upwd" not in data:
            return PARAMS_MISS

        Utel = data["Utel"]
        list_utel = self.susers.get_user_by_utel(Utel)
        print(self.title.format("list_utel"))
        print(list_utel)
        print(self.title.format("list_utel"))
        if not list_utel:
            return SYSTEM_ERROR

        if Utel not in list_utel:
            return import_status("ERROR_MESSAGE_NONE_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_TELPHONE")

        upwd = self.susers.get_upwd_by_utel(Utel)
        if upwd != data["Upwd"]:
            return import_status("ERROR_MESSAGE_WRONG_PASSWORD", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_PASSWORD")

        Uid = self.susers.get_uid_by_utel(Utel)

        back_response = import_status("SUCCESS_MESSAGE_LOGIN", "OK")
        back_response["data"]["token"] = Uid
        return back_response

    def update_info(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS
        Uid = args["token"]
        is_user = self.susers.get_user_by_usid(Uid)
        print(self.title.format("is_user"))
        print(is_user)
        print(self.title.format("is_user"))
        if not is_user:
            return import_status("ERROR_MESSAGE_NONE_USER", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_USER")

        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "Uname" not in data and "Usex" not in data:
            return PARAMS_MISS

        users = {}
        if "Uname" in data:
            Uname = data["Uname"]
            users["USname"] = Uname
        if "Usex" in data:
            Usex = data["Usex"]
            if Usex == "男":
                Usex = 101
            elif Usex == "女":
                Usex = 102
            users["USsex"] = Usex

        update_info = self.susers.update_users_by_uid(Uid, users)
        print(self.title.format("update_info"))
        print(update_info)
        print(self.title.format("update_info"))
        if not update_info:
            return SYSTEM_ERROR

        back_response = import_status("SUCCESS_MESSAGE_UPDATE_INFO", "OK")
        return back_response

    def update_pwd(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS
        Uid = args["token"]
        is_user = self.susers.get_user_by_usid(Uid)
        print(self.title.format("is_user"))
        print(is_user)
        print(self.title.format("is_user"))
        if not is_user:
            return import_status("ERROR_MESSAGE_NONE_USER", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_USER")

        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "Upwd" not in data:
            return PARAMS_MISS

        users = {}
        Upwd = data["Upwd"]
        users["USpassword"] = Upwd

        update_info = self.susers.update_users_by_uid(Uid, users)
        print(self.title.format("update_info"))
        print(update_info)
        print(self.title.format("update_info"))
        if not update_info:
            return SYSTEM_ERROR

        back_response = import_status("SUCCESS_MESSAGE_UPDATE_PASSWORD", "OK")
        return back_response

    def all_info(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS
        Uid = args["token"]

        users_info = self.susers.get_all_users_info(Uid)
        print(self.title.format("users_info"))
        print(users_info)
        print(self.title.format("users_info"))
        if not users_info:
            return SYSTEM_ERROR

        response_data = {}
        Utel = users_info.UStelphone
        response_data["Utel"] = Utel
        if users_info.USname not in ["", None]:
            Uname = users_info.USname
            response_data["Uname"] = Uname
        else:
            response_data["Uname"] = None
        if users_info.USsex not in["", None]:
            Usex = users_info.USsex
            if Usex == 101:
                response_data["Usex"] = "男"
            elif Usex == 102:
                response_data["Usex"] = "女"
            else:
                response_data["Usex"] = "未知性别"
        else:
            response_data["Usex"] = None
        response_data["Ucoin"] = users_info.UScoin
        response_data["Uinvate"] = users_info.USinvatecode

        back_response = import_status("SUCCESS_GET_MESSAGE", "OK")
        back_response["data"] = response_data
        return back_response


    def get_inforcode(self):
        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))
        if "Utel" not in data:
            return PARAMS_MISS
        Utel = data["Utel"]
        # 拼接验证码字符串（6位）
        code = ""
        while len(code) < 6:
            import random
            item = random.randint(1,9)
            code = code + str(item)

        # 获取当前时间，与上一次获取的时间进行比较，小于60秒的获取直接报错
        import datetime
        time_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(time_time, "%Y%m%d%H%M%S")

        utel_list = self.susers.get_user_by_utel(Utel)
        print(self.title.format("utel_list"))
        print(utel_list)
        print(self.title.format("utel_list"))
        if not utel_list:
            return import_status("ERROR_MESSAGE_REPEAT_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_TELPHONE")
        # 根据电话号码获取时间
        time_up = self.susers.get_uptime_by_utel(Utel)
        print(self.title.format("time_up"))
        print time_up
        print(self.title.format("time_up"))
        if time_up:
            time_up_time = datetime.datetime.strptime(time_up.ICtime, "%Y%m%d%H%M%S")
            delta = time_time - time_up_time
            if delta.seconds < 60:
                return import_status("ERROR_MESSAGE_GET_CODE_FAST", "LOVEBREAKFAST_ERROR", "ERROR_CODE_GET_CODE_FAST")

        new_inforcode = self.susers.add_inforcode(Utel, code, time_str)
        print(self.title.format("new_inforcode"))
        print(new_inforcode)
        print(self.title.format("new_inforcode"))

        if not new_inforcode:
            return SYSTEM_ERROR
        from config.Inforcode import SignName, TemplateCode
        from common.Inforsend import send_sms
        params = '{\"code\":\"' + code + '\",\"product\":\"etech\"}'

        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        __business_id = uuid.uuid1()
        response_send_message = send_sms(__business_id, Utel, SignName, TemplateCode, params)

        response_send_message = json.loads(response_send_message)
        print(self.title.format("response_send_message"))
        print(response_send_message)
        print(self.title.format("response_send_message"))

        if response_send_message["Code"] == "OK":
            status = 200
        else:
            status = 405
        response_ok = {}
        response_ok["status"] = status
        response_ok["messages"] = response_send_message["Message"]

        return response_ok
