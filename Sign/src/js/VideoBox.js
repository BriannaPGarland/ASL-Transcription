import React from 'react';
import Webcam from 'react-webcam';

export default function VideoBox() {
	return (
		<div>
			<div id='container'>
				<Webcam id='videoElement'/>
				<button id='btn'>Start</button>
			</div>
		</div>
	);
}
