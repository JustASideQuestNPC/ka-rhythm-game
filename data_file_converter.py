'''
Simple python script to wrap chart text and base64 audio/image strings into a JS file. I'd do this
manually, but most of the files are so large that doing it myself crashes VSCode.
'''

from pathlib import Path

FILE_PATH = Path.cwd() / 'songs/flavor-foley-weiward-romance/audio.js'

file_type = ('audio' if FILE_PATH.parts[-1] == 'audio.js' else
             'thumbnail' if FILE_PATH.parts[-1] == 'thumbnail.js' else
             'chart') # FILE_PATH.parts[-1] == 'chart.js'

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

base_name = to_camel_case(FILE_PATH.parts[-2])

with open(FILE_PATH) as file_reader:
    contents = ''
    if file_type == 'audio':
        contents = f'var {base_name}_audio = "data:audio/mpeg;base64,{file_reader.read()}";'
    elif file_type == 'thumbnail':
        contents = f'var {base_name}_thumbnail = "data:content/type;base64,{file_reader.read()}";'
    else: # file_type == 'chart'
        contents = f'var {base_name}_chart = `{file_reader.read()}`;'
    with open(FILE_PATH, 'w') as file_writer:
        file_writer.write(contents)
