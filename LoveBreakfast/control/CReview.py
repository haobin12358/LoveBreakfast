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
from services.SReview import SReview
from control.COrders import COrders
from models import model
from services.SUsers import SUsers
from services.SOrders import SOrders

class CReview():
    def __init__(self):
        self.service_product = SProduct()
        self.service_review = SReview()
        self.control_order = COrders()
        self.service_user = SUsers()
        self.service_order = SOrders()

    #  创建评论
    def create_review(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 2 or "token" not in args.keys() or "Oid" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        token_to_str = get_str(args, "token")
        print('token'+token_to_str)
        oid_to_str = get_str(args, "Oid")
        oid_list_service = self.service_order.get_all_order_by_uid(token_to_str)
        oid_list_control = []
        print(oid_list_service)
        if oid_list_service == None:
            message, status, statuscode = import_status("messages_error_wrong_status_code", "response_error",
                                                        "error_wrong_status_code")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        for i in range(len(oid_list_service)):
            oid = oid_list_service[i].OMid
            oid_list_control.append(oid)
        print(oid_to_str)
        if oid_to_str not in oid_list_control:
            message, status, statuscode = import_status("messages_error_wrong_status_code", "response_error",
                                                        "error_wrong_status_code")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
        else:
            # 查看订单状态是否正常
            order_abo = self.service_order.get_order_abo_by_oid(oid_to_str)
            if order_abo.OMstatus != 42:
                message, status, statuscode = import_status("messages_error_wrong_status_code", "response_error",
                                                            "error_wrong_status_code")
                return {
                    "message": message,
                    "status": status,
                    "statuscode": statuscode,
                }
        form = request.data  # 获取前端发送的body体
        form = json.loads(form)
        pro_list = form["Product_list"]
        print pro_list
        for i in range(len(pro_list)):
            review = model.Review()
            Rid = uuid.uuid4()
            review.REid = str(Rid)
            review.OMid = oid_to_str
            review.PRid = pro_list[i].get("Pid")
            review.USid = token_to_str
            review.REscore = pro_list[i].get("Rscore")
            review.REcontent = pro_list[i].get("Rcontent")
            review.REstatus = 1
            result = self.service_review.create_review(review)
            print(result)
        # 更新订单状态
        try:
            order_status = {}
            order_status["OMstatus"] = 49
            self.service_order.update_status_by_oid(oid_to_str, order_status)
        except Exception as e:
            print(e)
            from config.status import response_error
            from config.status_code import SYSTEM_ERROR
            from config.messages import error_system_error
            return {
                "message": error_system_error,
                "status": response_error,
                "statuscode": SYSTEM_ERROR,
            }
        from config.messages import create_review_success
        return {
            "message": create_review_success,
            "status": 200,
        }

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
                if order_abo.OMstatus != 49:
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