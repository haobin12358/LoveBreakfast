# *- coding:utf8 *-
from flask import Flask
import flask_restful
from LoveBreakfast.apis.AUsers import AUsers
from LoveBreakfast.apis.AProduct import AProduct
from LoveBreakfast.apis.ACarts import ACarts
from LoveBreakfast.apis.ACategory import ACategory
# from LoveBreakfast.apis.AShop import AShop
from LoveBreakfast.apis.AReview import AReview
from LoveBreakfast.apis.AOrders import AOrders
from LoveBreakfast.apis.ALocations import ALocations
from LoveBreakfast.apis.ACoupons import ACoupons
from LoveBreakfast.apis.AAddress import AAddress
from LoveBreakfast.apis.AOther import AOther
from LoveBreakfast.apis.AVotes import AVotes

bk = Flask(__name__)
api = flask_restful.Api(bk)

api.add_resource(AUsers, "/love/breakfast/users/<string:users>")
api.add_resource(AProduct, "/love/breakfast/product/<string:product>")
api.add_resource(ACarts, "/love/breakfast/salelist/<string:cart>")
api.add_resource(AReview, "/love/breakfast/review/<string:review>")
api.add_resource(ACategory, "/love/breakfast/category/<string:category>")
# api.add_resource(AShop, "/love/breakfast/shop/<string:shop>")
api.add_resource(AOrders, "/love/breakfast/orders/<string:orders>")
api.add_resource(ALocations, "/love/breakfast/locations/<string:locations>")
api.add_resource(ACoupons, "/love/breakfast/cardpkg/<string:card>")
api.add_resource(AAddress, "/love/breakfast/address/<string:address>")
api.add_resource(AOther, "/love/breakfast/other/<string:other>")
api.add_resource(AVotes, "/love/breakfast/votes/<string:votes>")

'''
if __name__ == '__main__':
    bk.run('0.0.0.0', 443, debug=True, ssl_context=(
        "/etc/nginx/cert/1525609592348.pem"
    ))
'''
if __name__ == '__main__':
    bk.run('0.0.0.0', 7444, debug=True)
