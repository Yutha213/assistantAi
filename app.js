// LiveKit Connection and Session Management
class ExpertAI {
    constructor() {
        this.room = null;
        this.isConnected = false;
        this.isMuted = false;
        this.isCameraOff = false;

        // Detect LiveKit namespace
        if (typeof LiveKit === 'undefined' && typeof LivekitClient !== 'undefined') {
            window.LiveKit = LivekitClient;
        }

        this.initializeElements();
        this.attachEventListeners();

        // Check if LiveKit SDK loaded
        if (typeof LiveKit === 'undefined') {
            console.error('LiveKit SDK not loaded!');
        } else {
            console.log('LiveKit SDK loaded successfully');
        }
    }

    initializeElements() {
        // Panels
        this.connectionPanel = document.getElementById('connection-panel');
        this.sessionPanel = document.getElementById('session-panel');

        // Form elements
        this.connectForm = document.getElementById('connect-form');
        this.roomNameInput = document.getElementById('room-name');
        this.tokenInput = document.getElementById('participant-token');

        // Chat elements
        this.chatContainer = document.getElementById('chat-container');
        this.chatMessages = document.getElementById('chat-messages');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');

        // Session elements
        this.statusText = document.getElementById('status-text');
        this.aiStatus = document.getElementById('ai-status');
        this.videoGrid = document.getElementById('video-grid');
        this.audioContainer = document.getElementById('audio-container');

        // Buttons
        this.disconnectBtn = document.getElementById('disconnect-btn');
        this.muteBtn = document.getElementById('mute-btn');
        this.cameraBtn = document.getElementById('camera-btn');
    }

    attachEventListeners() {
        this.connectForm.addEventListener('submit', (e) => this.handleConnect(e));
        this.disconnectBtn.addEventListener('click', () => this.handleDisconnect());
        this.muteBtn.addEventListener('click', () => this.toggleMute());
        this.cameraBtn.addEventListener('click', () => this.toggleCamera());
        this.chatForm.addEventListener('submit', (e) => this.handleChatMessage(e));
    }

    async handleConnect(event) {
        event.preventDefault();

        // Check/sync LiveKit namespace again before connection
        if (typeof LiveKit === 'undefined' && typeof LivekitClient !== 'undefined') {
            window.LiveKit = LivekitClient;
        }

        // Check if LiveKit SDK is loaded
        if (typeof LiveKit === 'undefined') {
            this.showError('LiveKit SDK failed to load. Please check your internet connection and refresh the page.');
            console.error('LiveKit SDK not available');
            return;
        }

        const roomName = this.roomNameInput.value.trim();
        const token = this.tokenInput.value.trim();

        if (!roomName || !token) {
            this.showError('Please fill in all fields');
            return;
        }

        try {
            // Show loading state
            const submitBtn = this.connectForm.querySelector('.btn');
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            submitBtn.textContent = 'CONNECTING...';

            // Get LiveKit URL from environment or use default
            const livekitUrl = 'wss://ehs-assistant-iudkaul6.livekit.cloud';

            // Create room instance
            this.room = new LiveKit.Room({
                adaptiveStream: true,
                dynacast: true,
            });

            // Set up event listeners
            this.setupRoomListeners();

            // Connect to room
            await this.room.connect(livekitUrl, token);

            this.isConnected = true;
            this.showSessionPanel();

            console.log('Connected to room:', roomName);
        } catch (error) {
            console.error('Connection error:', error);
            this.showError(`Failed to connect: ${error.message}`);

            // Reset button state
            const submitBtn = this.connectForm.querySelector('.btn');
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            submitBtn.textContent = 'INITIALIZE_CONNECTION';
        }
    }

    setupRoomListeners() {
        // Participant connected
        this.room.on(LiveKit.RoomEvent.ParticipantConnected, (participant) => {
            console.log('Participant connected:', participant.identity);
            this.aiStatus.textContent = 'Connected and ready';
        });

        // Participant disconnected
        this.room.on(LiveKit.RoomEvent.ParticipantDisconnected, (participant) => {
            console.log('Participant disconnected:', participant.identity);
        });

        // Track subscribed (audio/video from AI)
        this.room.on(LiveKit.RoomEvent.TrackSubscribed, (track, publication, participant) => {
            console.log('Track subscribed:', track.kind, participant.identity);

            if (track.kind === LiveKit.Track.Kind.Video) {
                this.attachVideoTrack(track, participant);
            } else if (track.kind === LiveKit.Track.Kind.Audio) {
                this.attachAudioTrack(track, participant);
            }
        });

        // Track unsubscribed
        this.room.on(LiveKit.RoomEvent.TrackUnsubscribed, (track, publication, participant) => {
            console.log('Track unsubscribed:', track.kind);
            track.detach();
        });

        // Disconnected from room
        this.room.on(LiveKit.RoomEvent.Disconnected, (reason) => {
            console.log('Disconnected from room:', reason);
            this.handleDisconnect();
        });

        // Connection quality changed
        this.room.on(LiveKit.RoomEvent.ConnectionQualityChanged, (quality, participant) => {
            console.log('Connection quality:', quality);
        });

        // Data received (Chat messages)
        this.room.on(LiveKit.RoomEvent.DataReceived, (payload, participant) => {
            const decoder = new TextDecoder();
            const text = decoder.decode(payload);
            try {
                const data = JSON.parse(text);
                if (data.type === 'chat') {
                    this.addChatMessage(data.sender || 'FRIDAY', data.message, 'ai');
                }
            } catch (e) {
                // Handle plain text if not JSON
                this.addChatMessage('FRIDAY', text, 'ai');
            }
        });
    }

    attachVideoTrack(track, participant) {
        const videoElement = track.attach();
        videoElement.style.width = '100%';
        videoElement.style.borderRadius = '8px';
        videoElement.setAttribute('data-participant', participant.identity);

        this.videoGrid.appendChild(videoElement);
    }

    attachAudioTrack(track, participant) {
        const audioElement = track.attach();
        audioElement.setAttribute('data-participant', participant.identity);

        this.audioContainer.appendChild(audioElement);
    }

    async toggleMute() {
        if (!this.room) return;

        this.isMuted = !this.isMuted;

        await this.room.localParticipant.setMicrophoneEnabled(!this.isMuted);

        if (this.isMuted) {
            this.muteBtn.classList.add('active');
            this.muteBtn.querySelector('.control-icon').textContent = '🔇';
            this.muteBtn.querySelector('.control-label').textContent = 'Unmute';
        } else {
            this.muteBtn.classList.remove('active');
            this.muteBtn.querySelector('.control-icon').textContent = '🎤';
            this.muteBtn.querySelector('.control-label').textContent = 'Mute';
        }
    }

    async toggleCamera() {
        if (!this.room) return;

        this.isCameraOff = !this.isCameraOff;

        await this.room.localParticipant.setCameraEnabled(!this.isCameraOff);

        if (this.isCameraOff) {
            this.cameraBtn.classList.add('active');
            this.cameraBtn.querySelector('.control-icon').textContent = '📹';
            this.cameraBtn.querySelector('.control-label').textContent = 'Turn On Camera';
        } else {
            this.cameraBtn.classList.remove('active');
            this.cameraBtn.querySelector('.control-icon').textContent = '📹';
            this.cameraBtn.querySelector('.control-label').textContent = 'Camera';
        }
    }

    async handleChatMessage(event) {
        if (event) event.preventDefault();
        const message = this.chatInput.value.trim();
        if (!message || !this.isConnected || !this.room) {
            console.warn('Cannot send message: Not connected or empty message');
            return;
        }

        // Display locally
        this.addChatMessage('You', message, 'user');
        this.chatInput.value = '';

        // Publish to room
        const encoder = new TextEncoder();
        const data = encoder.encode(JSON.stringify({
            type: 'chat',
            message: message,
            sender: 'User'
        }));

        try {
            await this.room.localParticipant.publishData(data, { reliable: true });
        } catch (error) {
            console.error('Failed to send chat message:', error);
        }
    }

    addChatMessage(sender, message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        const senderSpan = document.createElement('span');
        senderSpan.className = 'sender';
        senderSpan.textContent = sender.toUpperCase();

        const textSpan = document.createElement('span');
        textSpan.textContent = message;

        messageDiv.appendChild(senderSpan);
        messageDiv.appendChild(textSpan);

        this.chatMessages.appendChild(messageDiv);

        // Auto-scroll
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async handleDisconnect() {
        if (this.room) {
            this.room.disconnect();
            this.room = null;
        }

        this.isConnected = false;
        this.isMuted = false;
        this.isCameraOff = false;

        // Clear media elements
        this.videoGrid.innerHTML = '';
        this.audioContainer.innerHTML = '';

        // Reset button states
        this.muteBtn.classList.remove('active');
        this.cameraBtn.classList.remove('active');
        this.muteBtn.querySelector('.label').textContent = 'MUTE_INPUT';
        this.cameraBtn.querySelector('.label').textContent = 'CAM_FEED';

        // Show connection panel
        this.showConnectionPanel();
    }

    showSessionPanel() {
        this.connectionPanel.style.display = 'none';
        this.sessionPanel.style.display = 'block';
    }

    showConnectionPanel() {
        this.connectionPanel.style.display = 'block';
        this.sessionPanel.style.display = 'none';

        // Reset form
        const submitBtn = this.connectForm.querySelector('.btn');
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        submitBtn.textContent = 'INITIALIZE_UPLINK';
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, hsl(0, 70%, 50%), hsl(0, 70%, 60%));
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            animation: slideIn 0.3s ease;
            max-width: 400px;
        `;
        errorDiv.textContent = message;

        document.body.appendChild(errorDiv);

        // Add slide-in animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);

        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => errorDiv.remove(), 300);
        }, 5000);
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Expert AI Frontend initialized');
    console.log('LiveKit available:', typeof LiveKit !== 'undefined');
    new ExpertAI();
});
