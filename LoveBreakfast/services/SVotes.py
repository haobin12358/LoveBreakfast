# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy import func
from LoveBreakfast.models.model import Votes as VS, Vote as VO, Votenotes as VN, VoteChoice as VC, VoteResult as VR
from LoveBreakfast.services.SBase import SBase, close_session


class SVotes(SBase):
    def __init__(self):
        super(SVotes, self).__init__()

    # @close_session
    # def get_all_vote(self, vsid):
    #     return self.session.query(VO.VOid, VO.VOtext, VO.VOtype, VO.VOno, VO.VOisnull, VO.VSid).filter(
    #         VO.VSid == vsid).order_by(VO.VOno.asc()).all()

    # @close_session
    # def get_voteitem_by_void(self, void):
    #     return self.session.query(Voteitems.VIid, Voteitems.VItext, Voteitems.VIno)\
    #         .filter_by(VOid=void).order_by(Voteitems.VIno.asc()).all()

    @close_session
    def get_votes(self, vsid):
        return self.session.query(
            VS.VSid, VS.VScontent, VS.VSname, VS.VSstartTime, VS.VSendTime, VS.VSurl, VS.VShead).filter(
            VS.VSid == vsid).first()

    @close_session
    def get_vote(self, vsid, vono=1):
        return self.session.query(
            VO.VOid, VO.VOtext, VO.VOtype, VO.VOno, VO.VOisnull, VO.VSid, VO.VOunit, VO.VObackgroud).filter(
            VO.VSid == vsid, VO.VOno == vono).first()

    @close_session
    def get_all_votes(self):
        return self.session.query(
            VS.VSid, VS.VScontent, VS.VSname, VS.VSstartTime, VS.VSendTime, VS.VSurl, VS.VShead, VS.VSbannel).all()

    @close_session
    def get_votechoisce(self, void):
        return self.session.query(VC.VCid, VC.VCno, VC.VCtext, VC.VCnext, VC.VCtype).filter(VC.VOid == void).all()

    @close_session
    def get_count(self, vsid):
        return self.session.query(func.count(VO.VOid)).filter(VO.VSid == vsid).scalar()

    @close_session
    def get_Votenotes(self, vsid, usid):
        return self.session.query(
            VN.VNid, VN.VSid, VN.USid, VN.VNtime
        ).filter(VN.USid == usid, VN.VSid == vsid).scalar()

if __name__ == "__main__":
    import uuid
    sv = SVotes()
    # sv.add_model("Votes", **{
    #     "VSid": str(uuid.uuid1()),
    #     "VSname": "早安city线上问卷",
    #     "VScontent": "https://daaiti.cn/imgs/LoveBreakfast/vote/bg.png",
    #     "VSstartTime": "",
    #     "VSendTime": "",
    #     "VSurl": "/pages/questionnaire/index",
    #     "VSbannel": "https://daaiti.cn/imgs/LoveBreakfast/{0}/question.png"
    #
    # })
    vsid = 'd1e69bde-9af0-11e8-a394-74d02b0d3622'
    void = "1bb127a1-9af5-11e8-8010-74d02b0d3622"
    # sv.add_model("Vote", **{
    #     "VOid": void,
    #     "VOtext": "早餐真的很重要！在遇到我之前，主人都是怎么吃早餐的呢？",
    #     "VOtype": 1001,
    #     "VOno": 1,
    #     "VOisnull": 1100,
    #     "VOunit": 0,
    #     "VOappend": "",
    #     "VSid": vsid,
    #     "VObackgroud": "https://daaiti.cn/imgs/LoveBreakfast/vote/bg.png"
    # })
    #
    # sv.add_model("VoteChoice", **{
    #     "VCid": str(uuid.uuid1()),
    #     "VCno": "A",
    #     "VCtext": "在家自己做，安全又健康~",
    #     "VCnext": "3",
    #     "VCtype": 1200,
    #     "VOid": void,
    # })
    sv.add_model("VoteChoice", **{
        "VCid": str(uuid.uuid1()),
        "VCno": "B",
        "VCtext": "路上顺路买，节约时间最重要!",
        "VCnext": "2",
        "VCtype": 1200,
        "VOid": void,
    })
    sv.add_model("VoteChoice", **{
        "VCid": str(uuid.uuid1()),
        "VCno": "C",
        "VCtext": "有才华的人从不吃早饭!",
        "VCnext": "8",
        "VCtype": 1200,
        "VOid": void,
    })