import React from 'react'
import ReactDom from 'react-dom'

var Hello = React.createClass({
    render: function(){
        return (
            <h1>
            Hello World!
            </h1>
        );
    }
})

ReactDom.render(<Hello />,
document.getElementById('container'));