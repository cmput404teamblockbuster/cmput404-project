
module.exports = {
    send: function (content, uuid, Callback) {
        this.getAuthor(content,uuid, this.sendPostRequest, Callback);
    },

    sendPostRequest: function (p1,uuid, p3,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const url = '/api/posts/'+uuid+'/comments/';
        axios.post(url,
            {"author":p3,body:p1},
            {headers:{
            'X-CSRFToken':csrfToken,
            'Content-Type':'application/json',
            'Authorization':userToken}})
            .then((res)=>{
                cb();
                console.log(res);
            })
    },

    getMe:function (p1, uuid, cb, cb2) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.get('/api/author/me/',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               cb(p1, uuid, res.data, cb2);
            })
    }
};