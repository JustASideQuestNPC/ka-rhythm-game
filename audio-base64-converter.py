'''
Simple python script to wrap the base64 song strings in a JS string, because all of them are so
large that VSCode crashes if I try to do it manually.
'''

from pathlib import Path

FILE_PATH = Path.cwd() / 'songs/flavor-foley-weiward-romance/audio.js'
SONG_NAME = 'flavorFoleyWeiwardRomance'

with open(FILE_PATH) as file_reader:
    contents = f'var {SONG_NAME} = "data:audio/mpeg;base64,{file_reader.read()}";'
    with open(FILE_PATH, 'w') as file_writer:
        file_writer.write(contents)
