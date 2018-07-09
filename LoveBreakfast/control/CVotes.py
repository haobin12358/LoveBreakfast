# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.response import SYSTEM_ERROR, PARAMS_MISS
from common.import_status import import_status
from common.TransformToList import add_model

class CVotes():
    def __init__(self):
        from services.SVotes import SVotes
        self.svotes = SVotes()
        from services.SUsers import SUsers
        self.susers = SUsers()
        self.title = '============{0}============'

    def get_all(self):
        all_vote = self.svotes.get_all_vote()
        print(self.title.format("all_vote"))
        print(all_vote)
        print(self.title.format("all_vote"))
        if not all_vote:
            return SYSTEM_ERROR
        vote_list = []
        for row in all_vote:
            vote_item = {}
            VOid = row.VOid
            VOno = row.VOno
            VOtext = row.VOtext
            VOchoice = row.VOchoice
            VOisnull = row.VOisnull
            if VOchoice == 1001:
                choice = "[单选题]"
            elif VOchoice == 1002:
                choice = "[多选题]"
            elif VOchoice == 1003:
                choice = "[填空题]"
            else:
                choice = None
            vote_item["VOid"] = VOid
            vote_item["VOno"] = VOno
            vote_item["VOtext"] = VOtext
            vote_item["VOisnull"] = VOisnull
            vote_item["VOchoice"] = choice
            if VOchoice == 1001 or VOchoice == 1002:
                vote_item["choice_items"] = []
                all_vote_items = self.svotes.get_voteitem_by_void(VOid)
                print(self.title.format("all_vote_items"))
                print(all_vote_items)
                print(self.title.format("all_vote_items"))
                for item in all_vote_items:
                    vote_choice_item = {}
                    VItext = item.VItext
                    VIno = item.VIno
                    vote_choice_item["VItext"] = VItext
                    vote_choice_item["VIno"] = VIno
                    vote_item["choice_items"].append(vote_choice_item)
            vote_list.append(vote_item)
        response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")
        response["data"] = vote_list
        return response

    def make_vote(self):
        data = json.loads(request.data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))
        if "UStelphone" not in data or "USname" not in data or "USchoose" not in data:
            return PARAMS_MISS
        UStelphone = data["UStelphone"]
        if len(UStelphone) != 11:
            return import_status("ERROR_MESSAGE_WRONG_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_TELPHONE")
        user = self.susers.get_user_by_utel(UStelphone)
        if user:
            return import_status("ERROR_MESSAGE_REPEAT_VOTE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_VOTE")
        USname = data["USname"]
        USchoose = data["USchoose"]
        for row in USchoose:
            add_model("Votenotes",
                      **{
                          "VNid": str(uuid.uuid1()),
                          "VOno": row["VOno"],
                          "VNtext": row["VNtext"],
                          "VNtelphone": UStelphone
                      })

        # 注册+免单优惠券
        USinvate = self.make_invate_code()
        USpassword = self.make_password()
        add_model("Users",
                 **{
                     "USid": str(uuid.uuid1()),
                     "UStelphone": UStelphone,
                     "USpassword": USpassword,
                     "USname": USname,
                     "UScoin": 999.99,
                     "USinvatecode": USinvate
                 })
        # TODO 设计优惠券，利用当前999.99积分后期创建
        response = {}
        response["USpassword"] = USpassword
        response["UScode"] = USinvate
        response_of_add = import_status("SUCCESS_MESSAGE_NEW_VOTE","OK")
        response_of_add["data"] = response
        return response_of_add

    def make_password(self):
        return self.make_random_code(3, 8)

    def make_invate_code(self):
        USinvate = self.susers.get_all_invate_code()
        while True:
            invate_code = self.make_random_code(3, 7)
            if invate_code not in USinvate:
                break
        return invate_code

    def make_random_code(self, m, n):
        import random
        random_code = ""
        while len(random_code) < m:
            a = random.randint(97, 122)
            a = chr(a)
            random_code = random_code + a
        while len(random_code) < n:
            a = random.randint(0, 9)
            random_code = random_code + str(a)
        return random_code
