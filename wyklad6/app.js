/* global faceapi */

const acceptBtn = document.getElementById('accept-btn');
const disclaimer = document.getElementById('disclaimer-modal');
const mainContent = document.getElementById('main-content');
const videoAd = document.getElementById('videoAd');
const webcam = document.getElementById('webcam');
const evilAlert = document.getElementById('evil-alert');
const alertMsg = document.getElementById('alert-message');
const statusDiv = document.getElementById('status');

// Audio (pisk)
let audioCtx;
let oscillator;

// Tracking control
let trackingActive = false;

// =============================
// Mobile-friendly, MORE SENSITIVE settings
// =============================
const DETECT_EVERY_MS = 200;        // szybciej niż 250ms
const MAX_CONSECUTIVE_FAILS = 2;    // mniej taryfy ulgowej niż 3
let consecutiveFails = 0;

const detectorOptions = new faceapi.TinyFaceDetectorOptions({
  inputSize: 320,          // 224/320/416; 320 = dobry kompromis
  scoreThreshold: 0.35     // było 0.3 -> odrobinę pewniejsza detekcja
});

// Progi (bardziej czułe / bardziej “agresywne”)
const FACE_TOO_CLOSE_RATIO = 0.65; // było 0.70 -> szybciej uzna "za blisko"
const EAR_CLOSED_THRESHOLD = 0.205;// było 0.19 -> łatwiej uzna "oczy zamknięte"

// 1) Start po kliknięciu Accept
acceptBtn.addEventListener('click', async () => {
  disclaimer.style.display = 'none';
  mainContent.style.display = 'block';

  // AudioContext musi być zainicjowany po interakcji użytkownika
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();

  await initAI();
});

async function initAI() {
  statusDiv.innerText = "Loading AI models...";
  try {
    // Ścieżki do modeli (względnie, stabilnie na Pages)
    await faceapi.nets.tinyFaceDetector.loadFromUri('./models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('./models');

    statusDiv.innerText = "Accessing camera...";

    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "user",
        width: { ideal: 640 },
        height: { ideal: 480 }
      },
      audio: false
    });

    webcam.srcObject = stream;

    webcam.onloadedmetadata = async () => {
      try {
        await webcam.play();
      } catch (e) {
        console.log("webcam play blocked:", e);
      }

      statusDiv.innerText = "BIOMETRIC MONITORING: ACTIVE";
      startTracking();
    };
  } catch (err) {
    statusDiv.innerText = "Fatal Error: Camera access denied or models missing.";
    console.error(err);
  }
}

function startTracking() {
  trackingActive = true;
  consecutiveFails = 0;
  loopDetect();
}

/**
 * setTimeout loop (stabilniej na mobile niż setInterval)
 */
async function loopDetect() {
  if (!trackingActive) return;

  // jeśli jeszcze brak wymiarów video, poczekaj
  if (!webcam.videoWidth || !webcam.videoHeight) {
    setTimeout(loopDetect, DETECT_EVERY_MS);
    return;
  }

  // jeśli webcam zatrzymany, nie rób nic
  if (webcam.paused || webcam.ended) {
    setTimeout(loopDetect, DETECT_EVERY_MS);
    return;
  }

  try {
    const detections = await faceapi
      .detectSingleFace(webcam, detectorOptions)
      .withFaceLandmarks();

    if (!detections) {
      consecutiveFails++;

      if (consecutiveFails >= MAX_CONSECUTIVE_FAILS) {
        triggerAction("USER NOT DETECTED! PLEASE LOOK AT THE SCREEN.");
      } else {
        // lżejszy status zamiast alarmu przy pojedynczym hiccup
        statusDiv.innerText = `Scanning... (${consecutiveFails}/${MAX_CONSECUTIVE_FAILS})`;
      }

      setTimeout(loopDetect, DETECT_EVERY_MS);
      return;
    }

    // mamy twarz -> reset fail counter
    consecutiveFails = 0;

    const box = detections.detection.box;
    const faceSizeRatio = box.width / webcam.videoWidth;

    if (faceSizeRatio > FACE_TOO_CLOSE_RATIO) {
      triggerAction("TOO CLOSE! STEP BACK FOR BIOMETRIC VERIFICATION.");
      setTimeout(loopDetect, DETECT_EVERY_MS);
      return;
    }

    const landmarks = detections.landmarks;
    const leftEye = landmarks.getLeftEye();
    const rightEye = landmarks.getRightEye();

    const leftEAR = getEAR(leftEye);
    const rightEAR = getEAR(rightEye);
    const avgEAR = (leftEAR + rightEAR) / 2;

    // Debug status (możesz wywalić jak już działa)
    statusDiv.innerText = `BIOMETRIC MONITORING: ACTIVE | EAR=${avgEAR.toFixed(3)} | ratio=${faceSizeRatio.toFixed(2)}`;

    if (avgEAR < EAR_CLOSED_THRESHOLD) {
      triggerAction("EYES CLOSED! ATTENTION IS MANDATORY.");
    } else {
      resumeAd();
    }
  } catch (err) {
    console.error("Detection error:", err);
    statusDiv.innerText = "Tracking hiccup... retrying.";
  }

  setTimeout(loopDetect, DETECT_EVERY_MS);
}

/**
 * EAR (Eye Aspect Ratio) - stopień otwarcia oka
 */
function getEAR(eye) {
  const v1 = Math.hypot(eye[1].x - eye[5].x, eye[1].y - eye[5].y);
  const v2 = Math.hypot(eye[2].x - eye[4].x, eye[2].y - eye[4].y);
  const h  = Math.hypot(eye[0].x - eye[3].x, eye[0].y - eye[3].y);
  return (v1 + v2) / (2.0 * h);
}

// Oscylator (pisk)
function startSqueak() {
  if (!audioCtx) return;
  if (oscillator) return;

  oscillator = audioCtx.createOscillator();
  oscillator.type = 'sawtooth';
  oscillator.frequency.setValueAtTime(3000, audioCtx.currentTime);

  const gainNode = audioCtx.createGain();
  gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime);

  oscillator.connect(gainNode);
  gainNode.connect(audioCtx.destination);
  oscillator.start();
}

function stopSqueak() {
  if (oscillator) {
    oscillator.stop();
    oscillator = null;
  }
}

function triggerAction(message) {
  if (!videoAd.paused) {
    videoAd.pause();
  }

  alertMsg.innerText = message;
  evilAlert.style.display = 'flex';

  startSqueak();
}

function resumeAd() {
  if (evilAlert.style.display === 'flex') {
    evilAlert.style.display = 'none';
    stopSqueak();

    videoAd.play().catch(() => {
      // autoplay może być blokowany – olać, UX i tak “złe”
    });
  }
}
