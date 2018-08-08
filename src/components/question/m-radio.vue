<style  lang="less" rel="stylesheet/less">

</style>
<template>
  <view class="m-one-question">
    <view class="my-num">Q{{question_index + 1}}:</view>
    <p class="my-name">{{question_data.VOtext}}</p>
    <view >
      <view wx:for="{{question_data.choice_items}}" wx:key="item" class="my-btn {{question_data.choose == question_data.choice_items[index].VItext?'active':''}}" @tap="radioTap({{question_index}},index)">{{question_data.choice_items[index].VIno}}、{{question_data.choice_items[index].VItext}}</view>
    </view>
  </view>
</template>

<script>
    import wepy from 'wepy';

    export default class FirstIndex extends wepy.page {
        config = {
            navigationBarTitleText: ''
        }
        data = {}
      props = {
        question_data:{
          type:Object,
          default:null
        },
        question_index:{
          type:Number,
          default:0
        }
      }


        onLoad(options) {

        }

        methods = {}
    }
</script>
