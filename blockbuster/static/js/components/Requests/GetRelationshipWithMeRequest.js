
module.exports = {
    get: function (uuid, callback) {
        this.sendGetRequest(uuid, callback);
    },

    sendGetRequest: function (id, cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const url = '/api/author/me/relationship/'+id+'/';

        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                cb(res.data);
                console.log("getRelationship");
                console.log(res.data);
            })
    },

};