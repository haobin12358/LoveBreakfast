import {
  wxRequest
} from '@/utils/wxRequest';

let env = "-test" //-dev 或者 -test
const api= '';

/**
 * 获取发现好商品接口
 * @param  {[type]} params [description]
 * @return {[type]}        [description]
 */
const getDiscoverList = (params) => wxRequest(params, api + '/goods/list?cateidOne=1&cateidTwo=0&price=0&sales=2');

export default {
  getDiscoverList,

}
