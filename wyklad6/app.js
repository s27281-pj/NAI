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

// Mobile-friendly settings
const DETECT_EVERY_MS = 250;        // stabilniej na telefonach niż 150ms
const MAX_CONSECUTIVE_FAILS = 3;    // ile razy z rzędu może "nie wykryć", zanim zablokuje
let consecutiveFails = 0;

const detectorOptions = new faceapi.TinyFaceDetectorOptions({
  inputSize: 320,          // 224/320/416; 320 to dobry kompromis
  scoreThreshold: 0.3      // niżej = mniej "NO FACE" na gorszej kamerze
});

// progi (tune pod mobile)
const FACE_TOO_CLOSE_RATIO = 0.70; // >70% szerokości = za blisko (było 0.8, za ostre)
const EAR_CLOSED_THRESHOLD = 0.19; // 0.21 bywa zbyt czułe na mobile

// 1) Start po kliknięciu Accept
acceptBtn.addEventListener('click', async () => {
  disclaimer.style.display = 'none';
  mainContent.style.display = 'block';

  // AudioContext musi być zainicjowany w wyniku interakcji użytkownika
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();

  await initAI();
});

async function initAI() {
  statusDiv.innerText = "Loading AI models...";
  try {
    // Ładowanie modeli (ścieżki względne)
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
        await webcam.play(); // ważne na mobile
      } catch (e) {
        // jeśli play zablokowany, user i tak kliknął accept, zwykle przejdzie
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
 * Zamiast setInterval (który może nakładać kolejne detekcje),
 * robimy pętlę setTimeout -> stabilniej na mobile.
 */
async function loopDetect() {
  if (!trackingActive) return;

  // jeśli jeszcze brak wymiarów video, poczekaj
  if (!webcam.videoWidth || !webcam.videoHeight) {
    setTimeout(loopDetect, DETECT_EVERY_MS);
    return;
  }

  // jeśli user zatrzymał webcam (rzadkie), nie rób nic
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
        // informacyjnie, bez karania od razu
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

    // debug (możesz zakomentować)
    statusDiv.innerText = `BIOMETRIC MONITORING: ACTIVE | EAR=${avgEAR.toFixed(2)} | ratio=${faceSizeRatio.toFixed(2)}`;

    if (avgEAR < EAR_CLOSED_THRESHOLD) {
      triggerAction("EYES CLOSED! ATTENTION IS MANDATORY.");
    } else {
      resumeAd();
    }
  } catch (err) {
    // Gdy telefon dławi się na chwilę, nie rób dramatu – spróbuj dalej
    console.error("Detection error:", err);
    statusDiv.innerText = "Tracking hiccup... retrying.";
  }

  setTimeout(loopDetect, DETECT_EVERY_MS);
}

/**
 * EAR (Eye Aspect Ratio) - Oblicza stopień otwarcia oka
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
  // pauzuj reklamę
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

    // odpalanie wideo na mobile czasem wymaga "gesture" – ale user już kliknął accept
    videoAd.play().catch(() => {
      // jeśli przeglądarka blokuje autoplay, przynajmniej nie syp w konsoli
    });
  }
}
