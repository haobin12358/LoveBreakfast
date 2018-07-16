# *- coding:utf8 *-
header = "https://"
ip = "h878.cn/"
nginx_dir = "imgs/LoveBreakfast"

address = header + ip + nginx_dir

product_url_list = [
    address + "/image_1.png",
    address + "/image_2.png",
    address + "/image_3.png",
]


home = [

    address + "/{0}/question.png"
]

"""
address + "/{0}/banner1.png",
address + "/{0}/banner2.png",
"""

weekday_pic = (
    address + "/{0}/timg.gif",
    address + "/{0}/timg.gif",
    address + "/{0}/timg.gif",
    address + "/{0}/timg.gif",
    address + "/{0}/timg.gif",
    address + "/{0}/timg.gif",
    address + "/{0}/timg.gif"
)

"""
   address + "/{0}/image_1.jpg",
   address + "/{0}/image_2.jpg",
   address + "/{0}/image_3.jpg",
   address + "/{0}/image_4.jpg",
   address + "/{0}/image_5.png",
   address + "/{0}/image_6.png",
   address + "/{0}/image_7.png",
   """