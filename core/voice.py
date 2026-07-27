import subprocess

MODEL_PATH = "/home/ny_san/piper-voices/en_US-lessac-medium.onnx"
PIPER_BIN = "/home/ny_san/piper-tts/piper/piper"

def parler(texte):
    result = subprocess.run(
        [PIPER_BIN, "-m", MODEL_PATH, "-f", "output.wav"],
        input=texte.encode("utf-8"),
        capture_output=True
    )
    if result.returncode != 0:
        print("Erreur Piper:", result.stderr.decode())
        return
    subprocess.run(["aplay", "output.wav"])