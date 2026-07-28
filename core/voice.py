import subprocess

MODEL_PATH = "/home/ny_san/piper-voices/en_US-lessac-medium.onnx"
PIPER_BIN = "/home/ny_san/piper-tts/piper/piper"
OUTPUT_WAV = "output.wav"


def synthesize(texte, output_path=OUTPUT_WAV):
    """
    Génère le fichier audio SANS le jouer. Retourne True si la synthèse
    a réussi, False sinon. Séparé de play() pour permettre d'afficher
    le texte au même moment que le début de la lecture audio.
    """
    result = subprocess.run(
        [PIPER_BIN, "-m", MODEL_PATH, "-f", output_path],
        input=texte.encode("utf-8"),
        capture_output=True
    )
    if result.returncode != 0:
        print("Erreur Piper:", result.stderr.decode())
        return False
    return True


def play(output_path=OUTPUT_WAV):
    """Joue le fichier audio déjà généré par synthesize()."""
    subprocess.run(["aplay", output_path])


def parler(texte):
    """
    Comportement historique : synthèse + lecture immédiate, dans l'ordre.
    Toujours utilisable si tu veux la voix sans te soucier de la synchro
    avec le texte affiché.
    """
    if synthesize(texte):
        play()