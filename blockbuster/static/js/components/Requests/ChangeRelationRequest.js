var cookie = require('react-cookie');
var axios = require('axios');
const csrfToken = cookie.load('csrftoken');
const userToken ="Token "+localStorage.token;

module.exports = {
    send: function (friend, status, callback) {
        //duct tape solution to change 'username' to 'displayName' !!!!!!!!! Fix me !!!!!!!!!!!!!1
        if(friend['displayName'] == null){
            friend['displayName'] = friend['username'];
        }
        this.getAuthor(friend,status, this.sendPostRequest,callback);
    },

    update: function (author, friend, status, cb) {
        this.sendPostRequest(author, friend, status, cb);
    },

    sendPostRequest: function (p1,p2, p3, cb) {
        axios.post('/api/friendrequest/',
            {"author":p1,"friend":p2,"status":p3, query:"friendrequest"},
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
                    if (res.data==="success"){
                        callback("No Relationship Found.")
                    } else {
                        callback(res.data);
                    }
                }
            })
    },
};