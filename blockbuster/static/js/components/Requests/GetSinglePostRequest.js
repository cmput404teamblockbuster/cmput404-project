var cookie = require('react-cookie');
var axios = require('axios');
const csrfToken = cookie.load('csrftoken');
const userToken ="Token "+localStorage.token;

module.exports = {
    get: function (uuid, callback) {
        this.sendGetRequest(uuid, callback);
    },

    sendGetRequest: function (id, cb) {
        const url = '/api/posts/'+id+'/';

        axios.get(url,
            {headers:{'X-CSRFToken':csrfToken},
            auth: {username: 'team2', password: 'team2'}})
            .then((res)=>{
                cb(res.data);
                console.log("get single post", res.data);
            })
    },

};