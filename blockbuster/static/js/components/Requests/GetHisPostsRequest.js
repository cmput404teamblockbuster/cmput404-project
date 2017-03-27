
module.exports = {
    get: function (me, uuid, callback) {
        this.sendGetRequest(me, uuid, callback);
    },

    sendGetRequest: function (me, id,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const url = '/api/author/'+id+'/posts/';

        axios.post(url,{requesting_user_uuid:me},
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                cb(res.data);
                console.log(res.data);
            })
    },

};