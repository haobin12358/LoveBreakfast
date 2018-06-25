# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok as ok
from common.ServiceManager import get_model_return_list, get_model_return_dict
from common.ErrorManager import dberror
from common.Tools import get_db_time_str
from config.response import PARAMS_MISS, SYSTEM_ERROR


class CCoupons():
    def __init__(self):
        from services.SCoupons import SCoupons
        self.scoupons = SCoupons()
        print("coupons service", id(self.scoupons))

    def add_cardpackage(self):
        args = request.args.to_dict()
        data = json.loads(request.data)

        if "token" not in args:
            return PARAMS_MISS
        uid = args.get("token")

        couid = data.get("COid")

        try:
            cart_pkg = self.scoupons.get_card_by_uid_couid(uid, couid)
            cend = get_db_time_str()  # TODO 后期补充优惠券截止日期计算方法
            if cart_pkg:
                if cart_pkg.CAstatus == 2:
                    from config.status import response_error as status
                    from config.status_code import error_coupon_used as code
                    from config.messages import error_coupons_used as msg
                    return {"status": status, "status_code": code, "message": msg}
                self.scoupons.update_carbackage(cart_pkg.CAid)
            else:
                self.scoupons.add_model("Cardpackage", **{
                    "CAid": str(uuid.uuid4()),
                    "USid": uid,
                    "CAstatus": 1,
                    "CAstart": get_db_time_str(),
                    "CAend": cend,
                    "COid": couid
                })
        except dberror:
            return SYSTEM_ERROR
        except Exception as e:
            print(e.message)
            return SYSTEM_ERROR

        from config.messages import messages_add_coupons_success as msg
        return {"status": ok, "message": msg}

    def get_cart_pkg(self):
        args = request.args.to_dict()
        if "token" not in args:
            return PARAMS_MISS
        uid = args.get("token")

        try:
            cart_list = []
            cart_pkgs = get_model_return_list(self.scoupons.get_cardpackage_by_uid(uid))
            for cart_pkg in cart_pkgs:
                if cart_pkg.get("CAstatus") == 2:
                    continue
                coupon = get_model_return_dict(self.scoupons.get_coupons_by_couid(cart_pkg.get("COid")))
                for key in coupon.keys():
                    cart_pkg[key] = coupon.get(key)
                cart_list.append(cart_pkg)
        except Exception as e:
            print("ERROR: " + e.message)
            return SYSTEM_ERROR
        from config.messages import messages_get_carpkg_success as msg
        return {"status": ok, "message": msg, "data": cart_list}
