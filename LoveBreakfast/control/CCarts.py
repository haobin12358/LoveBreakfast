# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok as ok
from common.lovebreakfast_error import dberror
from common.TransformToList import add_model
from config.response import SYSTEM_ERROR, PARAMS_MISS
from common.import_status import import_status

class CCarts():
    def __init__(self):
        from services.SCarts import SCarts
        self.scart = SCarts()
        from services.SProduct import SProduct
        self.spro = SProduct()
        from services.SUsers import SUsers
        self.susers = SUsers()
        self.title = '============{0}============'

    def get_carts_by_uid(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS

        uid = args.get("token")
        is_user = self.susers.get_user_by_usid(uid)
        print(self.title.format("is_user"))
        print(is_user)
        print(self.title.format("is_user"))
        if not is_user:
            return import_status("ERROR_MESSAGE_NONE_USER", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_USER")

        try:
            cart_info_list = []
            cart_list = self.scart.get_carts_by_Uid(uid)
            print(self.title.format("cartlist"))
            print(cart_list)
            print(self.title.format("cartlist"))

            for cart in cart_list:
                if cart.CAstatus != 1:
                    continue
                cart_service_info = (self.spro.get_all_pro_fro_carts(cart.PRid))

                print(self.title.format("cart_service_info"))
                print(cart_service_info)
                print(self.title.format("cart_service_info"))
                if cart_service_info:
                    cart_service_info = cart_service_info[0]
                    cart_info = {}
                    cart_info["PRid"] = cart_service_info.PRid
                    cart_info["PRimage"] = cart_service_info.PRimage
                    cart_info["PRname"] = cart_service_info.PRname
                    cart_info["PRstatus"] = cart_service_info.PRstatus
                    cart_info["P_sales_volume"] = cart_service_info.PRsalesvolume
                    cart_info["Pprice"] = cart_service_info.PRprice
                    cart_info["Pscore"] = cart_service_info.PRscore
                    cart_info["Pnum"] = cart.CAnumber
                    cart_info_list.append(cart_info)

            back_response = import_status("SUCCESS_GET_MESSAGE", "OK")
            back_response["data"] = cart_info_list
            return back_response

        except Exception as e:
            print(e.message)
            return self.system_error

    def add_or_update_cart(self):
        args = request.args.to_dict()
        data = json.loads(request.data)

        if "token" not in args:
            return self.param_miss
        uid = args.get("token")
        pid = data.get("Pid")
        pnum = data.get("Pnum")
        if pnum <= 0:
            # from config.messages import error_messages_pnum_illegal as msg
            # from config.status import response_error as status
            # from config.status_code import error_pnum_illegal as code
            # return {"status": status, "statuscode": code, "message": msg}
            # elif pnum == 0:
            return self.del_cart()

        try:
            if not self.spro.get_product_all_by_pid(pid):
                from config.messages import error_messages_no_pid as msg
                from config.status import response_error as status
                from config.status_code import error_no_pid as code
                return {"status": status, "statuscode": code, "message": msg}
            cart = self.scart.get_cart_by_uid_pid(uid, pid)
            if cart:
                self.scart.update_num_cart(pnum, cart.CAid)
            else:
                add_model("Cart",
                    **{
                        "CAid": str(uuid.uuid4()),
                        "CAnumber": pnum,
                        "USid": uid,
                        "CAstatus": 1,
                        "PRid": pid
                    })
        except dberror:
            return self.system_error
        except Exception as e:
            print(e.message)
            return self.system_error

        from config.messages import messages_add_cart as msg
        return {"status": ok, "message":  msg}

    def del_cart(self):
        args = request.args.to_dict()
        data = json.loads(request.data)
        if "token" not in args:
            return self.system_error
        uid = args.get("token")
        pid = data.get("Pid")
        try:
            cart = self.scart.get_cart_by_uid_pid(uid, pid)
            if not cart:
                from config.status import response_system_error as status
                from config.status_code import error_cart_no_pro as code
                from config.messages import error_messages_cart_no_pro as msg
                return {"status": status, "statuscode": code, "message": msg}
            self.scart.del_carts(cart.CAid)
            from config.messages import messages_del_cart as msg
            return {"status": ok, "message": msg}
        except Exception as e:
            print(e.message)
            return self.system_error
