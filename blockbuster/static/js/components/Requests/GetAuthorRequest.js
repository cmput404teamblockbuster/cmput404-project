var cookie = require('react-cookie');
var axios = require('axios');
const csrfToken = cookie.load('csrftoken');
const userToken ="Token "+localStorage.token;



module.exports = {

    getMe:function (callback) {

        axios.get('/api/author/me/',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               callback(res.data);
            })
    },

    getHim: function (id, callback) {

        //const url = '/api/author/'+uuid+'/';
        const url = id+'/';
        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               callback(res.data);
            })
    },

    getAll: function (callback) {

        const url = '/api/author/all/';
        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken,'Authorization':userToken}})
            .then((res)=>{
                callback(res.data);
            })
    }
};