
module.exports = {
    get: function (uuid, callback) {
        this.sendGetRequest(uuid, callback);
    },

    sendGetRequest: function (id,cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        var uuid = id.split('/');
        uuid = uuid[uuid.length-1];

        //const url = '/api/author/'+uuid+'/friends/';

        const url = id + '/friends/';
        console.log("attempting to get friends with url: " + url);

        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                console.log("result of GetTheirFreindsRequest:");
                console.log(res.data);
                cb(res.data);
            })
    },

};