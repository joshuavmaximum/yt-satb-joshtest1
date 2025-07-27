class YouTubeToMIDIConverter {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentProcess = null;
    }

    initializeElements() {
        this.youtubeUrlInput = document.getElementById('youtube-url');
        this.validateBtn = document.getElementById('validate-btn');
        this.processBtn = document.getElementById('process-btn');
        this.progressSection = document.getElementById('progress-section');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.statusLog = document.getElementById('status-log');
        this.resultsSection = document.getElementById('results-section');
        this.midiTracks = document.getElementById('midi-tracks');
        this.loadingModal = document.getElementById('loading-modal');
        this.audioQualitySelect = document.getElementById('audio-quality');
        this.midiResolutionSelect = document.getElementById('midi-resolution');
    }

    bindEvents() {
        this.validateBtn.addEventListener('click', () => this.validateYouTubeUrl());
        this.processBtn.addEventListener('click', () => this.processVideo());
        this.youtubeUrlInput.addEventListener('input', () => this.handleUrlInput());
        this.youtubeUrlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.validateYouTubeUrl();
            }
        });
    }

    handleUrlInput() {
        const url = this.youtubeUrlInput.value.trim();
        this.validateBtn.disabled = !url;
        this.processBtn.disabled = true;
    }

    async validateYouTubeUrl() {
        const url = this.youtubeUrlInput.value.trim();
        if (!url) {
            this.showError('Please enter a YouTube URL');
            return;
        }

        if (!this.isValidYouTubeUrl(url)) {
            this.showError('Please enter a valid YouTube URL');
            return;
        }

        this.validateBtn.disabled = true;
        this.validateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validating...';

        try {
            // Simulate validation (in a real app, you'd make an API call)
            await this.simulateValidation(url);
            
            this.validateBtn.innerHTML = '<i class="fas fa-check"></i> Valid';
            this.validateBtn.style.background = '#28a745';
            this.processBtn.disabled = false;
            this.addLogEntry('URL validated successfully', 'success');
        } catch (error) {
            this.showError('Failed to validate URL: ' + error.message);
            this.validateBtn.disabled = false;
            this.validateBtn.innerHTML = '<i class="fas fa-check"></i>';
        }
    }

    isValidYouTubeUrl(url) {
        const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[a-zA-Z0-9_-]{11}/;
        return youtubeRegex.test(url);
    }

    async simulateValidation(url) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, 1000);
        });
    }

    async processVideo() {
        const url = this.youtubeUrlInput.value.trim();
        const audioQuality = this.audioQualitySelect.value;
        const midiResolution = this.midiResolutionSelect.value;

        if (!url) {
            this.showError('Please enter a YouTube URL');
            return;
        }

        this.showLoadingModal();
        this.showProgressSection();
        this.resetProgress();

        try {
            // Step 1: Extract video ID and download audio
            this.updateProgress(10, 'Extracting video information...');
            this.addLogEntry('Starting video processing...', 'info');
            
            const videoId = this.extractVideoId(url);
            this.addLogEntry(`Video ID extracted: ${videoId}`, 'success');

            // Step 2: Download audio from YouTube
            this.updateProgress(20, 'Downloading audio from YouTube...');
            this.addLogEntry('Downloading audio file...', 'info');
            
            const audioData = await this.downloadAudio(url, audioQuality);
            this.addLogEntry('Audio download completed', 'success');

            // Step 3: Process with Spleeter API
            this.updateProgress(40, 'Separating audio tracks with Spleeter...');
            this.addLogEntry('Processing with Spleeter API...', 'info');
            
            const separatedTracks = await this.processWithSpleeter(audioData);
            this.addLogEntry('Audio separation completed', 'success');

            // Step 4: Convert to MIDI
            this.updateProgress(70, 'Converting to MIDI format...');
            this.addLogEntry('Converting audio tracks to MIDI...', 'info');
            
            const midiFiles = await this.convertToMIDI(separatedTracks, midiResolution);
            this.addLogEntry('MIDI conversion completed', 'success');

            // Step 5: Generate results
            this.updateProgress(90, 'Generating download files...');
            this.addLogEntry('Preparing MIDI files for download...', 'info');
            
            await this.generateResults(midiFiles);
            
            this.updateProgress(100, 'Processing completed!');
            this.addLogEntry('All processing completed successfully!', 'success');
            
            this.hideLoadingModal();
            this.showResults();

        } catch (error) {
            this.addLogEntry(`Error: ${error.message}`, 'error');
            this.hideLoadingModal();
            this.showError('Processing failed: ' + error.message);
        }
    }

    extractVideoId(url) {
        const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
    }

    async downloadAudio(url, quality) {
        // Simulate audio download
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    format: quality === 'high' ? 'wav' : 'mp3',
                    quality: quality,
                    duration: Math.random() * 300 + 60 // 1-6 minutes
                });
            }, 2000);
        });
    }

    async processWithSpleeter(audioData) {
        // Simulate Spleeter processing
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    vocals: { data: 'vocals_audio', confidence: 0.85 },
                    drums: { data: 'drums_audio', confidence: 0.92 },
                    bass: { data: 'bass_audio', confidence: 0.88 },
                    piano: { data: 'piano_audio', confidence: 0.78 },
                    other: { data: 'other_audio', confidence: 0.82 }
                });
            }, 3000);
        });
    }

    async convertToMIDI(separatedTracks, resolution) {
        // Simulate MIDI conversion
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    vocals: {
                        filename: 'vocals.mid',
                        data: this.generateMockMIDIData('vocals'),
                        notes: 45,
                        duration: 180
                    },
                    drums: {
                        filename: 'drums.mid',
                        data: this.generateMockMIDIData('drums'),
                        notes: 23,
                        duration: 180
                    },
                    bass: {
                        filename: 'bass.mid',
                        data: this.generateMockMIDIData('bass'),
                        notes: 67,
                        duration: 180
                    },
                    piano: {
                        filename: 'piano.mid',
                        data: this.generateMockMIDIData('piano'),
                        notes: 89,
                        duration: 180
                    },
                    other: {
                        filename: 'other.mid',
                        data: this.generateMockMIDIData('other'),
                        notes: 34,
                        duration: 180
                    }
                });
            }, 2000);
        });
    }

    generateMockMIDIData(trackType) {
        // Generate mock MIDI data for demonstration
        const base64Data = btoa(`Mock MIDI data for ${trackType} track`);
        return base64Data;
    }

    async generateResults(midiFiles) {
        // Simulate file generation
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(midiFiles);
            }, 1000);
        });
    }

    showResults() {
        const tracks = [
            { name: 'Vocals', type: 'vocals', icon: 'fas fa-microphone' },
            { name: 'Drums', type: 'drums', icon: 'fas fa-drum' },
            { name: 'Bass', type: 'bass', icon: 'fas fa-guitar' },
            { name: 'Piano', type: 'piano', icon: 'fas fa-piano' },
            { name: 'Other', type: 'other', icon: 'fas fa-music' }
        ];

        this.midiTracks.innerHTML = '';
        
        tracks.forEach(track => {
            const trackElement = this.createTrackElement(track);
            this.midiTracks.appendChild(trackElement);
        });

        this.resultsSection.style.display = 'block';
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    createTrackElement(track) {
        const trackDiv = document.createElement('div');
        trackDiv.className = 'midi-track';
        
        trackDiv.innerHTML = `
            <div class="track-header">
                <div class="track-icon ${track.type}">
                    <i class="${track.icon}"></i>
                </div>
                <div class="track-info">
                    <h4>${track.name}</h4>
                    <p>MIDI file with ${Math.floor(Math.random() * 100) + 20} notes</p>
                </div>
            </div>
            <div class="track-actions">
                <button class="track-btn download-btn" onclick="app.downloadMIDIFile('${track.type}')">
                    <i class="fas fa-download"></i> Download
                </button>
                <button class="track-btn preview-btn" onclick="app.previewMIDIFile('${track.type}')">
                    <i class="fas fa-play"></i> Preview
                </button>
            </div>
        `;
        
        return trackDiv;
    }

    downloadMIDIFile(trackType) {
        const filename = `${trackType}.mid`;
        const mockData = this.generateMockMIDIData(trackType);
        
        // Create a blob and download link
        const blob = new Blob([mockData], { type: 'audio/midi' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.addLogEntry(`Downloaded ${filename}`, 'success');
    }

    previewMIDIFile(trackType) {
        // In a real implementation, this would play the MIDI file
        this.addLogEntry(`Previewing ${trackType} track...`, 'info');
        
        // Simulate MIDI playback
        setTimeout(() => {
            this.addLogEntry(`${trackType} track preview completed`, 'success');
        }, 2000);
    }

    showProgressSection() {
        this.progressSection.style.display = 'block';
        this.progressSection.scrollIntoView({ behavior: 'smooth' });
    }

    updateProgress(percentage, text) {
        this.progressFill.style.width = `${percentage}%`;
        this.progressText.textContent = text;
    }

    resetProgress() {
        this.progressFill.style.width = '0%';
        this.progressText.textContent = 'Initializing...';
        this.statusLog.innerHTML = '';
    }

    addLogEntry(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.textContent = `[${timestamp}] ${message}`;
        this.statusLog.appendChild(logEntry);
        this.statusLog.scrollTop = this.statusLog.scrollHeight;
    }

    showLoadingModal() {
        this.loadingModal.style.display = 'block';
    }

    hideLoadingModal() {
        this.loadingModal.style.display = 'none';
    }

    showError(message) {
        this.addLogEntry(message, 'error');
        alert(message);
    }
}

// Initialize the app when the page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new YouTubeToMIDIConverter();
});

// Add some utility functions for the Spleeter API integration
class SpleeterAPI {
    constructor() {
        this.baseUrl = 'https://api.spleeter.ai'; // Example API endpoint
        this.apiKey = null;
    }

    setApiKey(key) {
        this.apiKey = key;
    }

    async separateAudio(audioData, stems = 5) {
        const formData = new FormData();
        formData.append('audio', audioData);
        formData.append('stems', stems);

        const response = await fetch(`${this.baseUrl}/separate`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Spleeter API error: ${response.statusText}`);
        }

        return await response.json();
    }

    async convertToMIDI(audioTrack, options = {}) {
        const formData = new FormData();
        formData.append('audio', audioTrack);
        formData.append('resolution', options.resolution || 240);
        formData.append('quality', options.quality || 'medium');

        const response = await fetch(`${this.baseUrl}/convert-midi`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`MIDI conversion error: ${response.statusText}`);
        }

        return await response.blob();
    }
}

// Export for use in other modules
window.SpleeterAPI = SpleeterAPI;