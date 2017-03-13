
module.exports = {
    get: function (callback) {
        this.sendGetRequest( callback);
    },

    sendGetRequest: function (cb) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        // const url = '/api/author/posts/';
        const url = '/api/posts/'; //TODO: change it back to author/posts/
        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                cb(res.data);
                console.log(res.data);
            })
    },

};