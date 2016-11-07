/**
 * Created by yinxing on 16/8/14.
 */

new Vue({
    el: '#app',
    data: {
        listData: [],
        logInfo: {
            name: '',
            pwd: ''
        },
        logged: false,
        newSentence: {
            en: '',
            cn: ''
        }
    },
    created: function () {
        this.checkLoginState();
        $('#login input[type="text"]').focus();
    },
    methods: {
        checkLoginState: function () {
            console.log('check login state.');
        },
        showEn: function (item) {
            console.log('showEn');
            item.show_en = !item.show_en;
        },
        getList: function(){
            var vm = this;
            Vue.http.get('http://127.0.0.1:5000/'+ this.logInfo.name +'/items')
                .then(function(resp){
                    var respData = resp.data.sentences.map(function (item) {
                        item.show_en = false;
                        return item;
                    });
                    vm.listData = respData;

                }, function(resp){
                    console.log(resp);
                });
        },
        logIn: function () {
            var vm = this;
            Vue.http.get('http://127.0.0.1:5000/login', {
                params: {
                    username: vm.logInfo.name,
                    password: vm.logInfo.pwd
                }
            }).then(function (resp) {
                console.log(resp);
                if(!resp.data.code) {
                    alert('用户名或密码错误')
                } else {
                    vm.logged = true;
                    vm.getList();
                }
            }, function (resp) {
                console.log(resp);
            })
        },
        addNew: function () {
            console.log(this.newSentence);
            var vm = this;
            var create_time = '2016-11-06 11:11:11';
            Vue.http.post('http://127.0.0.1:5000/'+ this.logInfo.name +'/items', {
                    chinese: vm.newSentence.cn,
                    english: vm.newSentence.en,
                    create_time: create_time
            }).then(function (resp) {
                console.log(resp);
            }, function (resp) {
                console.log(resp);
            })
        }
    }
});
