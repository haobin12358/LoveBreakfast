# *- coding:utf8 *-
from flask import Flask
import flask_restful
from LoveBreakfast.apis.AUsers import LBUsers as lbuser
from LoveBreakfast.apis.AProduct import LBProduct as lbproduct
from LoveBreakfast.apis.ACarts import LBCarts as lbcarts
from LoveBreakfast.apis.ACategory import LBCategory as lbcategory
# from LoveBreakfast.apis.AShop import AShop as lbshop
from LoveBreakfast.apis.AReview import LBReview as lbreview
from LoveBreakfast.apis.AOrders import LBOrders as lborder
from LoveBreakfast.apis.ALocations import LBLocations as lblocations
from LoveBreakfast.apis.ACoupons import LBCoupons as lbcoupons
from LoveBreakfast.apis.AAddress import LBAddress as lbaddress
from LoveBreakfast.apis.AOther import LBOther as lbother
from LoveBreakfast.apis.AVotes import LBVotes as lbvote

from SharpGoods.apis.AUsers import SGUsers as sguser
from SharpGoods.apis.AProducts import SGProducts as sgproduct
from SharpGoods.apis.ACarts import SGCarts as sgcarts
from SharpGoods.apis.AReviews import SGReviews as sgreview
from SharpGoods.apis.AOrders import SGOrders as sgorder
from SharpGoods.apis.ALocations import SGLocations as sglocations
from SharpGoods.apis.ACoupons import SGCoupons as sgcoupons
from SharpGoods.apis.AOther import SGOther as sgother
from SharpGoods.apis.ACards import SGCards as sgcards

from GroupMeal.apis.AMeals import GMMeals
from GroupMeal.apis.AUsers import GMUsers
from GroupMeal.apis.AMess import GMMess
from GroupMeal.apis.ACarts import GMCarts
from GroupMeal.apis.AOrders import GMOrders
from GroupMeal.apis.AReview import GMReview
from GroupMeal.apis.ACoupons import GMCoupons
from GroupMeal.apis.AOther import GMOther
bk = Flask(__name__)
api = flask_restful.Api(bk)

api.add_resource(lbuser, "/love/breakfast/users/<string:users>")
api.add_resource(lbproduct, "/love/breakfast/product/<string:product>")
api.add_resource(lbcarts, "/love/breakfast/salelist/<string:cart>")
api.add_resource(lbreview, "/love/breakfast/review/<string:review>")
api.add_resource(lbcategory, "/love/breakfast/category/<string:category>")
# api.add_resource(AShop, "/love/breakfast/shop/<string:shop>")
api.add_resource(lborder, "/love/breakfast/orders/<string:orders>")
api.add_resource(lblocations, "/love/breakfast/locations/<string:locations>")
api.add_resource(lbcoupons, "/love/breakfast/cardpkg/<string:card>")
api.add_resource(lbaddress, "/love/breakfast/address/<string:address>")
api.add_resource(lbother, "/love/breakfast/other/<string:other>")
api.add_resource(lbvote, "/love/breakfast/votes/<string:votes>")

api.add_resource(sguser, "/sharp/goods/users/<string:users>")
api.add_resource(sgproduct, "/sharp/goods/product/<string:product>")
api.add_resource(sgcarts, "/sharp/goods/cart/<string:cart>")
api.add_resource(sgreview, "/sharp/goods/review/<string:review>")
api.add_resource(sgorder, "/sharp/goods/orders/<string:orders>")
api.add_resource(sglocations, "/sharp/goods/locations/<string:locations>")
api.add_resource(sgcoupons, "/sharp/goods/card/<string:card>")
api.add_resource(sgother, "/sharp/goods/other/<string:other>")
api.add_resource(sgcards, "/card/<string:card>")

api.add_resource(GMUsers, "/group/meal/user/<string:users>")
api.add_resource(GMMeals, "/group/meal/meal/<string:meals>")
api.add_resource(GMMess, "/group/meal/mess/<string:mess>")
api.add_resource(GMCarts, "/group/meal/cart/<string:cart>")
api.add_resource(GMOrders, "/group/meal/order/<string:orders>")
api.add_resource(GMReview, "/group/meal/order/<string:review>")
api.add_resource(GMCoupons, "/group/meal/coupon/<string:card>")
api.add_resource(GMOther, "/group/meal/other/<string:other>")
if __name__ == '__main__':
    bk.run('0.0.0.0', 443, debug=True, ssl_context=(
        "/etc/nginx/cert/1525609592348.pem"
    ))
'''
if __name__ == '__main__':
    bk.run('0.0.0.0', 7444, debug=True)
'''