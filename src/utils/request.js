import wepy from 'wepy';
import tip from './tip';
const request = async(params = {}, url) => {
  tip.loading();
  let data = params.query || {};
  let res =  wepy.request({
    url: url,
    method: params.method || 'GET',
    data: data,
    header: { 'Content-Type': 'application/json' },
  });
  tip.loaded();
  return res;
};


module.exports = {
  request
}
