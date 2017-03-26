var cookie = require('react-cookie');
var axios = require('axios');
const csrfToken = cookie.load('csrftoken');
const userToken ="Token "+localStorage.token;

module.exports = {
    getFollowers: function (cb) {
        const path = '/api/author/me/followers/'

        axios.get(path, {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
              cb(res.data)
            })
    },

    getFollowings: function (cb) {
        const path = '/api/author/me/following/'
        axios.get(path, {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
              cb(res.data)
            })
    },

    getFriends: function (cb) {
        const path = '/api/author/'
        axios.get(path, {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
              cb(res.data)
            })
    }

};