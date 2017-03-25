
module.exports = {
    send: function (content, privacy, refreshCallback, targetAuthor) {
        this.getMe(content,privacy, this.sendPostRequest, refreshCallback, targetAuthor);
    },

    sendPostRequest: function (p1,p2, p3,cb, targetAuthor) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const data = p2==="private_to_one_friend" ?{author:p3,content:p1,visibility:p2} : {author:p3,content:p1,visibility:p2,private_to:targetAuthor }

        axios.post('/api/posts/',
            data,
            {headers:{
            'X-CSRFToken':csrfToken,
            'Content-Type':'application/json',
            'Authorization':userToken}})
            .then((res)=>{
                cb(res.data);
                console.log(res);
            })
    },

    getMe:function (p1, p2, cb, cb2, targetAuthor) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.get('/api/author/me/',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               cb(p1, p2, res.data, cb2,targetAuthor);
            })
    }
};
