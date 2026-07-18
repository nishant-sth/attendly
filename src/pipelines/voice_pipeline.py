import librosa
import torch
import numpy as np
import streamlit as st
import io
from speechbrain.inference.speaker import EncoderClassifier
from scipy.spatial.distance import cosine


@st.cache_resource
def load_encoder_model():
    encoder = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb"
        )
    return encoder

def preprocess_audio(audio_path, sample_rate=16000):
    audio, sr = librosa.load(io.BytesIO(audio_path), sr=sample_rate)

    # Remove silence
    audio, _ = librosa.effects.trim(audio, top_db=30)

    # Normalize volume
    audio = librosa.util.normalize(audio)
    return audio


def get_voice_embedding(audio_path):
        try:
            encoder = load_encoder_model()
            audio = preprocess_audio(audio_path)
            # numpy -> torch tensor
            waveform = torch.tensor(audio,dtype=torch.float32)

            # SpeechBrain expects batch dimension
            waveform = waveform.unsqueeze(0)

            with torch.no_grad():
                embedding = encoder.encode_batch(waveform)
            embedding = embedding.squeeze()
            return embedding.tolist()
        
        except Exception as e:
            st.error("Voice Recognition error!")
            return None


# identify speakers
def identify_speaker(new_embedding, candidate_dict, threshold=0.65):
    if new_embedding is None or not candidate_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity >= best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score


def process_bulk_audio(audio_bytes, candidate_dict, threshold=0.65): 
    try:
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identify_results = {}

        for start, end in segments:
            if (start-end) < sr*0.5:
                continue
            segment_audio = audio[start:end]
            embedding = get_voice_embedding(segment_audio)  

            sid, score = identify_speaker(embedding, candidate_dict, threshold)
            if sid:
                if sid not in identify_speaker or score > identify_results[sid]:
                    identify_results[sid] = score
            return identify_results
    except Exception as e:
        st.error("Bulk processing error")
        return {}