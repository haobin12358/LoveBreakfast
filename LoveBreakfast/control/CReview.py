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
from models import model
from services.SUsers import SUsers
from services.SOrders import SOrders
from config.response import PARAMS_MISS, SYSTEM_ERROR
from common.TransformToList import add_model

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
        # 判断url参数是否异常
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        if "token" not in args.keys() or "Oid" not in args.keys():
            return PARAMS_MISS

        USid = get_str(args, "token")
        OMid = get_str(args, "Oid")

        data = request.data
        data = json.loads(data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        for row in data:
            print(self.title.format("data_item"))
            print(row)
            print(self.title.format("data_item"))
            if "Pid" not in row or "Rscore" not in row:
                return PARAMS_MISS
            if "Rcontent" in data:
                REcontent = row["Rcontent"]
            else:
                REcontent = None
            PRid = row["Pid"]
            REscore = row["Rscore"]
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
                "PRscore":score
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

    # 根据Oid获取商品评论
    def get_review(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 2 or "Oid" not in args.keys() or "token" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        # 验证是否存在该订单
        token_to_str = get_str(args, "token")
        oid_to_str = get_str(args, "Oid")
        oid_list_service = self.service_order.get_all_order_by_uid(token_to_str)
        if oid_list_service != None:
            oid_list_control = []
            for i in range(len(oid_list_service)):
                oid = oid_list_service[i].OMid
                oid_list_control.append(oid)
            if oid_to_str in oid_list_control:
                # 查看订单状态是否正常
                order_abo = self.service_order.get_order_abo_by_oid(oid_to_str)
                if order_abo.Ostatus != 49:
                    message, status, statuscode = import_status("messages_error_wrong_status_code", "response_error",
                                                                "error_wrong_status_code")
                    return {
                        "message": message,
                        "status": status,
                        "statuscode": statuscode,
                    }
            oid_to_str = get_str(args, "Oid")
            review_list_service = self.service_review.get_review(oid_to_str)
            print(review_list_service)
            review_list_control = []
            for i in range(len(review_list_service)):
                review_dic = {}
                review_dic["Pid"] = review_list_service[i].PRid
                review_dic["Rscore"] = review_list_service[i].REscore
                review_dic["Rcontent"] = review_list_service[i].REcontent
                review_list_control.append(review_dic)
            from config.messages import get_review_success
            return {
                "message": get_review_success,
                "status": 200,
                "data": review_list_control
            }
        else:
            from config.status import response_error
            from config.status_code import SYSTEM_ERROR
            from config.messages import error_system_error
            return {
                "message": error_system_error,
                "status": response_error,
                "status_code": SYSTEM_ERROR

            }

    # def get_user_review(self):
    #     args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
    #     # 判断url参数是否异常
    #     if len(args) != 1 or "Uid" not in args.keys():
    #         message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
    #         return {
    #             "message": message,
    #             "status": status,
    #             "statuscode": statuscode,
    #         }
    #     uid_to_str = get_str(args, "Uid")
    #     uid_list = []
    #     if uid_to_str not in uid_list:
    #         message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
    #         return {
    #             "message": message,
    #             "status": status,
    #             "statuscode": statuscode,
    #         }
    #     review_of_control = self.service_review.get_user_review(uid_to_str)
    #     review_list = []
    #     for i in range(len(review_of_control)):
    #         dict_of_review = {}
    #         dict_of_review["Rid"] = review_of_control[i].get("Rid")
    #         dict_of_review["Rpname"] = review_of_control[i].get("Rpname")
    #         dict_of_review["Rpimage"] = review_of_control[i].get("Rpimage")
    #         dict_of_review["Rscore"] = review_of_control[i].get("Rscore")
    #         dict_of_review["Rcontent"] = review_of_control[i].get("Rcontent")
    #         review_list.append(dict_of_review)
    #     return {
    #         "message": "get user revirew success !",
    #         "status": 200,
    #         "statuscode": review_list
    #     }

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