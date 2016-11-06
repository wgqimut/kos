/**
 * Created by yinxing on 16/8/14.
 */

var kos = {};
Vue.http.get('http://127.0.0.1:5000/wangguoqing/items')
        .then(function(resp){

            kos.listData = resp.data.map(function (item) {
                item.show_en = false;
                return item;
            });

            new Vue({
                el: '#list',
                data: {
                    listData: kos.listData
                },
                methods: {
                    showEn: function (item) {
                        item.show_en = !item.show_en;
                    }
                }
            });

    }, function(resp){
        console.log(resp);
    });


