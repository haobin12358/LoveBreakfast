import {request} from '../utils/request';
//接口前缀
const _title = 'http://120.79.182.43:7444';
//定义接口
//首页
const get_product_all =  _title + '/love/breakfast/product/get_all';
//商品详情
const get_product_info =  _title + '/love/breakfast/product/get_info_by_id';
//订单
const make_main_order =  _title + '/love/breakfast/orders/make_main_order';//创建订单
const get_order_user =  _title + '/love/breakfast/orders/get_order_user';//获取下单人信息
const update_order_status =  _title + '/love/breakfast/orders/update_order_status';//更新订单状态
const get_order_list = _title + '/love/breakfast/orders/get_order_list';//获取所有订单
const get_order_abo =  _title + '/love/breakfast/orders/get_order_abo';//获取订单性情

//购物车
const get_all_car = _title + '/love/breakfast/salelist/get_all';//获取购物车信息
const update_car = _title + '/love/breakfast/salelist/update';//更新购物车信息
const delete_car =  _title + '/love/breakfast/salelist/delete_product';//删除购物车信息

//下单
const get_line = _title + '/love/breakfast/locations/get_lline';//获取站点信息
const get_all_location = _title + '/love/breakfast/locations/get_all_location';//获取站点信息
const get_lno = _title + '/love/breakfast/locations/get_lno';//获取出口信息

//登录
const login =  _title + '/love/breakfast/users/login';
//注册
const register =  _title + '/love/breakfast/users/register';
//个人中心
const get_person_info = _title + '/love/breakfast/users/all_info';//获取用户信息
const change_person_info = _title + '/love/breakfast/users/update_info';//修改用户信息
const change_person_Pwd =  _title + '/love/breakfast/users/update_pwd';//修改用户信息

//评价
// const change_person_Pwd = _title + '/love/breakfast/users/update_pwd';//修改用户信息
const create_review = _title +'/love/breakfast/review/create_review';//添加评价
const get_review = _title +'/love/breakfast/review/get_review';//添加评价

const get_cardpkg = _title + '/love/breakfast/cardpkg/get_cardpkg';//获取优惠券

module.exports = {
  get_product_all,
  get_product_info,
  make_main_order,
  get_order_user,
  update_order_status,
  get_order_list,
  get_order_abo,
  get_all_car,
  update_car,
  delete_car,
  get_all_location,
  get_lno,
  get_line,
  login,
  register,
  get_person_info,
  change_person_info,
  change_person_Pwd,
  create_review,
  get_cardpkg,
  get_review
}
