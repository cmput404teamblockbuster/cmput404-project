
module.exports = {
    send: function (content, privacy, refreshCallback) {
        this.getMe(content,privacy, this.sendPostRequest, refreshCallback);
    },

    sendPostRequest: function (p1,p2, p3,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.post('/api/posts/',
            {"author":p3,content:p1,privacy:p2},
            {headers:{
            'X-CSRFToken':csrfToken,
            'Content-Type':'application/json',
            'Authorization':userToken}})
            .then((res)=>{
                cb(res.data);
                console.log(res);
            })
    },

    getMe:function (p1, p2, cb, cb2) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.get('/api/author/me/',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               cb(p1, p2, res.data, cb2);
            })
    }
};
