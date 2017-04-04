
module.exports = {
    send: function (content, title, des, mode, privacy, refreshCallback, targetAuthor) {
        this.getMe(content,title, des, mode, privacy, this.sendPostRequest, refreshCallback, targetAuthor);
    },

    sendPostRequest: function (p1, t, des,mode, p2, p3,cb, targetAuthor) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const data = p2!=="private_to" ?
            {author:p3, title:t, description:des, content:p1,contentType:mode,visibility:p2}
            :
            {author:p3, title:t, description:des,content:p1,contentType:mode,visibility:p2,visibleTo:[targetAuthor.id] }
        console.log("make post request: ", data);
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

    getMe:function (p1,title, des,mode, p2, cb, cb2, targetAuthor) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.get('/api/author/me/',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               cb(p1,title, des,mode, p2, res.data, cb2,targetAuthor);
            })
    }
};
