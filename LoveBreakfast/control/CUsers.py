# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok


class CUsers():
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

    def register(self):
        data = request.data
        print(data)
        data = json.loads(data)

        if "Utel" not in data or "Upwd" not in data:
            return self.param_miss

        from services.SUsers import SUsers
        susers = SUsers()
        list_utel = susers.get_all_user_tel()

        if list_utel == False:
            return self.system_error

        if data["Utel"] in list_utel:
            from config.status import response_system_error
            from config.status_code import error_repeat_tel
            from config.messages import messages_repeat_tel
            repeated_tel = {}
            repeated_tel["status"] = response_system_error
            repeated_tel["status_code"] = error_repeat_tel
            repeated_tel["messages"] = messages_repeat_tel
            return repeated_tel

        if "Uinvate" in data:
            Uinvate = data["Uinvate"]
            # 创建优惠券

        is_register = susers.login_users(data["Utel"], data["Upwd"])
        if is_register:
            from config.messages import messages_regist_ok
            register_ok = {}
            register_ok["status"] = response_ok
            register_ok["messages"] = messages_regist_ok
            return register_ok
        else:
            return self.system_error

    def login(self):
        data = request.data
        print(data)
        data = json.loads(data)

        if "Utel" not in data or "Upwd" not in data:
            return self.param_miss

        Utel = data["Utel"]
        from services.SUsers import SUsers
        susers = SUsers()
        list_utel = susers.get_all_user_tel()

        if list_utel == False:
            return self.system_error

        if Utel not in list_utel:
            from config.status import response_error
            from config.status_code import error_no_utel
            from config.messages import messages_no_user
            no_utel = {}
            no_utel["status"] = response_error
            no_utel["status_code"] = error_no_utel
            no_utel["messages"] = messages_no_user
            return no_utel

        upwd = susers.get_upwd_by_utel(Utel)
        if upwd != data["Upwd"]:
            from config.status import response_error
            from config.status_code import error_wrong_pwd
            from config.messages import messages_wrong_pwd
            wrong_pwd = {}
            wrong_pwd["status"] = response_error
            wrong_pwd["status_code"] = error_wrong_pwd
            wrong_pwd["messages"] = messages_wrong_pwd
            return wrong_pwd

        Uid = susers.get_uid_by_utel(Utel)

        login_success = {}
        from config.messages import messages_login_ok
        login_success["status"] = response_ok
        login_success["messages"] = messages_login_ok
        login_success["token"] = Uid

        return login_success

    def update_info(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        data = request.data
        data = json.loads(data)

        if "Uname" not in data and "Usex" not in data:
            return self.param_miss

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

        from services.SUsers import SUsers
        susers = SUsers()
        update_info = susers.update_users_by_uid(Uid, users)

        if not update_info:
            return self.system_error

        response_of_update_users = {}
        from config.messages import messages_update_personal_ok
        response_of_update_users["status"] = response_ok
        response_of_update_users["messages"] = messages_update_personal_ok

        return response_of_update_users

    def update_pwd(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        data = request.data
        data = json.loads(data)

        if "Upwd" not in data:
            return self.param_miss

        users = {}
        Upwd = data["Upwd"]
        users["USpassword"] = Upwd

        from services.SUsers import SUsers
        susers = SUsers()
        update_info = susers.update_users_by_uid(Uid, users)

        if not update_info:
            return self.system_error

        response_of_update_users = {}
        from config.messages import messages_update_pwd_ok
        response_of_update_users["status"] = response_ok
        response_of_update_users["messages"] = messages_update_pwd_ok

        return response_of_update_users

    def all_info(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        from services.SUsers import SUsers
        susers = SUsers()
        users_info = susers.get_all_users_info(Uid)

        if not users_info:
            return self.system_error

        response_user_info = {}
        Utel = users_info.UStelphone
        response_user_info["Utel"] = Utel
        if users_info.USname not in ["", None]:
            Uname = users_info.USname
            response_user_info["Uname"] = Uname
        else:
            response_user_info["Uname"] = None
        if users_info.USsex not in["", None]:
            Usex = users_info.USsex
            if Usex == 101:
                response_user_info["Usex"] = "男"
            elif Usex == 102:
                response_user_info["Usex"] = "女"
            else:
                response_user_info["Usex"] = "未知性别"
        else:
            response_user_info["Usex"] = None
        response_user_info["Ucoin"] = users_info.UScoin
        response_user_info["Uinvate"] = users_info.USinvatecode

        response_of_get_all = {}
        response_of_get_all["status"] = response_ok
        from config.messages import messages_get_item_ok
        response_of_get_all["messages"] = messages_get_item_ok
        response_of_get_all["data"] = response_user_info
        return response_of_get_all
        