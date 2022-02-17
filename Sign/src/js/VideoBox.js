import React from 'react'

//import logo from '../../whiteLogo.png'

/*
 <script>
                var video = document.querySelector("#videoElement");

                if (navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function (stream) {
                    video.srcObject = stream;
                    })
                    .catch(function (err0r) {
                    console.log("Something went wrong!");
                    })
                };
            </script>
*/


export default function VideoBox(){
    return(
        <div >
            <div id="container">
	            <video autoplay="true" id="videoElement">

	            </video>
                <button id="btn">Start</button>
            </div>
           
            
        </div>
        
      
    )
}