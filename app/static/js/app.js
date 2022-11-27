//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var recorder; 						//WebAudioRecorder object
var input; 							//MediaStreamAudioSourceNode  we'll be recording
var encodingType; 					//holds selected encoding for resulting audio (file)
var encodeAfterRecord = true;       // when to encode

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record
var recordButton = document.getElementById("recordButton");
var recordingsList = document.getElementById("recordingsList");
var upldForm = document.getElementById("upldData");
var upldBtn = document.getElementById("upld");
var rcrdBt = document.getElementById('recordButton');
var sndBar = document.getElementById('sound');
var inp = document.getElementById('inp');

function viewRcrd() {
    inp.style.display = "none";
	rcrdBt.style.display = "block";
    sndBar.style.display = "block";
    upldBtn.style.display = "block";
    upldBtn.disabled = true;
};

function viewUpld() {
    rcrdBt.style.display = "none";
    sndBar.style.display = "none";
    inp.style.display = "block";
    upldBtn.style.display = "block";
    upldBtn.disabled = false;
};

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);

function startRecording() {

	/*
		Simple constraints object, for more advanced features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    upldBtn.disabled = true;
    var constraints = { audio: true, video:false }
    /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();


		//assign to gumStream for later use
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);
		
		//stop the input from playing back through the speakers
		//input.connect(audioContext.destination)

		//get the encoding 
		encodingType = "wav";

		recorder = new WebAudioRecorder(input, {
		  workerDir: "static/js/", // must end with slash
		  encoding: encodingType,
		  numChannels:2, //2 is the default, mp3 encoding supports only 2
		  onEncoderLoading: function(recorder, encoding) {
		    // show "loading encoder..." display
		  },
		  onEncoderLoaded: function(recorder, encoding) {
		    // hide "loading encoder..." display
		  }
		});

		recorder.onComplete = function(recorder, blob) { 
			createDownloadLink(blob);
			recordButton.disabled = false;
		}

		recorder.setOptions({
		  timeLimit:3,
		  encodeAfterRecord:encodeAfterRecord,
	      ogg: {quality: 0.5},
	      mp3: {bitRate: 160}
	    });

		//start the recording process
		recorder.startRecording();

	}).catch(function(err) {
	  	//enable the record button if getUSerMedia() fails
    	recordButton.disabled = false;

	});

	//disable the record button
    recordButton.disabled = true;
}

function stopRecording() {
	
	gumStream.getAudioTracks()[0].stop();
	recordButton.disabled = false;
	
	recorder.finishRecording();
}

function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var au = document.getElementById('sound');

	au.controls = true;
	au.src = url;

	const dT = new DataTransfer();
	dT.items.add(new File([blob], 'audio.wav', {type: "audio/wav"}));

	upldBtn.disabled = false;

	inp.files = dT.files;
	recordingsList.appendChild(au);
}


