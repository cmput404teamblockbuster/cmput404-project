module.exports = {
    put:function (github, bio, id, callback) {
        var cookie = require('react-cookie');
        var axios = require('axios');
        const csrfToken = cookie.load('csrftoken');
        const userToken ="Token "+localStorage.token;

        axios.put(`/api/author/${id}/`,
            {github:github,bio:bio},
            {headers:{'X-CSRFToken':csrfToken, 'Authorization':userToken}})
            .then((res)=>{
                console.log("put profile request:", res.data);
               callback(res.data);
            })
    }

};