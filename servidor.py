# -*- coding: utf-8 -*-
"""
Created on Thu May 15 22:45:45 2025

@author: Neftali Carranza
"""

from flask import Flask, request, send_file
import numpy as np
import soundfile as sf

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_bytes = request.data
    with open('audio_recibido.raw', 'wb') as f:
        f.write(audio_bytes)
    print("Audio recibido y guardado.")
    # Convertir raw PCM a WAV para playback fácil (suponiendo 16-bit unsigned)
    data = np.frombuffer(audio_bytes, dtype=np.uint16)
    sf.write('audio_recibido.wav', data, 5000)
    return "Archivo recibido", 200

@app.route('/')
def index():
    return """
    <h2>Estetoscopio Digital - Audio Recibido</h2>
    <audio controls>
      <source src="/audio" type="audio/wav">
      Tu navegador no soporta audio.
    </audio>
    """

@app.route('/audio')
def serve_audio():
    try:
        return send_file('audio_recibido.wav', mimetype='audio/wav')
    except Exception:
        return "Archivo no encontrado", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
