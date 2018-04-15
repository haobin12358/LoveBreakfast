# *- coding:utf8 *-
from flask import Flask
import flask_restful
from apis.AUsers import AUsers
from apis.AProduct import AProduct
from apis.ACarts import ACarts
from apis.ACategory import ACategory
from apis.AShop import AShop
from apis.AReview import AReview
from apis.AOrders import AOrders
from apis.ALocations import ALocations
from apis.ACoupons import ACoupons

bk = Flask(__name__)
api = flask_restful.Api(bk)

api.add_resource(AUsers, "/love/breakfast/users/<string:users>")
api.add_resource(AProduct, "/love/breakfast/product/<string:product>")
api.add_resource(ACarts, "/love/breakfast/salelist/<string:cart>")
api.add_resource(AReview, "/love/breakfast/review/<string:review>")
api.add_resource(ACategory, "/love/breakfast/category/<string:category>")
api.add_resource(AShop, "/love/breakfast/shop/<string:shop>")
api.add_resource(AOrders, "/love/breakfast/orders/<string:orders>")
api.add_resource(ALocations, "/love/breakfast/locations/<string:locations>")
api.add_resource(ACoupons, "/love/breakfast/cardpkg/<string:card>")


if __name__ == '__main__':
    bk.run('0.0.0.0', 7444, debug=True)
