import React from 'react'
import Header from './Header'
import VideoBox from './VideoBox'
import ToolBar from './ToolBar'
import Transcription from './transcriptionText'

   
export default function App(){
 // this.caption = React.createRef(); //create ref
 
  return ( 
        <>
            <Header/>
            <VideoBox/>
        <ToolBar/>
        <Transcription/>
        </>
    )
         
}
