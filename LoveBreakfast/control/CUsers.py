# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from LoveBreakfast.config.response import SYSTEM_ERROR, PARAMS_MISS, TIME_ERROR
from LoveBreakfast.common.import_status import import_status
from LoveBreakfast.common.get_model_return_list import get_model_return_dict
from LoveBreakfast.common.MakeToken import token_to_usid

class CUsers():
    def __init__(self):
        from LoveBreakfast.services.SUsers import SUsers
        self.susers = SUsers()
        self.title = '============{0}============'

    def register(self):
        return TIME_ERROR
        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "UStelphone" not in data or "USpassword" not in data or "UScode" not in data:
            return PARAMS_MISS

        user = self.susers.get_user_by_utel(data["UStelphone"])
        print(self.title.format("user"))
        print(user)
        print(self.title.format("user"))
        if user:
            return import_status("messages_repeat_tel", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_TELPHONE")

        UScode_dict = self.susers.get_code_by_utel(data["UStelphone"])
        print(self.title.format("UScode"))
        print(UScode_dict)
        print(self.title.format("UScode"))
        if not UScode_dict:
            return import_status("ERROR_MESSAGE_NONE_ICCODE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_ICCODE")
        UScode = UScode_dict.ICcode
        if UScode != data["UScode"]:
            return import_status("ERROR_MESSAGE_WRONG_ICCODE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_ICCODE")

        if "USinvatecode" in data:
            Uinvate = data["USinvatecode"]
            # TODO 创建优惠券

        USinvatecode = self.make_invate_code()
        is_register = self.susers.login_users(data["UStelphone"], data["USpassword"], USinvatecode)
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

        if "UStelphone" not in data or "USpassword" not in data:
            return PARAMS_MISS

        Utel = data["UStelphone"]
        usid = get_model_return_dict(self.susers.get_user_by_utel(Utel))
        print(self.title.format("usid"))
        print(usid)
        print(self.title.format("usid"))
        if not usid:
            return import_status("ERROR_MESSAGE_NONE_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_TELPHONE")

        upwd = self.susers.get_upwd_by_utel(Utel)
        if upwd != data["USpassword"]:
            return import_status("ERROR_MESSAGE_WRONG_PASSWORD", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_PASSWORD")

        back_response = import_status("SUCCESS_MESSAGE_LOGIN", "OK")
        from LoveBreakfast.common.MakeToken import usid_to_token
        token = usid_to_token(usid.get("USid"))
        back_response["data"] = {}
        back_response["data"]["token"] = token
        return back_response

    def update_info(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS
        token = args.get("token")
        Uid = token_to_usid(token)
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

        if "USname" not in data and "USsex" not in data:
            return PARAMS_MISS

        users = {}
        if "USname" in data:
            users["USname"] = data["USname"]
        if "USsex" in data:
            Usex = data["USsex"]

            if Usex == "男":
                Usex = 101
            else:
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
        data = request.data
        data = json.loads(data)
        print self.title.format("data")
        print data
        print self.title.format("data")
        if "USpasswordold" not in data or "USpasswordnew" not in data or "UStelphone" not in data:
            return SYSTEM_ERROR

        Utel = data["UStelphone"]
        list_utel = self.susers.get_all_user_tel()
        print self.title.format("list_utel")
        print list_utel
        print self.title.format("list_utel")
        if list_utel == False:
            return SYSTEM_ERROR

        if Utel not in list_utel:
            return import_status("ERROR_MESSAGE_NONE_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_TELPHONE")

        upwd = self.susers.get_upwd_by_utel(Utel)
        print self.title.format("USpassword")
        print upwd
        print self.title.format("USpassword")
        if upwd != data["USpasswordold"]:
            return import_status("ERROR_MESSAGE_WRONG_PASSWORD", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_PASSWORD")
        users = {}
        Upwd = data["USpasswordnew"]
        users["USpassword"] = Upwd
        Uid = self.susers.get_uid_by_utel(Utel)
        update_info = self.susers.update_users_by_uid(Uid, users)
        print self.title.format("update_info")
        print update_info
        print self.title.format("update_info")
        if not update_info:
            return SYSTEM_ERROR

        response_of_update_users = import_status("SUCCESS_MESSAGE_UPDATE_PASSWORD", "OK")
        return response_of_update_users

    def all_info(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS
        token = args.get("token")
        Uid = token_to_usid(token)

        users_info = get_model_return_dict(self.susers.get_all_users_info(Uid))
        print(self.title.format("users_info"))
        print(users_info)
        print(self.title.format("users_info"))
        if not users_info:
            return SYSTEM_ERROR

        if users_info.get("USsex") not in["", None]:
            Usex = users_info.get("USsex")
            if Usex == 101:
                users_info["USsex"] = "男"
            elif Usex == 102:
                users_info["USsex"] = "女"
            else:
                users_info["USsex"] = "未知性别"
        else:
            users_info["USsex"] = None

        back_response = import_status("SUCCESS_GET_MESSAGE", "OK")
        back_response["data"] = users_info
        return back_response

    def get_inforcode(self):
        return TIME_ERROR
        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))
        if "UStelphone" not in data:
            return PARAMS_MISS
        Utel = data["UStelphone"]
        # 拼接验证码字符串（6位）
        code = ""
        while len(code) < 6:
            import random
            item = random.randint(1, 9)
            code = code + str(item)

        # 获取当前时间，与上一次获取的时间进行比较，小于60秒的获取直接报错
        import datetime
        from LoveBreakfast.common.timeformate import format_for_db
        time_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(time_time, format_for_db)

        """
        utel_list = self.susers.get_user_by_utel(Utel)
        print(self.title.format("utel_list"))
        print(utel_list)
        print(self.title.format("utel_list"))
        if utel_list:
            return import_status("ERROR_MESSAGE_REPEAT_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_TELPHONE")
            """
        # 根据电话号码获取时间
        time_up = self.susers.get_uptime_by_utel(Utel)
        print(self.title.format("time_up"))
        print time_up
        print(self.title.format("time_up"))
        if time_up:
            time_up_time = datetime.datetime.strptime(time_up.ICtime, format_for_db)
            delta = time_time - time_up_time
            if delta.seconds < 60:
                return import_status("ERROR_MESSAGE_GET_CODE_FAST", "LOVEBREAKFAST_ERROR", "ERROR_CODE_GET_CODE_FAST")

        new_inforcode = self.susers.add_inforcode(Utel, code, time_str)

        print(self.title.format("new_inforcode"))
        print(new_inforcode)
        print(self.title.format("new_inforcode"))

        if not new_inforcode:
            return SYSTEM_ERROR
        from LoveBreakfast.config.Inforcode import SignName, TemplateCode
        from LoveBreakfast.common.Inforsend import send_sms
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

    def forget_pwd(self):
        data = request.data
        data = json.loads(data)
        print self.title.format("data")
        print data
        print self.title.format("data")
        if "USpasswordnew" not in data or "USpasswordnewrepeat" not in data or "UStelphone" not in data or "UScode" not in data:
            return SYSTEM_ERROR

        Utel = data["UStelphone"]
        list_utel = self.susers.get_all_user_tel()
        print self.title.format("list_utel")
        print list_utel
        print self.title.format("list_utel")
        if not list_utel:
            return SYSTEM_ERROR

        if Utel not in list_utel:
            return import_status("ERROR_MESSAGE_NONE_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_TELPHONE")

        code_in_db = self.susers.get_code_by_utel(data["UStelphone"])
        print self.title.format("code_in_db")
        print code_in_db
        print self.title.format("code_in_db")
        if not code_in_db:
            return import_status("ERROR_MESSAGE_WRONG_TELCODE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_TELCODE")
        if code_in_db.ICcode != data["UScode"]:
            return import_status("ERROR_MESSAGE_WRONG_TELCODE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_TELCODE")

        if data["USpasswordnew"] != data["USpasswordnewrepeat"]:
            return import_status("ERROR_MESSAGE_WRONG_REPEAT_PASSWORD", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_REPEAT_PASSWORD")

        users = {}
        Upwd = data["USpasswordnew"]
        users["USpassword"] = Upwd
        Uid = self.susers.get_uid_by_utel(Utel)
        update_info = self.susers.update_users_by_uid(Uid, users)
        print self.title.format("update_info")
        print update_info
        print self.title.format("update_info")
        if not update_info:
            return SYSTEM_ERROR

        response_of_update_users = import_status("SUCCESS_MESSAGE_UPDATE_PASSWORD", "OK")

        return response_of_update_users