from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
import os
from datetime import datetime, timedelta

app = Flask(__name__)
AUDIO_DIR = 'static/audios'
os.makedirs(AUDIO_DIR, exist_ok=True)

# Limpa áudios com mais de 1 hora
def limpar_audios_antigos():
    agora = datetime.now()
    for f in os.listdir(AUDIO_DIR):
        caminho = os.path.join(AUDIO_DIR, f)
        if os.path.isfile(caminho):
            criado = datetime.fromtimestamp(os.path.getctime(caminho))
            if agora - criado > timedelta(hours=1):
                os.remove(caminho)

@app.route('/', methods=['GET', 'POST'])
def index():
    limpar_audios_antigos()
    audio_file = None

    if request.method == 'POST':
        texto = request.form.get('texto')
        idioma = request.form.get('idioma', 'pt')
        voz = request.form.get('voz', 'feminina')

        if texto.strip():
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"audio_{timestamp}.mp3"
            filepath = os.path.join(AUDIO_DIR, filename)

            # Usar gTTS (voz feminina online)
            if voz == 'feminina':
                tts = gTTS(text=texto, lang=idioma)
                tts.save(filepath)
            else:
                # Simulação com voz masculina (via sistema local - pyttsx3)
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    voices = engine.getProperty('voices')
                    # Tenta selecionar voz masculina
                    for v in voices:
                        if "male" in v.name.lower() or "masculina" in v.name.lower():
                            engine.setProperty('voice', v.id)
                            break
                    engine.save_to_file(texto, filepath)
                    engine.runAndWait()
                except Exception as e:
                    print("Erro ao usar pyttsx3:", e)

            audio_file = filename

    audios = sorted(os.listdir(AUDIO_DIR), reverse=True)
    return render_template('index.html', audio_file=audio_file, audios=audios)

@app.route('/audios/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)





