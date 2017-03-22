import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';


export default class EmptyPost extends React.Component{

    render(){
        return(
            <li style={{textAlign:"center"}}>
                <Card className="textField">
                    <CardText >
                        <p style={{fontSize:'3em', }} >
                            404 POST NOT FOUND
                        </p>
                    </CardText>
                </Card>
            </li>
        );
    }
}