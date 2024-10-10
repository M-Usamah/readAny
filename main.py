from src.read_pdf import read_single_page_text, total_pages
from transformers import AutoProcessor, AutoModel
from src.txt_audio import process_long_text
import torch
import subprocess
import os

def play_audio(file_path):
    try:
        # First, try using paplay (PulseAudio)
        subprocess.run(["paplay", file_path], check=True)
    except subprocess.CalledProcessError:
        try:
            # If paplay fails, try aplay (ALSA)
            subprocess.run(["aplay", file_path], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to play audio file: {file_path}")
            print("Make sure you have PulseAudio or ALSA installed.")

def main():
    book = "Artificial Intelligence A Modern Approach.pdf"
    pages = total_pages(book)
    page_num = 19
    model_name = "suno/bark-small"
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    while 0 <= page_num < pages:
        content_info = read_single_page_text(book, page_num)
        content = content_info[1]
        output_file = f"page_{page_num}.wav"
        process_long_text(content, processor, model, device, output_file=output_file)
        print("\n\n\n\n\n\n\n\n\n")
        print(content)
        print(f"{page_num}/{pages}")
        
        # Play the generated audio
        play_audio(output_file)

        in_page = input('''
                        Press According to the following option
                        1) Next Page (n)
                        2) Previous Page (p)
                        3) Exit (e)
                        ''')
        if in_page.lower() == 'n':
            page_num += 1
        elif in_page.lower() == "p":
            page_num -= 1
        elif in_page.lower() == "e":
            break
        else:
            print("Invalid input. Please try again.")

    # Clean up temporary audio files
    for file in os.listdir():
        if file.startswith("page_") and file.endswith(".wav"):
            os.remove(file)

if __name__ == "__main__":
    main()