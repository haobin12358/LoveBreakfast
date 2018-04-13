# *- coding:utf8 *-
# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
sys.path.append(os.path.dirname(os.getcwd())) # 增加系统路径
#引用python类
from flask import request
import uuid
import json
#引用项目类
from services.SProduct import SProduct
from common.get_str import get_str
from common.import_status import import_status
from services.SCategory import SCategory
from services.SReview import SReview
from control.COrders import COrders
from models import model
from services.SUsers import SUsers

class CReview():
    def __init__(self):
        self.service_product = SProduct()
        self.service_review = SReview()
        self.control_order = COrders()
        self.service_user = SUsers()

    #  创建评论
    def create_review(self):
        # args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        # if len(args) != 1 or "Oid" not in args.keys():
        #     message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
        #     return {
        #         "message": message,
        #         "status": status,
        #         "statuscode": statuscode,
        #     }
        # order_to_str = get_str(args, "Oid")
        order_list = self.control_order.get_order_list()
        # if order_to_str not in order_list:
        #     message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
        #     return {
        #         "message": message,
        #         "status": status,
        #         "statuscode": statuscode,
        #     }
        form = request.data  # 获取前端发送的body体
        form = json.loads(form)
        pro_list = form["Product_list"]
        print pro_list
        for i in range(len(pro_list)):
            review = model.Review()
            Rid = uuid.uuid4()
            print(Rid)
            review.Rid = str(Rid)
            review.Oid = pro_list[i].get("Oid")
            review.Pid = pro_list[i].get("Pid")
            review.Rscore = pro_list[i].get("Rscore")
            review.Rcontent = pro_list[i].get("Rcontent")
            review.Rstatus = "on"
            result = self.service_review.create_review(review)
            print(result)
        return {
            "message": "create review success !",
            "status": 200,
        }
    # 更具Oid获取商品评论
    def get_review(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "Oid" not in args.keys() :
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
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
            review_dic["Pid"] = review_list_service[i].Pid
            review_dic["Rscore"] = review_list_service[i].Rscore
            review_dic["Rcontent"] = review_list_service[i].Rcontent
            review_list_control.append(review_dic)
        return {
            "message": "获取商品评论成功",
            "status": 200,
            "data": review_list_control
        }

    def get_user_review(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "Uid" not in args.keys():
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
        review_of_control = self.service_review.get_user_review(uid_to_str)
        review_list = []
        for i in range(len(review_of_control)):
            dict_of_review = {}
            dict_of_review["Rid"] = review_of_control[i].get("Rid")
            dict_of_review["Rpname"] = review_of_control[i].get("Rpname")
            dict_of_review["Rpimage"] = review_of_control[i].get("Rpimage")
            dict_of_review["Rscore"] = review_of_control[i].get("Rscore")
            dict_of_review["Rcontent"] = review_of_control[i].get("Rcontent")
            review_list.append(dict_of_review)
        return {
            "message": "get user revirew success !",
            "status": 200,
            "statuscode": review_list
        }

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