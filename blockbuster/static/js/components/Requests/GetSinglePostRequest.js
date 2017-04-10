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
            auth: {username: 'god', password: 'god'}})
            .then((res)=>{
                cb(res.data);
                console.log("get single post", res.data);
            })
    },

    delete: function (id, callback) {
        const path = "api/posts/"+id+"/";

        axios.delete(path, {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((response)=>{
                callback(response.data)
            })
    },

    edit: function (id, visibility, callback, visibleTo) {
        const path = "api/posts/"+id+"/";
        const data = visibleTo? {visibility:visibility,visibleTo:[visibleTo.id]} : {visibility:visibility};
        axios.put(path, data,
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((response)=>{
                callback(response.data)
            })
    }





};