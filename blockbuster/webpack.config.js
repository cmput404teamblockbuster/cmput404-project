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
    entry: './static/js/index.js',
    
    output:{
        //where you want your compiled bundle to be stored
        path: path.resolve('./static/bundles'),
        //naming convention webpack should use for your files
        filename: "[name]-[hash].js"
    },
    
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
        ]
    },
    
    resolve: {
        //tells webpack where to look for modules
        modules: ['node_modules'],
        //extensions that should be used to resolve modules
        extensions: [ '.js', '.jsx'] 
    }
}