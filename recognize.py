from GLOBAL import DRAFT_TEXT_PATH, AUDIO_OUTPUT_PATH
import whisper
import warnings
import sys

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")


#INFILENAME = 'output.wav'
INFILENAME = AUDIO_OUTPUT_PATH
OUTFILENAME = DRAFT_TEXT_PATH

def recognizing_by_whisper(model_name="base", in_file_name='output.wav', out_file_name='output.txt'):
    print("Распознание начато")
    model = whisper.load_model(model_name)
    result = model.transcribe(in_file_name, language="ru")

    with open(OUTFILENAME, 'w', encoding='utf-8') as f:
        f.write(result["text"])
        
    return result["text"]


def recognize(in_file_name, out_file_name):
    recognizing_by_whisper(in_file_name=INFILENAME, out_file_name=OUTFILENAME)

if __name__ == "__main__" and "--no-main" not in sys.argv:
    print("Распознанный текст:", recognize(INFILENAME, OUTFILENAME))

else:
    recognize(INFILENAME, OUTFILENAME)
