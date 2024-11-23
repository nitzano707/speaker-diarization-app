from flask import Flask, request, jsonify, render_template
from gradio_client import Client, file

app = Flask(__name__)

# הגדרות Space של Hugging Face
SPACE_NAME = "Delik/pyannote-speaker-diarization-3.1"
client = Client(SPACE_NAME)

@app.route('/')
def index():
    return render_template('index.html')  # ממשק ה-Frontend

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio']
    file_path = f"uploads/{audio_file.filename}"
    audio_file.save(file_path)

    # שליחת קובץ ל-Space
    result = client.predict(
        audio=file(file_path),
        num_speakers=0,
        min_speakers=0,
        max_speakers=0,
        api_name="/process_audio"
    )

    return jsonify({
        "transcription": result[0],  # טקסט עם זיהוי דוברים
        "download_link": result[1]  # קובץ הורדה בפורמט DAW
    })

if __name__ == "__main__":
    app.run(debug=True)
