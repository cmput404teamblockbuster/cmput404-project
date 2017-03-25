
module.exports = {
    get: function (uuid, callback) {
        this.sendGetRequest(uuid, callback);
    },

    sendGetRequest: function (id,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const url = '/api/author/'+id+'/posts/';

        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                cb(res.data);
                console.log(res.data);
            })
    },

};