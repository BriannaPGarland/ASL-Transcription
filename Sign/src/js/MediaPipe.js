import React, { Component, useRef, useEffect } from 'react';
import { Holistic } from '@mediapipe/holistic';
import * as Cam from '@mediapipe/camera_utils';
import Webcam from 'react-webcam';

export default function CameraView() {
	const webcamRef = useRef(null);
	const canvasRef = useRef(null);
	var camera = null;

	function onResults(results) {
		// const video = webcamRef.current.video;
		const videoWidth = webcamRef.current.video.videoWidth;
		const videoHeight = webcamRef.current.video.videoHeight;

		// Set canvas width
		canvasRef.current.width = videoWidth;
		canvasRef.current.height = videoHeight;

		const canvasElement = canvasRef.current;
		const canvasCtx = canvasElement.getContext('2d');

		canvasCtx.save();
		canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
		// This is to completely redraw the image (only use when you have to actually show off the landmarks alone
		// as just drawing them on a blank canvas and the camera underneath visible shows the small delay calculating
		// the landmarks)
		//canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

		canvasCtx.globalCompositeOperation = 'source-over';
		window.drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#FFFFFF', lineWidth: 1 });
		window.drawLandmarks(canvasCtx, results.poseLandmarks, { color: '#000000', lineWidth: 1 });
		window.drawConnectors(canvasCtx, results.faceLandmarks, FACEMESH_TESSELATION, { color: '#FFFFFF', lineWidth: 1 });
		window.drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS, { color: '#FFFFFF', lineWidth: 1 });
		window.drawLandmarks(canvasCtx, results.leftHandLandmarks, { color: '#000000', lineWidth: 1 });
		window.drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS, { color: '#FFFFFF', lineWidth: 1 });
		window.drawLandmarks(canvasCtx, results.rightHandLandmarks, { color: '#000000', lineWidth: 1,  });
		canvasCtx.restore();
	}

	useEffect(() => {
		const holistic = new Holistic({
			locateFile: (file) => {
				return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
			},
		});
		holistic.setOptions({
			modelComplexity: 1,
			smoothLandmarks: true,
			enableSegmentation: true,
			smoothSegmentation: true,
			refineFaceLandmarks: true,
			minDetectionConfidence: 0.8,
			minTrackingConfidence: 0.5,
		});
		holistic.onResults(onResults);

		if (typeof webcamRef.current !== 'undefined' && webcamRef.current !== null) {
			camera = new Cam.Camera(webcamRef.current.video, {
				onFrame: async () => {
					// This is each frame of the webcam, handle like main loop in python
					await holistic.send({ image: webcamRef.current.video });
				},
			});
			camera.start();
		}
	}, []);

	return (
		<>
			<Webcam
				ref={webcamRef}
				style={{
					position: 'absolute',
					marginLeft: 'auto',
					marginRight: 'auto',
					left: 0,
					right: 0,
					textAlign: 'center',
					zindex: 9,
					width: 'fit-content',
					height: 'fit-content',
				}}
			/>
			<canvas
				ref={canvasRef}
				className='output_canvas'
				style={{
					position: 'absolute',
					marginLeft: 'auto',
					marginRight: 'auto',
					left: 0,
					right: 0,
					textAlign: 'center',
					zindex: 9,
					width: 'fit-content',
					height: 'fit-content',
				}}
			></canvas>
		</>
	);
}
