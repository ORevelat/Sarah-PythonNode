# Sarah-PythonNode
Scripts python remplaçant les modules C# de Sarah v5

listen.py
- snowboy pour la détection du hotword puis l'enregistrement audio
- une fois le silence détecté, envoie du buffer audio en http au remote indiqué en paramètre

== testé/utilisé avec un kinect v1 sous debian 8

speak.py
- simple serveur http écoutant sur le port spécifié et attendant un paramètre speak dans la querystring
- svox pico tts pour la synthèse de la voix

== testé/utilisé sous debian 8
