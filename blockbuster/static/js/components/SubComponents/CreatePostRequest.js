
module.exports = {
    send: function (content, privacy) {
        this.getAuthor(content,privacy, this.sendPostRequest);
    },

    sendPostRequest: function (p1,p2, p3) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');

        var qs = require('qs');
        var urlencode = require('urlencode')
        const data = {"author":p3,content:p1,privacy:p2};
        console.log(data)
        axios.post('/api/posts/',
            data,
            {headers:{'X-CSRFToken':csrfToken,'Content-Type':'application/json'}})
            .then((res)=>{
                console.log(res);
            })
    },

    getAuthor:function (p1,p2,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');

        axios.get('/api/author/',{headers:{'X-CSRFToken':csrfToken}})
            .then((res)=>{
               cb(p1, p2, res.data[0]);
            })
    }
};