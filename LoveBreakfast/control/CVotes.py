# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from LoveBreakfast.config.response import SYSTEM_ERROR, PARAMS_MISS
from LoveBreakfast.common.import_status import import_status
# from LoveBreakfast.common.TransformToList import add_model
from LoveBreakfast.common.timeformate import get_db_time_str, get_web_time_str, format_forweb_no_HMS
from LoveBreakfast.common.get_model_return_list import get_model_return_dict as todict, get_model_return_list as tolist


class CVotes():
    conversion_VOunit = {1300: "站"}
    conversion_VOtype = {1001: "单选题", 1002: '多选题', 1003: '填空题'}
    conversion_VOunit_reverse = {k: v for v, k in conversion_VOunit.items()}
    conversion_VOtype_reverse = {k: v for v, k in conversion_VOtype.items()}

    def __init__(self):
        from LoveBreakfast.services.SVotes import SVotes
        self.svotes = SVotes()
        from LoveBreakfast.services.SUsers import SUsers
        self.susers = SUsers()
        self.title = '============{0}============'

    # def get_all(self):
    #     args = request.args.to_dict()
    #     if "VSid" not in args:
    #         return PARAMS_MISS
    #     all_vote = self.svotes.get_all_vote()
    #     print(self.title.format("all_vote"))
    #     print(all_vote)
    #     print(self.title.format("all_vote"))
    #     if not all_vote:
    #         return SYSTEM_ERROR
    #     vote_list = []
    #     for row in all_vote:
    #         vote_item = {}
    #         VOid = row.VOid
    #         VOno = row.VOno
    #         VOtext = row.VOtext
    #         VOchoice = row.VOchoice
    #         VOisnull = row.VOisnull
    #         if VOchoice == 1001:
    #             choice = "[单选题]"
    #         elif VOchoice == 1002:
    #             choice = "[多选题]"
    #         elif VOchoice == 1003:
    #             choice = "[填空题]"
    #         else:
    #             choice = None
    #         vote_item["VOid"] = VOid
    #         vote_item["VOno"] = VOno
    #         vote_item["VOtext"] = VOtext
    #         vote_item["VOisnull"] = VOisnull
    #         vote_item["VOchoice"] = choice
    #         if VOchoice == 1001 or VOchoice == 1002:
    #             vote_item["choice_items"] = []
    #             all_vote_items = self.svotes.get_voteitem_by_void(VOid)
    #             print(self.title.format("all_vote_items"))
    #             print(all_vote_items)
    #             print(self.title.format("all_vote_items"))
    #             for item in all_vote_items:
    #                 vote_choice_item = {}
    #                 VItext = item.VItext
    #                 VIno = item.VIno
    #                 vote_choice_item["VItext"] = VItext
    #                 vote_choice_item["VIno"] = VIno
    #                 vote_item["choice_items"].append(vote_choice_item)
    #         vote_list.append(vote_item)
    #     response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")
    #     response["data"] = vote_list
    #     return response

    def get_vote(self):
        args = request.args.to_dict()
        print(self.title.format('args'))
        print(args)
        print(self.title.format('args'))

        if "VSid" not in args:
            return PARAMS_MISS

        vono = args.get("VOno") if args.get("VOno") else 1
        vsid = args.get("VSid")
        try:
            votes = self.svotes.get_votes(vsid)
            print(self.title.format('votes'))
            print(votes)
            print(self.title.format('votes'))
            count = self.svotes.get_count(vsid)
            print(self.title.format('count'))
            print(count)
            print(self.title.format('count'))
            time_now = get_db_time_str()
            # 答题时间判断
            if votes.VSstartTime and votes.VSstartTime > time_now:
                return import_status("error_vote_time", "LOVEBREAKFAST_ERROR", "error_vote_time_start")
            if votes.VSendTime and votes.VSendTime < time_now:
                return import_status("error_vote_time", "LOVEBREAKFAST_ERROR", "error_vote_time_end")

            vote = todict(self.svotes.get_vote(vsid, vono))
            print(self.title.format("vote"))
            print(vote)
            print(self.title.format("vote"))
            # 获取下一题no
            if int(vote.get("VOno")) < count:
                if vote.get("VOtype") < 1003:
                    votechoice_list = tolist(self.svotes.get_votechoisce(vote.get("VOid")))
                    if vote.get("VOtype") < 1002:
                        for votechoice in votechoice_list:
                            if not votechoice.get("VCnext"):
                                votechoice["VCnext"] = int(vote.get("VOno")) + 1
                    else:
                        vote["VCnext"] = int(vote.get("VOno")) + 1
                    vote["votechoice"] = votechoice_list
                else:
                    vote["VCnext"] = int(vote.get("VOno")) + 1
            else:
                vote["VCnext"] = ""
            vote["VOunit"] = self.conversion_VOunit.get(vote.get("VOunit"))
            vote["VOtype"] = self.conversion_VOtype.get(vote.get('VOtype', 1001))
            response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")

            vote["progress"] = int(float(vote.get("VOno")) / float(count) * 100)
            response["data"] = vote
            return response
        except Exception as e:
            print(self.title.format("get vote"))
            print(e.message)
            print(self.title.format("get vote"))
            return SYSTEM_ERROR

    def get_host(self):
        args = request.args.to_dict()
        print(self.title.format('args'))
        print(args)
        print(self.title.format('args'))

        if "VSid" not in args:
            return PARAMS_MISS
        vsid = args.get("VSid")
        votes = todict(self.svotes.get_votes(vsid))
        print(self.title.format('votes'))
        print(votes)
        print(self.title.format('votes'))

        # votes.pop("VSstartTime")
        # votes.pop("VSendTime")
        time_now = get_db_time_str()
        time_status = "时间没问题"
        time_status_code = 200
        if votes.get("VSstartTime") and time_now < votes.get("VSstartTime"):
            time_status_code = 405601
            time_status = "答题时间未到"
        if votes.get("VSendTime") and time_now > votes.get("VSendTime"):
            time_status_code = 405602
            time_status = "答题时间已超"

        votes["VSstartTime"] = get_web_time_str(votes.get("VSstartTime"), format_forweb_no_HMS)

        votes["VSendTime"] = get_web_time_str(votes.get("VSendTime"), format_forweb_no_HMS)
        votes["VStime"] = "2018-08-10"
        votes["TimeStatus"] = time_status
        votes["TimeStatusCode"] = time_status_code
        response = import_status("SUCCESS_MESSAGE_GET_VOTE", "OK")
        response["data"] = votes
        return response

    # def make_vote(self):
    #     data = json.loads(request.data)
    #     print(self.title.format("data"))
    #     print(data)
    #     print(self.title.format("data"))
    #     if "UStelphone" not in data or "USname" not in data or "USchoose" not in data:
    #         return PARAMS_MISS
    #     UStelphone = data["UStelphone"]
    #     if len(UStelphone) != 11:
    #         return import_status("ERROR_MESSAGE_WRONG_TELPHONE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_WRONG_TELPHONE")
    #     user = self.susers.get_user_by_utel(UStelphone)
    #     if user:
    #         return import_status("ERROR_MESSAGE_REPEAT_VOTE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_VOTE")
    #     USname = data["USname"]
    #     USchoose = data["USchoose"]
    #     for row in USchoose:
    #         add_model("Votenotes",
    #                   **{
    #                       "VNid": str(uuid.uuid1()),
    #                       "VOno": row["VOno"],
    #                       "VNtext": row["VNtext"],
    #                       "VNtelphone": UStelphone
    #                   })
    #
    #     # 注册+免单优惠券
    #     USinvate = self.make_invate_code()
    #     USpassword = self.make_password()
    #     add_model("Users",
    #              **{
    #                  "USid": str(uuid.uuid1()),
    #                  "UStelphone": UStelphone,
    #                  "USpassword": USpassword,
    #                  "USname": USname,
    #                  "UScoin": 999.99,
    #                  "USinvatecode": USinvate
    #              })
    #     # TODO 设计优惠券，利用当前999.99积分后期创建
    #     response = {}
    #     response["USpassword"] = USpassword
    #     response["UScode"] = USinvate
    #     response_of_add = import_status("SUCCESS_MESSAGE_NEW_VOTE","OK")
    #     response_of_add["data"] = response
    #     return response_of_add

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

    def make_vote(self):
        data = json.loads(request.data)
        print(self.title.format('data'))
        print(data)
        print(self.title.format('data'))
        usertel = data.get("UStelphone")
        username = data.get("USname")

        user = self.susers.get_uid_by_utel(usertel)

        print(self.title.format('data'))
        print(data)
        print(self.title.format('data'))

        if not user:
            # 注册+免单优惠券
            USinvate = self.make_invate_code()
            print(self.title.format('USinvate'))
            print(USinvate)
            print(self.title.format('USinvate'))

            USpassword = self.make_password()

            print(self.title.format('USpassword'))
            print(USpassword)
            print(self.title.format('USpassword'))

            user = str(uuid.uuid1())
            self.susers.add_model("Users", **{
                "USid": user,
                "UStelphone": usertel,
                "USpassword": USpassword,
                "USname": username,
                "UScoin": 999.99,
                "USinvatecode": USinvate
            })
        vn = self.svotes.get_Votenotes(data.get("VSid"), user)
        if vn:
            return import_status("ERROR_MESSAGE_REPEAT_VOTE", "LOVEBREAKFAST_ERROR", "ERROR_CODE_REPEAT_VOTE")
        vntime = get_db_time_str()
        vnid = str(uuid.uuid1())
        self.svotes.add_model("Votenotes", **{
            "VNid": vnid,
            "VSid": data.get("VSid"),
            "USid": user,
            "VNtime": vntime
        })
        VoteResult = data.get("USchoose")
        for vr in VoteResult:
            if not isinstance(vr.get("VRchoice"), basestring):
                vr["VRchoice"] = json.dumps(vr.get("VRchoice"))

            self.svotes.add_model("VoteResult", **{
                "VRid": str(uuid.uuid1()),
                "VNid": vnid,
                "VOid": vr.get("VOid"),
                "VRchoice": vr.get("VRchoice"),
                "VRabo": vr.get("VRabo")
            })

        self.susers.add_model("Cardpackage", **{
            "CAid": str(uuid.uuid1()),
            "USid": user,
            "CAstatus": 2,
            "CAstart": get_db_time_str(),
            "CAend": "20181231235959",
            "COid": "123",
        })
        response = import_status("SUCCESS_MESSAGE_NEW_VOTE", "OK")
        response["data"] = {
            "UStelphone": usertel,
            "USpassword": self.susers.get_upwd_by_utel(usertel),
        }
        return response
