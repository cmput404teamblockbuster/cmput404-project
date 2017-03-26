module.exports = {
    get: function (callback) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        const url = '/api/posts/';

        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                callback(res.data);
                console.log("get public posts:",res.data);
                console.log();
            })
    }
}