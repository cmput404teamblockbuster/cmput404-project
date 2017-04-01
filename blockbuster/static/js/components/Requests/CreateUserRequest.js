
module.exports = {
    send: function (username, password, email, callback, errCallback) {
        this.sendPostRequest(username,password,email, callback, errCallback);
    },

    sendPostRequest: function (p1,p2, p3, cb, errCallback) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');

        axios.post('/api/register/',
            {username:p1,password:p2,email:p3},
            {headers:{'X-CSRFToken':csrfToken,'Content-Type':'application/json'}})
            .then((res)=>{
                cb();
                console.log(res);
            })
            .catch(
                (err)=>{
                    errCallback();
                }
            )
    },

};