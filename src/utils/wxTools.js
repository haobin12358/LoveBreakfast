/**
 * offetHeight  滚动计算部分到顶部距离
 * scrollTop   滚动高度
 * height      每个模块的高度
 * colunm      列数
 **/

function countIndex (offetHight, scrollTop, height, colunm) {
  // 单例获取屏幕宽度比
  if (!countIndex.pix) {
    try {
      let res = wx.getSystemInfoSync()
      countIndex.pix = res.windowWidth / 375
    } catch (e) {
      countIndex.pix = 1
    }
  }
  let scroll = scrollTop - offetHight * countIndex.pix
  let hei = height * countIndex.pix
  return scroll > 0 ? Math.floor(scroll / hei) * colunm : 0
}
