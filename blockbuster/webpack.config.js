/*** 
*    the following configuration is mostly lifted from 
*    http://geezhawk.github.io/using-react-with-django-rest-framework
*    by Jonathan Cox 
***/

var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    
    //our app's entry point
    //to make multiple bundles:
     entry: {
         myStream: './static/js/components/Pages/MyStreamPage/index.js',
         myFriends: './static/js/components/Pages/MyFriendsPage/index.js',
         profile: './static/js/components/Pages/ProfilePage/index.js',
         login: './static/js/components/Pages/LoginPage/index.js',
         singlePost: './static/js/components/Pages/SinglePostPage/index.js'
     },

    // entry: './static/js/index.js',
    
    output:{
        //where you want your compiled bundle to be stored
        path: path.resolve('./static/bundles'),
        //naming convention webpack should use for your files
        /*publicPath: 'http://localhost:8000/'*/

        filename: "[name].js",
    },
    watch: true,

    plugins: [
         //tells webpack where to store data about your bundle
         new BundleTracker({filename: './webpack.stats.json'})
    ],
    
    module: {
        loaders: [
        /* a regexp that tells webpack use the following loaders on all 
        .js and .jsx files */
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                //probably won't need query here?
                query: {
                    //specify that we will be dealing with React code
                    presets: ['react']
                }
            },
            /* we can add another loader here to render the static image file */
            // from :https://medium.com/@rajaraodv/webpack-the-confusing-parts-58712f8fcad9#.4mcf8uagv
            /*{
                test: /\.png?$/,
                loader: "url-loader?limit=1"
            },*/

        ]
    },
    
    resolve: {
        //tells webpack where to look for modules
        modules: ['node_modules'],
        //extensions that should be used to resolve modules
        extensions: [ '.js', '.jsx'] 
    }
}