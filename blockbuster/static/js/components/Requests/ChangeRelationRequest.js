var cookie = require('react-cookie');
var axios = require('axios');
const csrfToken = cookie.load('csrftoken');
const userToken ="Token "+localStorage.token;

module.exports = {
    send: function (receiver, status, callback) {
        this.getAuthor(receiver,status, this.sendPostRequest,callback);
    },

    update: function (initiator, receiver, status, cb) {
        this.sendPostRequest(initiator, receiver, status, cb);
    },

    sendPostRequest: function (p1,p2, p3, cb) {
        axios.post('/api/friendrequest/',
            {"initiator":p1,"receiver":p2,"status":p3},
            {headers:{'X-CSRFToken':csrfToken,'Content-Type':'application/json','Authorization':userToken}})
            .then((res)=>{
                if(cb != null){
                    cb(res.data);
                }

            })
    },

    getAuthor:function (p1, p2, cb, cb2) {
        axios.get('/api/author/me',
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
               cb(res.data, p1, p2, cb2);
            })
    },

    deleteRelation: function(relationshipObject, callback){
        if (!relationshipObject.id){
            alert("change relationship request")
        }
        const path = '/api/friendrequest/'+relationshipObject.id+'/';

        axios.delete(path, {
            headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}
        })
            .then((res)=>{
                if (callback){
                    callback(res.data);
                }
            })
    },
};