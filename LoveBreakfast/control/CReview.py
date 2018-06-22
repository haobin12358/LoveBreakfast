# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import uuid
import json
from services.SProduct import SProduct
from common.get_str import get_str
from common.import_status import import_status
from services.SReview import SReview
from control.COrders import COrders
from services.SUsers import SUsers
from services.SOrders import SOrders
from config.response import PARAMS_MISS, SYSTEM_ERROR
from common.TransformToList import add_model
from common.get_model_return_list import get_model_return_dict, get_model_return_list


class CReview():
    def __init__(self):
        self.service_product = SProduct()
        self.service_review = SReview()
        self.control_order = COrders()
        self.service_user = SUsers()
        self.service_order = SOrders()
        self.title = '============{0}============'

    def create_review(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args.keys() or "OMid" not in args.keys():
            return PARAMS_MISS

        USid = get_str(args, "token")
        OMid = get_str(args, "OMid")
        OMstatus = self.service_order.get_omstatus_by_omid(OMid)
        if OMstatus >= 49:
            return import_status("ERROR_MESSAGE_WRONG_OMSTATUS", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_OMSTATUS")

        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        for row in data:
            print(self.title.format("data_item"))
            print(row)
            print(self.title.format("data_item"))
            if "PRid" not in row or "REscore" not in row:
                return PARAMS_MISS
            if "REcontent" in data:
                REcontent = row["REcontent"]
            else:
                REcontent = None
            PRid = row["PRid"]
            REscore = row["REscore"]
            try:
                add_model("Review",
                          **{
                              "REid": str(uuid.uuid1()),
                              "OMid": OMid,
                              "PRid": PRid,
                              "USid": USid,
                              "REscore": REscore,
                              "REcontent": REcontent,
                              "REstatus": 1
                          })
            except Exception as e:
                print(self.title.format("add_review"))
                print(e.message)
                print(self.title.format("add_review"))
                return SYSTEM_ERROR

            product_volue = self.service_product.get_product_volume_by_prid(PRid)
            product_score = self.service_product.get_product_score_by_prid(PRid)

            score = (product_score * product_volue + REscore)/product_volue
            product = {
                "PRscore": score
            }
            update_product = self.service_product.update_product_by_prid(PRid, product)
            print(self.title.format("update_product"))
            print(update_product)
            print(self.title.format("update_product"))
            if not update_product:
                return SYSTEM_ERROR

            order = {
                "OMstatus": 49
            }
            update_order = self.service_order.update_ordermain_by_omid(OMid, order)
            print(self.title.format("update_order"))
            print(update_order)
            print(self.title.format("update_order"))
            if not update_order:
                return SYSTEM_ERROR

        back_response = import_status("SUCCESS_MESSAGE_ADD_REVIEW", "OK")
        return back_response

    def get_review(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))

        if "OMid" not in args.keys() or "token" not in args.keys():
            return PARAMS_MISS

        USid = get_str(args, "token")
        # TODO USid的作用？

        OMid = get_str(args, "OMid")

        all_review = get_model_return_list(self.service_review.get_review(OMid))
        print(self.title.format("all_review"))
        print(all_review)
        print(self.title.format("all_review"))
        if not all_review:
            return SYSTEM_ERROR

        for row in all_review:
            product = get_model_return_dict(self.service_product.get_product_all_by_pid(row.get("PRid")))
            print(self.title.format("product"))
            print(product)
            print(self.title.format("product"))
            if not product:
                return SYSTEM_ERROR
            row.update(product)

        back_response = import_status("SUCCESS_MESSAGE_ADD_REVIEW", "OK")
        back_response["data"] = all_review
        return back_response

    def delete_user_review(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "Uid" not in args.keys() or "Rid" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        uid_to_str = get_str(args, "Uid")
        uid_list = []
        if uid_to_str not in uid_list:
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        rid_to_str = get_str(args, "Rid")
        rid_list = self.service_review.get_rid_by_uid(uid_to_str)
        if rid_to_str not in rid_list:
            message, status, statuscode = import_status("NO_THIS_REVIEW", "response_error", "NO_THIS_REVIEW")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        result = self.service_review.delete_user_review(rid_to_str)
        print(request)
        return {
            "message": "delete review success !",
            "status": 200,
        }