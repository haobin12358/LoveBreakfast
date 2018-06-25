# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
from config.status import response_ok
from config.response import PARAMS_MISS, SYSTEM_ERROR


class Clocations():
    def __init__(self):
        pass

    def get_city_location(self):
        args = request.args.to_dict()
        print "================args================"
        print args
        print "================args================"
        if "lon" not in args or "lat" not in args:
            return PARAMS_MISS

        url = "http://api.map.baidu.com/geocoder/v2/?callback={0}&location={1},{2}&output={3}&pois={4}&ak={5}"\
            .format("renderReverse", args["lat"], args["lon"], "xml", 0, "1bdd475a06ffdb9a4f3ee021da7ae847")

        strResult = None
        try:
            import urllib2
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            strResult = response.read()
            response.close()
        except Exception as e:
            print e.message
        print("=======================strResult===================")
        print(strResult)
        print("=======================strResult===================")
        import xmltodict
        json_strResult = xmltodict.parse(strResult)
        if not json_strResult:
            return PARAMS_MISS
        import json
        json_strResult = json.loads(json.dumps(json_strResult))
        print("=======================json_strResult===================")
        print(json_strResult)
        print("=======================json_strResult===================")

        status = json_strResult["GeocoderSearchResponse"]["status"]
        if status != '0':
            return SYSTEM_ERROR
            # 百度请求挂了
        city = json_strResult["GeocoderSearchResponse"]["result"]["addressComponent"]["city"]

        response = {}
        response["status"] = response_ok
        response["message"] = "获取当前城市成功"
        response["data"] = {}
        response["data"]["city"] = city

        return response
