// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Login form handling
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // In a real app, you would validate credentials here
            window.location.href = 'dashboard.html';
        });
    }

    // Dashboard tab switching
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Show corresponding content
                const tabId = this.getAttribute('data-tab') + '-tab';
                document.getElementById(tabId).classList.add('active');
            });
        });
    }

    // File upload handling
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadedImage = document.getElementById('uploadedImage');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const analyzeUploadBtn = document.getElementById('analyzeUploadBtn');

    if (uploadArea) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });

        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = '#2e7d32';
        });

        uploadArea.addEventListener('dragleave', function() {
            this.style.borderColor = '#ddd';
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = '#ddd';
            
            if (e.dataTransfer.files.length) {
                handleFile(e.dataTransfer.files[0]);
            }
        });

        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                handleFile(this.files[0]);
            }
        });

        function handleFile(file) {
            if (!file.type.match('image.*')) {
                alert('Please select an image file');
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = 'block';
                uploadPlaceholder.style.display = 'none';
                analyzeUploadBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    }

    // Camera handling
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const capturedImage = document.getElementById('capturedImage');
    const cameraPlaceholder = document.getElementById('cameraPlaceholder');
    const startCameraBtn = document.getElementById('startCameraBtn');
    const capturePictureBtn = document.getElementById('capturePictureBtn');
    const analyzeCaptureBtn = document.getElementById('analyzeCaptureBtn');

    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', async function() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                video.style.display = 'block';
                cameraPlaceholder.style.display = 'none';
                startCameraBtn.style.display = 'none';
                capturePictureBtn.style.display = 'inline-block';
            } catch (err) {
                console.error('Error accessing camera:', err);
                alert('Could not access the camera. Please make sure you have granted permission.');
            }
        });

        capturePictureBtn.addEventListener('click', function() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            capturedImage.src = canvas.toDataURL('image/png');
            capturedImage.style.display = 'block';
            video.style.display = 'none';
            
            // Stop the camera stream
            const stream = video.srcObject;
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            
            capturePictureBtn.style.display = 'none';
            startCameraBtn.style.display = 'inline-block';
            startCameraBtn.textContent = 'Retake Photo';
            analyzeCaptureBtn.disabled = false;
        });
    }

    // Analysis handling
    const analyzeButtons = [analyzeUploadBtn, analyzeCaptureBtn].filter(Boolean);
    const resultContainer = document.getElementById('resultContainer');
    const resultText = document.getElementById('resultText');

    analyzeButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', function() {
                // In a real app, you would send the image to a backend for processing
                // For now, we'll just simulate a response
                resultContainer.style.display = 'block';
                resultText.textContent = 'Healthy plant detected. No diseases found.';
                
                // Scroll to results
                resultContainer.scrollIntoView({ behavior: 'smooth' });
            });
        }
    });
});