import React from 'react'
//import logo from '../../whiteLogo.png'
import Speech from 'react-speech';

export default function ToolBar(){
    return(
        <div id ='tools'>
        {/*<label class="switch"> 
                <input type="checkbox"/>
                <span class="slider round"></span>
    </label>*/}
        <label id='left'>Enable:</label>
        {/*<Button onClick={()=>this.props.myFunction(param)}>button text</Button>
        <Speech text={parentToChild} />*/}
        <Speech text='transcribed text will appear here...' />
        <label id='left'>Sign to Voice</label>
            <label class="switch">
                <input type="checkbox"/>
                <span class="slider round"></span>
        </label>
            <label id='left'> Dark Mode</label>
            <div id='right'>
                <button class='copyBtn'>Copy Transcript</button>
            </div>
            <label id='right'> Transcript Recording</label>
            <label id='right' class="switch"> 
                <input type="checkbox"/>
                <span class="slider round"></span>
            </label>
      </div>
      
  )
}
