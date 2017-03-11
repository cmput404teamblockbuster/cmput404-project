import React from 'react'
import {Tabs, Tab} from 'material-ui/Tabs';
import TextField from 'material-ui/TextField'
import Upload from 'material-ui/svg-icons/file/file-upload'
import FlatButton from 'material-ui/FlatButton'

export default class MakePostContent extends React.Component{
    constructor(props){
        super(props);
        this.text = ''

        this.handle=this.handle.bind(this);
    }

    handle(event){
        this.text = event.target.value;
        console.log(this.text)
    }
    render(){
        const styles = {
          uploadButton: {
            verticalAlign: 'middle',
          },
          uploadInput: {
            cursor: 'pointer',
            position: 'absolute',
            top: 0,
            bottom: 0,
            right: 0,
            left: 0,
            width: '100%',
            opacity: 0,
          },
        };
        return(
            <Tabs>
                <Tab label="Text Post">
                    <TextField hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handle} hintText="Content"/>
                </Tab>
                <Tab label="Image Post">
                    <FlatButton icon={<Upload/>} labelPosition='after' label="Upload Image" containerElement="label" className="fullWidth">
                        <input type="file" className="uploadInput"/>
                    </FlatButton>

                </Tab>
            </Tabs>
        );
    }
}