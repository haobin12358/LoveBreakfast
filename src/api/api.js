import {wxRequest} from '../utils/wxRequest';
//接口前缀
const _title = '';
//定义接口
const getDiscoverList = (params) => wxRequest(params, apiMall + '/goods/list?cateidOne=1&cateidTwo=0&price=0&sales=2');

module.exports = {
  getDiscoverList
}
