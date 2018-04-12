# *- coding:utf8 *-
from flask import Flask
import flask_restful
from apis.AUsers import AUsers
from apis.AProduct import AProduct
from apis.ACarts import ACarts
from apis.ACategory import ACategory
from apis.AShop import AShop
from apis.AReview import AReview

app = Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(AUsers, "/love/breakfast/users/<string:users>")
api.add_resource(AProduct, "/love/breakfast/product/<string:product>")
api.add_resource(ACarts, "/love/breakfast/salelist/<string:cart>")
api.add_resource(AReview, "/love/breakfast/review/<string:review>")
api.add_resource(ACategory, "/love/breakfast/category/<string:category>")
api.add_resource(AShop, "/love/breakfast/shop/<string:shop>")

if __name__ == '__main__':
    app.run('0.0.0.0', 7443, debug=True)

@app.error_handlers(Exception)
def catchException(error):
    from flask import jsonify
    response = dict(status=0, message="500 Error")
    return jsonify(response), 400
