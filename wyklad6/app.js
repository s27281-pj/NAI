/* global faceapi */

const acceptBtn = document.getElementById('accept-btn');
const disclaimer = document.getElementById('disclaimer-modal');
const mainContent = document.getElementById('main-content');
const videoAd = document.getElementById('videoAd');
const webcam = document.getElementById('webcam');
const evilAlert = document.getElementById('evil-alert');
const alertMsg = document.getElementById('alert-message');
const statusDiv = document.getElementById('status');

// Zmienne do obsługi dźwięku (pisku)
let audioCtx;
let oscillator;

// 1. Start po kliknięciu przycisku w Disclaimerze
acceptBtn.addEventListener('click', () => {
    disclaimer.style.display = 'none';
    mainContent.style.display = 'block';

    // Inicjalizacja dźwięku przy pierwszym kliknięciu (wymóg przeglądarek)
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    initAI();
});

async function initAI() {
    statusDiv.innerText = "Loading AI models...";
    try {
        // Ładowanie modeli z folderu relatywnego 'models'
        await faceapi.nets.tinyFaceDetector.loadFromUri('models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('models');

        statusDiv.innerText = "Accessing camera...";
        const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
        webcam.srcObject = stream;

        webcam.onloadedmetadata = () => {
            statusDiv.innerText = "BIOMETRIC MONITORING: ACTIVE";
            startTracking();
        };
    } catch (err) {
        statusDiv.innerText = "Fatal Error: Camera access denied or models missing.";
        console.error(err);
    }
}

function startTracking() {
    setInterval(async () => {
        if (webcam.paused || webcam.ended) return;

        // OPTYMALIZACJA: Zwiększono inputSize do 512 dla lepszej detekcji z bliska
        const detections = await faceapi.detectSingleFace(
            webcam,
            new faceapi.TinyFaceDetectorOptions({ inputSize: 512, scoreThreshold: 0.5 })
        ).withFaceLandmarks();

        if (!detections) {
            triggerAction("USER NOT DETECTED! PLEASE LOOK AT THE SCREEN.");
        } else {
            // NOWA FUNKCJONALNOŚĆ: Sprawdzanie dystansu (rozmiar twarzy w kadrze)
            const box = detections.detection.box;
            const faceSizeRatio = box.width / webcam.videoWidth;

            if (faceSizeRatio > 0.8) {
                // Jeśli twarz zajmuje ponad 80% szerokości obrazu, użytkownik jest za blisko
                triggerAction("TOO CLOSE! SYSTEM CANNOT VERIFY BIOMETRICS. STEP BACK.");
            } else {
                const landmarks = detections.landmarks;
                const leftEye = landmarks.getLeftEye();
                const rightEye = landmarks.getRightEye();

                const leftEAR = getEAR(leftEye);
                const rightEAR = getEAR(rightEye);
                const avgEAR = (leftEAR + rightEAR) / 2;

                if (avgEAR < 0.21) {
                    triggerAction("EYES CLOSED! ATTENTION IS MANDATORY.");
                } else {
                    resumeAd();
                }
            }
        }
    }, 150);
}

// Funkcja generująca pisk (Oscylator)
function startSqueak() {
    if (oscillator) return; // Jeśli już piszczy, nie twórz nowego

    oscillator = audioCtx.createOscillator();
    oscillator.type = 'sawtooth'; // Bardzo nieprzyjemny dźwięk "piły"
    oscillator.frequency.setValueAtTime(3000, audioCtx.currentTime); // Wysoki ton (3000Hz)

    const gainNode = audioCtx.createGain();
    gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime); // Głośność (bezpieczne 5%)

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

/**
 * EAR (Eye Aspect Ratio) - Oblicza stopień otwarcia oka
 */

function getEAR(eye) {
    const v1 = Math.sqrt(Math.pow(eye[1].x - eye[5].x, 2) + Math.pow(eye[1].y - eye[5].y, 2));
    const v2 = Math.sqrt(Math.pow(eye[2].x - eye[4].x, 2) + Math.pow(eye[2].y - eye[4].y, 2));
    const h = Math.sqrt(Math.pow(eye[0].x - eye[3].x, 2) + Math.pow(eye[0].y - eye[3].y, 2));
    return (v1 + v2) / (2.0 * h);
}

function triggerAction(message) {
    if (!videoAd.paused) {
        videoAd.pause();
    }
    alertMsg.innerText = message;
    evilAlert.style.display = 'flex';

    // Włącz pisk przy alarmie
    startSqueak();
}

function resumeAd() {
    if (evilAlert.style.display === 'flex') {
        evilAlert.style.display = 'none';

        // Wyłącz pisk przy wznowieniu
        stopSqueak();

        videoAd.play().catch(e => console.log("Play blocked by browser policy"));
    }
}