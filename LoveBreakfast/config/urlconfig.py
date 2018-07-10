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
    address + "/{0}/banner1.png",
    address + "/{0}/banner2.png",
    address + "/{0}/question.png"
]


weekday_pic = (
    address + "/{0}/image_6.jpg",
    address + "/{0}/image_7.jpg",
    address + "/{0}/image_8.jpg",
    address + "/{0}/image_9.jpg",
    address + "/{0}/image_10.png",
    address + "/{0}/image_1.png",
    address + "/{0}/image_2.png",
)
