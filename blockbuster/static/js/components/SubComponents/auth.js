
/*
from http://geezhawk.github.io/user-authentication-with-react-and-django-rest-framework
*/

module.exports = {
    login: function(username, pass, cb) {
        if (localStorage.token) {
            if (cb) cb(true);
            return
        }
        this.getToken(username, pass, (res) => {
            if (res.authenticated) {
                localStorage.token = res.token;
                if (cb) cb(true)
            } else {
                if (cb) cb(false)
            }
        })
    },        
    
    logout: function() {
        delete localStorage.token
    },

    loggedIn: function() {
        return !!localStorage.token
    },

    getToken: function(username, pass, cb) {
        var cookie = require('react-cookie');
        const csrftoken = cookie.load('csrftoken');
        var axios = require('axios');
        axios.post('/obtain-auth-token/',{
                username: username,
                password: pass
            }, {headers:{'X-CSRFToken':csrftoken}})
            .then((res) => {
                cb({
                    authenticated: true,
                    token: res.data.token
                })
            })
    //     $.ajax({
    //         type: 'POST',
    //         url: '/api/obtain-auth-token/',
    //         data: {
    //             username: username,
    //             password: pass
    //         },
    //         success: function(res){
    //             cb({
    //                 authenticated: true,
    //                 token: res.token
    //             })
    //         }
    //     })
    },
}