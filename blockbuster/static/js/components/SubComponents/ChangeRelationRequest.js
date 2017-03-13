
module.exports = {
    send: function (receiver, status) {
        this.getAuthor(receiver,status, this.sendPostRequest);
    },

    update: function (initiator, receiver, status, cb) {
        this.sendPostRequest(initiator, receiver, status, cb);
    },

    sendPostRequest: function (p1,p2, p3, cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.post('/api/friendrequest/',
            {"initiator":p1,"receiver":p2,"status":p3},
            {headers:{'X-CSRFToken':csrfToken,'Content-Type':'application/json'}})
            .then((res)=>{
                if(cb != null){
                    cb();
                }
                console.log(res);
            })
    },

    getAuthor:function (p1,p2,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.get('/api/author/me',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
                console.log("result of get author");
                console.log(res);
               cb(res.data, p1, p2, cb);
               console.log(res);
            })
    }
};