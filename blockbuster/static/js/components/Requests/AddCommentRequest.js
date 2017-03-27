
module.exports = {
    send: function (host, content, uuid, Callback) {
        this.getMe(host, content,uuid, this.sendPostRequest, Callback);
    },

    sendPostRequest: function (h, p1,uuid, p3,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const url = '/api/posts/'+uuid+'/comments/';
        axios.post(url,
            {"author":p3,comment:p1, host:h},
            {headers:{
            'X-CSRFToken':csrfToken,
            'Content-Type':'application/json',
            'Authorization':userToken}})
            .then((res)=>{
                cb();
                console.log(res);
            })
    },

    getMe:function (host, p1, uuid, cb, cb2) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.get('/api/author/me/',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               cb(host, p1, uuid, res.data, cb2);
            })
    }
};