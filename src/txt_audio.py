from transformers import AutoProcessor, AutoModel
import scipy.io.wavfile as wavfile
import numpy as np
import torch

def split_text(text, max_length=200) -> list[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def generate_audio(text, processor, model, device):
    inputs = processor(text, return_tensors='pt', voice_preset="v2/en_speaker_9")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    speech_values = model.generate(**inputs)
    return speech_values.cpu().numpy().squeeze()

def process_long_text(text, processor, model, device, output_file="output.wav", sample_rate=24000):
    """Process long text by splitting it into chunks and generating audio for each chunk."""
    chunks = split_text(text)
    audio_chunks = []
    for chunk in chunks:
        audio_chunk = generate_audio(chunk, processor, model, device)
        audio_chunks.append(audio_chunk)
    # Concatenate all audio chunks
    full_audio = np.concatenate(audio_chunks)
    # Normalize audio
    full_audio = full_audio / np.max(np.abs(full_audio))
    # Save as WAV file
    wavfile.write(output_file, sample_rate, (full_audio * 32767).astype(np.int16))

if __name__ == "__main__":
    processor = AutoProcessor.from_pretrained("suno/bark-small")
    model = AutoModel.from_pretrained("suno/bark-small")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    # Example long text
    long_text = """
    Artificial intelligence has transformed various aspects of our lives, from voice assistants to autonomous vehicles.
    As we continue to push the boundaries of what's possible with AI, we must also consider the ethical implications
    and potential risks associated with these advancements. Responsible development and deployment of AI technologies
    are crucial to ensure that they benefit society as a whole while minimizing potential harm.
    """
    process_long_text(long_text, processor, model, device)
    print("Audio generated and saved as 'output.wav'")