# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok as ok
from common.get_model_return_list import get_model_return_list


class CCarts():
    def __int__(self):
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

        from services.SCarts import SCarts
        self.scart = SCarts()
        from services.SProduct import SProduct
        self.spro = SProduct()

    def get_carts_by_uid(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss

        #todo uid 验证未实现
        uid = args.get("token")
        res_get_all = {}

        try:
            cart_info_list = []
            cart_list = self.scart.get_carts_by_Uid(uid)
            for cart in cart_list:
                cart_info = get_model_return_list(self.spro.get_all_pro_fro_carts(cart.Pid))
                cart_info["Pnum"] = cart.Pnum
                cart_info_list.append(cart_info)
            res_get_all["data"] = cart_info_list
            res_get_all["status"] = ok
            from config.messages import messages_get_cart_success as msg
            res_get_all["message"] = msg

        except Exception as e:
            print(e.message)
            return self.system_error

    def add_or_update_cart(self):
        args = request.args.to_dict()
        data = request.data
        if "token" not in args:
            return self.param_miss
        uid = args.get("token")
        pid = data.get("Pid")
        pnum = data.get("Pnum")
        cid = self.scart.get_cart_by_uid_pid(uid, pid)
        try:
            if cid:
                self.scart.update_num_cart(pnum, cid)
            else:
                self.scart.add_carts(
                    {
                        "Cid": str(uuid.uuid4()),
                        "Pnum": pnum,
                        "Uid": uid,
                        "Cstatus": 1,
                        "Pid": pid
                    })
        except Exception as e:
            print(e.message)
            return self.system_error

        from config.messages import messages_add_cart as msg
        return {"status": ok, "message":  msg}

    def del_cart(self):
        args = request.args.to_dict()
        data = request.data
        if "token" not in args:
            return self.system_error
        uid = args.get("token")
        pid = data.get("Pid")
        try:
            cid = self.scart.get_cart_by_uid_pid(uid, pid)
            if not cid:
                from config.status import response_system_error as status
                from config.status_code import error_cart_no_pro as code
                from config.messages import error_messages_cart_no_pro as msg
                return {"status": status, "statuscode": code, "message": msg}
            self.scart.del_carts(cid)
            from config.messages import messages_del_cart as msg
            return {"status": ok, "message": msg}
        except Exception as e:
            print(e.message)
            return self.system_error
