# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from LoveBreakfast.common.lovebreakfast_error import dberror
from LoveBreakfast.common.TransformToList import add_model
from LoveBreakfast.config.response import SYSTEM_ERROR, PARAMS_MISS
from LoveBreakfast.common.import_status import import_status
from LoveBreakfast.common.MakeToken import token_to_usid

class CCarts():
    def __init__(self):
        from LoveBreakfast.services.SCarts import SCarts
        self.scart = SCarts()
        from LoveBreakfast.services.SProduct import SProduct
        self.spro = SProduct()
        from LoveBreakfast.services.SUsers import SUsers
        self.susers = SUsers()
        from LoveBreakfast.services.SProduct import SProduct
        self.sproduct = SProduct()
        from LoveBreakfast.services.SAddress import SAddress
        self.sadd = SAddress()
        from LoveBreakfast.services.SMachinery import SMachinery
        self.smach = SMachinery()
        self.title = '============{0}============'

    def get_carts_by_uid(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args or "AAid" not in args:
            return PARAMS_MISS

        token = args.get("token")
        uid = token_to_usid(token)
        ASid = args.get("ASid")
        is_user = self.susers.get_user_by_usid(uid)
        print(self.title.format("is_user"))
        print(is_user)
        print(self.title.format("is_user"))
        if not is_user:
            return import_status("ERROR_MESSAGE_NONE_USER", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_USER")

        cart_info_list = []
        cart_list = self.scart.get_carts_by_Uid(uid)
        print(self.title.format("cartlist"))
        print(cart_list)
        print(self.title.format("cartlist"))
        aaid_list = self.sadd.get_addabo_by_asid(ASid)

        for cart in cart_list:
            if cart.CAstatus != 1:
                continue
            PRid = cart.PRid
            address_list = [i.AAid for i in self.smach.get_aaid_by_prid(PRid)]
            print(self.title.format("address_list"))
            print(address_list)
            print(self.title.format("address_list"))
            if not address_list:
                return SYSTEM_ERROR

            if not set(address_list).intersection(aaid_list):
                continue
            cart_service_info = self.spro.get_all_pro_fro_carts(PRid)
            print(self.title.format("cart_service_info"))
            print(cart_service_info)
            print(self.title.format("cart_service_info"))
            if not cart_service_info:
                return SYSTEM_ERROR

            cart_info = {}
            cart_info["PRid"] = cart_service_info.PRid
            cart_info["PRimage"] = cart_service_info.PRimage
            cart_info["PRname"] = cart_service_info.PRname
            cart_info["PRstatus"] = cart_service_info.PRstatus
            cart_info["PRsalesvolume"] = cart_service_info.PRsalesvolume
            cart_info["PRprice"] = cart_service_info.PRprice
            cart_info["PRscore"] = cart_service_info.PRscore
            cart_info["CAnumber"] = cart.CAnumber
            cart_info_list.append(cart_info)

        back_response = import_status("SUCCESS_GET_MESSAGE", "OK")
        back_response["data"] = cart_info_list
        return back_response

    def add_or_update_cart(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        data = json.loads(request.data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "token" not in args:
            return PARAMS_MISS
        token = args.get("token")
        uid = token_to_usid(token)
        pid = data.get("PRid")
        CAnumber = data.get("CAnumber")
        if CAnumber <= 0:
            PBnumber = self.scart.get_pbnumber_by_pbid_and_usid(pid, uid)
            pnum = int(CAnumber) + int(PBnumber)
            if pnum <= 0:
                return self.del_cart(uid, pid)
        try:
            if not self.sproduct.get_pro_info_by_pid(pid):
                return import_status("ERROR_MESSAGE_NONE_PRODUCT", "SHARPGOODS_ERROR", "ERROR_NONE_PRODUCT")
            cart = self.scart.get_cart_by_uid_pid(uid, pid)
            print(self.title.format("cart"))
            print(cart)
            print(self.title.format("cart"))
            if cart:
                PBnumber = self.scart.get_pbnumber_by_pbid_and_usid(pid, uid)
                pnum = int(CAnumber) + int(PBnumber)
                self.scart.update_num_cart(pnum, cart.CAid)
            else:
                add_model("Cart",
                          **{
                              "CAid": str(uuid.uuid1()),
                              "CAnumber": CAnumber,
                              "USid": uid,
                              "CAstatus": 1,
                              "PRid": pid
                          })
        except dberror:
            return SYSTEM_ERROR
        except Exception as e:
            print(e.message)
            return SYSTEM_ERROR

        return import_status("SUCCESS_MESSAGE_UPDATE_CART", "OK")

    def del_cart(self, uid, pid):
        try:
            cart = self.scart.get_cart_by_uid_pid(uid, pid)
            print(self.title.format("cart"))
            print(cart)
            print(self.title.format("cart"))
            if not cart:
                return import_status("ERROR_MESSAGE_NONE_PRODUCT", "LOVEBREAKFAST_ERROR", "ERROR_NONE_PRODUCT")
            self.scart.del_carts(cart.CAid)
            return import_status("SUCCESS_MESSAGE_DEL_CART", "OK")
        except Exception as e:
            print(e.message)
            return SYSTEM_ERROR

    def del_product(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS
        data = json.loads(request.data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "PRid" not in data:
            return PARAMS_MISS
        token = args.get("token")
        uid = token_to_usid(token)
        return self.del_cart(uid, data.get("PRid"))

    def get_carts_by_uid_caid(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args:
            return PARAMS_MISS

        caid_list = []

        if request.environ.get("REQUEST_METHOD") == "POST":
            data = json.loads(request.data)
            print(self.title.format("data"))
            print(data)
            print(self.title.format("data"))
            caid_list = data.get("CAid")
        token = args.get("token")
        uid = token_to_usid(token)
        ASid = args.get("ASid")

        is_user = self.susers.get_user_by_usid(uid)
        print(self.title.format("is_user"))
        print(is_user)
        print(self.title.format("is_user"))
        if not is_user:
            return import_status("ERROR_MESSAGE_NONE_USER", "LOVEBREAKFAST_ERROR", "ERROR_CODE_NONE_USER")

        aaid_list = [i.AAid for i in self.sadd.get_addabo_by_asid(ASid)]
        cart_info_list = []
        cart_list = self.scart.get_carts_by_Uid(uid)
        print(self.title.format("cartlist"))
        print(cart_list)
        print(self.title.format("cartlist"))

        for cart in cart_list:
            if cart.CAstatus != 1:
                continue
            if caid_list and cart.CAid not in caid_list:
                continue
            PRid = cart.PRid
            address_list = [i.AAid for i in self.smach.get_aaid_by_prid(PRid)]
            print(self.title.format("address_list"))
            print(address_list)
            print(self.title.format("address_list"))
            if not address_list:
                return SYSTEM_ERROR
            if not set(address_list).intersection(aaid_list):
                continue

            cart_service_info = self.spro.get_all_pro_fro_carts(PRid)
            print(self.title.format("cart_service_info"))
            print(cart_service_info)
            print(self.title.format("cart_service_info"))
            if not cart_service_info:
                return SYSTEM_ERROR

            cart_info = {}
            cart_info["PRid"] = cart_service_info.PRid
            cart_info["PRimage"] = cart_service_info.PRimage
            cart_info["PRname"] = cart_service_info.PRname
            cart_info["PRstatus"] = cart_service_info.PRstatus
            cart_info["PRsalesvolume"] = cart_service_info.PRsalesvolume
            cart_info["PRprice"] = cart_service_info.PRprice
            cart_info["PRscore"] = cart_service_info.PRscore
            cart_info["CAnumber"] = cart.CAnumber
            cart_info["CAid"] = cart.CAid
            cart_info_list.append(cart_info)

        back_response = import_status("SUCCESS_GET_MESSAGE", "OK")
        back_response["data"] = cart_info_list
        return back_response
