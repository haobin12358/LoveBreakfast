# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from LoveBreakfast.models.model import Votes, Voteitems, Votenotes
from LoveBreakfast.services.SBase import SBase, close_session

class SVotes(SBase):

    def __init__(self):
        super(SVotes, self).__init__()

    @close_session
    def get_all_vote(self):
        return self.session.query(Votes.VOid, Votes.VOtext, Votes.VOchoice, Votes.VOisnull, Votes.VOno)\
            .order_by(Votes.VOno.asc()).all()

    @close_session
    def get_voteitem_by_void(self, void):
        return self.session.query(Voteitems.VIid, Voteitems.VItext, Voteitems.VIno)\
            .filter_by(VOid=void).order_by(Voteitems.VIno.asc()).all()