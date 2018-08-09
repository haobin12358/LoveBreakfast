# *- coding:utf8 *-
from flask import Flask
import flask_restful
from LoveBreakfast.apis.AUsers import LBUsers
from LoveBreakfast.apis.AProduct import LBProduct
from LoveBreakfast.apis.ACarts import LBCarts
from LoveBreakfast.apis.ACategory import LBCategory
# from LoveBreakfast.apis.AShop import AShop
from LoveBreakfast.apis.AReview import LBReview
from LoveBreakfast.apis.AOrders import LBOrders
from LoveBreakfast.apis.ALocations import LBLocations
from LoveBreakfast.apis.ACoupons import LBCoupons
from LoveBreakfast.apis.AAddress import LBAddress
from LoveBreakfast.apis.AOther import LBOther
from LoveBreakfast.apis.AVotes import LBVotes


bk = Flask(__name__)
api = flask_restful.Api(bk)

api.add_resource(LBUsers, "/love/breakfast/users/<string:users>")
api.add_resource(LBProduct, "/love/breakfast/product/<string:product>")
api.add_resource(LBCarts, "/love/breakfast/salelist/<string:cart>")
api.add_resource(LBReview, "/love/breakfast/review/<string:review>")
api.add_resource(LBCategory, "/love/breakfast/category/<string:category>")
# api.add_resource(AShop, "/love/breakfast/shop/<string:shop>")
api.add_resource(LBOrders, "/love/breakfast/orders/<string:orders>")
api.add_resource(LBLocations, "/love/breakfast/locations/<string:locations>")
api.add_resource(LBCoupons, "/love/breakfast/cardpkg/<string:card>")
api.add_resource(LBAddress, "/love/breakfast/address/<string:address>")
api.add_resource(LBOther, "/love/breakfast/other/<string:other>")
api.add_resource(LBVotes, "/love/breakfast/votes/<string:votes>")

'''
if __name__ == '__main__':
    bk.run('0.0.0.0', 443, debug=True, ssl_context=(
        "/etc/nginx/cert/1525609592348.pem"
    ))
'''
if __name__ == '__main__':
    bk.run('0.0.0.0', 7444, debug=True)
