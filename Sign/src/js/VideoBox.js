import React from 'react';
import Webcam from 'react-webcam';
import CameraView from './MediaPipe';

export default function VideoBox() {
	return (
		<div>
			<div id='container'>
				<CameraView />
				<button id='btn'>Start</button>
			</div>
		</div>
	);
}
