# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import datetime
import uuid
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from common.lovebreakfast_error import dberror
from common.timeformate import get_db_time_str, get_web_time_str, format_forweb_no_HMS, format_for_db
from config.response import SYSTEM_ERROR, PARAMS_MISS
from common.import_status import import_status


class CCoupons():
    def __init__(self):
        self.title = "============{0}==============="
        from services.SCoupons import SCoupons
        self.scoupons = SCoupons()

    def add_cardpackage(self):
        args = request.args.to_dict()
        data = json.loads(request.data)

        if "token" not in args:
            return PARAMS_MISS
        uid = args.get("token")

        couid = data.get("COid")

        try:
            cart_pkg = self.scoupons.get_card_by_uid_couid(uid, couid)
            cend = get_db_time_str()  # 后期补充优惠券截止日期计算方法
            if cart_pkg:
                if cart_pkg.CAstatus == 2:
                    return import_status("error_coupons_used", "LOVEBREAKFAST_ERROR", "error_coupons_used")

                self.scoupons.update_carbackage(cart_pkg.CAid)
            else:
                self.scoupons.add_cardpackage(**{
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

        return import_status("messages_add_coupons_success", "OK")

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
                print(self.title.format("coupon"))
                print(coupon)
                print(self.title.format("coupon"))

                coupon["COstart"] = get_web_time_str(coupon.get("COstart"), format_forweb_no_HMS)
                coupon["COend"] = get_web_time_str(coupon.get("COend"), format_forweb_no_HMS)
                cart_pkg["CAend"] = get_web_time_str(cart_pkg.get("CAend"), format_forweb_no_HMS)
                cart_pkg["CAstart"] = get_web_time_str(cart_pkg.get("CAstart"), format_forweb_no_HMS)
                cart_pkg.update(coupon)
                if not self.check_carttime(cart_pkg):
                    continue
                cart_list.append(cart_pkg)
        except Exception as e:
            print("ERROR: " + e.message)
            return SYSTEM_ERROR
        result = import_status("messages_get_carpkg_success", "OK")
        result["data"] = cart_list
        return result

    def check_carttime(self, cartpkg):
        time_now = datetime.datetime.now().date()
        if cartpkg.get("CAend") and \
                time_now > datetime.datetime.strptime(cartpkg.get("CAend"), format_forweb_no_HMS).date():
            return False
        if cartpkg.get("CAstart") and \
                time_now < datetime.datetime.strptime(cartpkg.get("CAstart"), format_forweb_no_HMS).date():
            return False
        if cartpkg.get("COend") and \
                time_now > datetime.datetime.strptime(cartpkg.get("COend"), format_forweb_no_HMS).date():
            return False
        if cartpkg.get("COstart") and \
                time_now < datetime.datetime.strptime(cartpkg.get("COstart"), format_forweb_no_HMS).date():
            return False
        return True
