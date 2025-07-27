// Configuration file for YouTube to MIDI Converter
const CONFIG = {
    // Spleeter API Configuration
    SPLEETER_API: {
        BASE_URL: 'https://api.spleeter.ai', // Example API endpoint
        ENDPOINTS: {
            SEPARATE: '/separate',
            CONVERT_MIDI: '/convert-midi',
            STATUS: '/status'
        },
        DEFAULT_STEMS: 5,
        SUPPORTED_STEMS: [2, 4, 5],
        MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
        TIMEOUT: 300000 // 5 minutes
    },

    // YouTube Configuration
    YOUTUBE: {
        SUPPORTED_FORMATS: [
            'https://www.youtube.com/watch?v=',
            'https://youtu.be/',
            'https://www.youtube.com/embed/'
        ],
        MAX_DURATION: 3600, // 1 hour in seconds
        SUPPORTED_QUALITIES: ['low', 'medium', 'high']
    },

    // MIDI Configuration
    MIDI: {
        SUPPORTED_RESOLUTIONS: [120, 240, 480],
        DEFAULT_RESOLUTION: 240,
        SUPPORTED_TRACKS: ['vocals', 'drums', 'bass', 'piano', 'other'],
        TRACK_COLORS: {
            vocals: '#e91e63',
            drums: '#ff9800',
            bass: '#2196f3',
            piano: '#4caf50',
            other: '#9c27b0'
        },
        TRACK_ICONS: {
            vocals: 'fas fa-microphone',
            drums: 'fas fa-drum',
            bass: 'fas fa-guitar',
            piano: 'fas fa-piano',
            other: 'fas fa-music'
        }
    },

    // Processing Configuration
    PROCESSING: {
        CHUNK_SIZE: 1024 * 1024, // 1MB chunks
        PROGRESS_UPDATE_INTERVAL: 1000, // 1 second
        MAX_RETRIES: 3,
        RETRY_DELAY: 2000 // 2 seconds
    },

    // UI Configuration
    UI: {
        ANIMATION_DURATION: 300,
        TOAST_DURATION: 5000,
        MAX_LOG_ENTRIES: 100,
        AUTO_SCROLL_LOG: true
    },

    // Error Messages
    ERRORS: {
        INVALID_URL: 'Please enter a valid YouTube URL',
        NETWORK_ERROR: 'Network error. Please check your connection.',
        PROCESSING_ERROR: 'Processing failed. Please try again.',
        FILE_TOO_LARGE: 'File is too large. Please try a shorter video.',
        UNSUPPORTED_FORMAT: 'Unsupported video format.',
        API_ERROR: 'API service error. Please try again later.',
        DOWNLOAD_ERROR: 'Download failed. Please try again.'
    },

    // Success Messages
    SUCCESS: {
        URL_VALIDATED: 'URL validated successfully',
        AUDIO_DOWNLOADED: 'Audio download completed',
        SEPARATION_COMPLETE: 'Audio separation completed',
        MIDI_CONVERTED: 'MIDI conversion completed',
        PROCESSING_COMPLETE: 'All processing completed successfully!',
        FILE_DOWNLOADED: 'File downloaded successfully'
    },

    // Development Configuration
    DEV: {
        DEBUG_MODE: false,
        MOCK_API: true, // Set to false for real API calls
        LOG_LEVEL: 'info', // 'debug', 'info', 'warn', 'error'
        API_TIMEOUT: 10000 // 10 seconds for development
    }
};

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
}