'''
Builds Typescript and fixes import errors so my live server works. I SHOULD NOT HAVE TO DO THIS.
'''
from pathlib import Path
import subprocess
import os

JS_FOLDER = 'js_build/src'

# convert relative paths to absolute ones
root_path = Path(__file__).parent
JS_FOLDER = (root_path / JS_FOLDER).resolve()
script_path = (root_path / 'node_modules/.bin/tsc.cmd').resolve()
config_path = (root_path / 'tsconfig.json').resolve();

print('building typescript...')
process_result = subprocess.run(f'{script_path} -p {config_path}')
if process_result.returncode != 0:
    print('error building typescript!')
    quit()

print('removing p5 imports...')
for root, dirs, files in os.walk(JS_FOLDER):
    for file_name in files:
        file_path = f'{root}/{file_name}'
        print(f'parsing {file_path}')
        lines: list[str] = []
        with open(file_path) as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip('\n') != 'import p5 from "p5";':
                    file.write(line)

print('build complete!')