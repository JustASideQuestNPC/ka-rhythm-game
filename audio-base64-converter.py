'''
Simple python script to wrap the base64 song strings in a JS string, because all of them are so
large that VSCode crashes if I try to do it manually.
'''

from pathlib import Path

FILE_PATH = Path.cwd() / 'songs/flavor-foley-ft-feng-yi-weiward-romance/audio.js'
SONG_NAME = 'flavor-foley-weiward-romance'

with open(FILE_PATH) as file_reader:
    contents = (
        f'console.log("loading base64 audio for song {SONG_NAME}"); '
         'if (typeof audioStrings === "undefined") { var audioStrings = {}; '
         'console.log("creating audioString object"); }\n'
         'if (typeof audioStrings["{SONG_NAME}"] === "undefined") ''{ '
        f'console.log("adding song: {SONG_NAME}"); '
        f'audioStrings["{SONG_NAME}"] = '
        f'"data:audio/mpeg;base64,{file_reader.read()}"; ''}')
    with open(FILE_PATH, 'w') as file_writer:
        file_writer.write(contents)
