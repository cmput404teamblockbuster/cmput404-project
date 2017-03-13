
module.exports = {
    send: function (receiver, status) {
        this.getAuthor(receiver,status, this.sendPostRequest);
    },

    sendPostRequest: function (p1,p2, p3, cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        console.log("About to attempt the post");
        console.log(p1);
        console.log(p2);
        console.log(p3);
        console.log("author: " + p1["username"]);

        var dict = {};
        dict["uuid"] = p2.id;
        dict["username"] = p2.receiver;

        var stat = {};
        stat["status"] = p3;

        axios.post('/api/friendrequest/',
            {"initiator":p1,"receiver":dict,"status":p3},
            {headers:{'X-CSRFToken':csrfToken,'Content-Type':'application/json'}})
            .then((res)=>{
                cb();
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
               cb(res.data, p1, p2);
               console.log(res);
            })
    }
};