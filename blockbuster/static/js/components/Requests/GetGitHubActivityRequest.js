module.exports = {
    get: function (github, page, callback) {
        const username = this.extractGitHubUserName(github);
        if (username){
            let axios = require('axios');
            const number = page? page:0;
            const path = 'https://api.github.com/users/'+username+'/events/public?page='+number;
            const header = localStorage.etag ? {"If-None-Match": localStorage.etag} : {};
            axios.get(path,{headers:header})
                .then((response)=>{
                    localStorage.etag= response.headers.etag;
                    localStorage.github =JSON.stringify(response.data);
                    callback(response.data)

                })
                .catch((err)=>{
                    if (err.response.status===304){
                        callback(JSON.parse(localStorage.github))
                    } else {
                        console.log("github request: failed with", err);
                        callback("Try Again Later")
                    }
                })
        } else {
            callback(false)
        }

    },

    extractGitHubUserName(url){
        if (url !== ""){
            const array = url.split('/');
            const index = array[array.length-1] === ""? array.length-2:array.length-1;
            return array[index]
        }
        return false
    }
};