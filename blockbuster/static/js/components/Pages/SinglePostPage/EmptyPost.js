import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';


export default class EmptyPost extends React.Component{

    render(){
        return(
            <li>
                <Card className="textField">
                    <CardText >
                        <p style={{fontSize:'3em', testAlign:"center"}} >
                            404 POST NOT FOUND
                        </p>
                    </CardText>
                </Card>
            </li>
        );
    }
}