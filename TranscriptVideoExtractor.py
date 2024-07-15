from youtube_transcript_api import YouTubeTranscriptApi as yta
from youtube_transcript_api._errors import NoTranscriptFound
import os
from fpdf import FPDF  
import re

def extract_video_id(video_url):
    """
    Extrai o ID do vídeo do URL do YouTube.
    """
    # Padrões de regex para diferentes URLs do YouTube
    patterns = [
        r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.match(pattern, video_url)
        if match:
            return match.group(1)  
    return None

def get_transcript(video_id, language_code='en'):
    """
    Obtém o transcript do vídeo do YouTube.
    """
    try:
        transcript = yta.get_transcript(video_id, languages=[language_code])
        return transcript
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_transcript_to_pdf(transcript, file_path):
    """
    Salva o transcript em formato PDF.
    """
    if transcript:
        trans_text = ' '.join(value['text'] for value in transcript)
        
        # Criar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, trans_text)
        
        # Salvar PDF
        pdf.output(file_path)
        
        print(f"Transcript saved to {file_path}")
    else:
        print("Failed to retrieve transcript.")

def get_available_languages(video_id):
    """
    Obtém os idiomas disponíveis para o vídeo.
    """
    try:
        transcript = yta.list_transcripts(video_id)
        languages = [{'language': trans.language, 'language_code': trans.language_code} for trans in transcript]
        return languages
    except NoTranscriptFound:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def choose_language(languages):
    """
    Permite ao usuário escolher um idioma disponível.
    """
    if languages:
        print("Available Languages:")
        for idx, language in enumerate(languages, start=1):
            print(f"{idx}. {language['language_code']} - {language['language']}")
        
        choice = input("Choose a language by entering its number: ")
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(languages):
                return languages[choice_idx]['language_code']
            else:
                print("Invalid choice. Please enter a valid number.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
    else:
        print("No transcripts found for the specified video.")
        return None

def fetch_transcript_from_url(video_url, file_name='transcript.pdf'):
    """
    Função principal para baixar o transcript de um vídeo do YouTube a partir do URL.
    """
    video_id = extract_video_id(video_url)
    if video_id:
        languages = get_available_languages(video_id)
        if languages:
            language_code = choose_language(languages)
            if language_code:
                transcripts_folder = "documents"
                if not os.path.exists(transcripts_folder):
                    os.makedirs(transcripts_folder)
                
                file_path = os.path.join(transcripts_folder, file_name)
                fetch_and_save_transcript(video_id, language_code, file_path)
        else:
            print("No transcripts found for the specified video.")
    else:
        print("Invalid YouTube video URL.")

def fetch_and_save_transcript(video_id, language_code='en', file_path='documents/transcript.pdf'):
    """
    Obtém e salva o transcript em formato PDF.
    """
    try:
        data = get_transcript(video_id, language_code)
        if data:
            save_transcript_to_pdf(data, file_path)
        else:
            print("Transcript not available.")
    except NoTranscriptFound:
        print("Transcript not available. Please check if the video has closed captions.")
    except Exception as e:
        print(f"Error: {e}")

# Exemplo de uso:
if __name__ == "__main__":
    video_url = input("Enter YouTube Video URL: ")
    file_name = input("Enter PDF file name (default: transcript.pdf): ") or "transcript.pdf"
    
    fetch_transcript_from_url(video_url, file_name=file_name)
