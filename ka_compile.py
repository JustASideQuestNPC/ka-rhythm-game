'''
Python script to convert compiled Javascript into a copy-pasteable file for Khan Academy.
'''
from pathlib import Path
import re

OUTFILE_PATH = 'ka_build.html'
JS_FOLDER = './js_build/src'
# files in load order
LOAD_ORDER = [
    'main'
]

# converts all filenames to camel case
to_camel_case_regex = re.compile(r"\-[a-z]")

# convert relative paths to absolute ones
root_path = Path(__file__).parent
OUTFILE_PATH = (root_path / OUTFILE_PATH).resolve()

# used if there isn't an existing build file
DEFAULT_HTML_START = '''
<!DOCTYPE html><html>
<!--
Comments go here.
-->
<head>
    <title>KA Typescript Template</title>
    <!-- It is WILD to me that I can just grab whatever jsdelivr packages I want. -->
    <script src="https://cdn.jsdelivr.net/npm/p5@2.2.3/lib/p5.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display&family=Roboto+Mono&display=swap" rel="stylesheet">
<!-- main project code -->
<script type>(()=>{
'''
DEFAULT_HTML_END = '''
})();</script>
</head>
<body style="margin:0;overflow:hidden;">
<!--The Thumbnail Script 2.1.0 12/18/2023 by Bluebird@kaid_157624541333313939750668--><script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script><script type>var r=600,s=document.documentElement.clientWidth;window.parent.html2canvas=t=>{try{html2canvas(document.body,{width:s,height:s,useCORS:!0,onclone:t=>t.getAnimations().forEach((t=>{try{t.finish()}catch{}}))}).then((t=>{var e=document.createElement("canvas");e.width=r,e.height=r,e.getContext("2d").drawImage(t,0,0,t.width,t.height,0,0,r,r),window.top.postMessage(e.toDataURL(),"*")})).catch((t=>{alert("Thumbnail Script Error: "+t)}))}catch{window.top.postMessage(document.createElement("canvas").toDataURL(),"*")}};
</script>
<script>/*Extra Script tag for reload button.*/</script>
</body>
</html>
'''

def to_camel_case(string: str) -> str:
    return to_camel_case_regex.sub(lambda s: s.group()[1].upper(), string)

def parse_code_file(file_name: str, lines: list[str]) -> list[str]:
    temp = to_camel_case(file_name)
    if temp != file_name:
        print(f'parsing build file "{file_name}" as "{temp}":')
        file_name = temp
    else:
        print(f'parsing build file "{file_name}":')

    # find imports and exports
    folder_structure = file_name.split('_')
    enclosing_folders = folder_structure[:-1]
    print(f'folder structure: {folder_structure}')
    print(f'enclosing folders: {enclosing_folders}')

    imports: dict[str, str] = {}
    exports: dict[str, str] = {}

    for line in lines:
        if line.startswith('import'):
            chunks = line.split(' ')

            # find prefix for the import
            import_source = chunks[-1][1:-6]
            source_folders = import_source.split('/')
            source_name = ''
            if source_folders[0] == '.':
                temp = folder_structure[:-1]
                temp.extend(source_folders[1:])
                source_name = '_'.join(temp)
            else:
                last_common_index = len(folder_structure) - 1
                source_start_index = 0
                for folder in source_folders:
                    if folder == '..':
                        last_common_index -= 1
                        source_start_index += 1
                        if last_common_index == 0:
                            break
                    else:
                        break
                
                temp = folder_structure[:last_common_index]
                temp.extend(source_folders[source_start_index:])
                source_name = '_'.join(temp)

            if chunks[1] == '{':
                imported_names: list[str] = []
                i = 2
                while i < len(chunks) and chunks[i] != '}':
                    name = chunks[i]
                    if name[-1] == ',':
                        name = name[:-1]
                    imported_names.append(name)
                    i += 1

                for name in imported_names:
                    full_import_name = f'{to_camel_case(source_name)}_{name}'
                    imports[name] = full_import_name
                    print(f'file imports "{name}" as "{full_import_name}"')
            else:
                full_import_name = f'{to_camel_case(source_name)}_{chunks[1]}'
                imports[chunks[1]] = full_import_name
                print(f'file imports "{chunks[1]}" as "{full_import_name}"')

        elif line.startswith('export'):
            chunks = line.split(' ')
            if chunks[1] == 'default':
                print(f'file exports default "{chunks[3]}" as "{file_name}" ')
                exports[chunks[3]] = file_name
            else:
                raw_name = chunks[2] if chunks[1] != 'async' else chunks[3]
                if raw_name.rfind(' ') != -1:
                    raw_name = raw_name[:raw_name.rfind(' ')]
                if raw_name.rfind('=') != -1:
                    raw_name = raw_name[:raw_name.rfind('=')]
                if raw_name.rfind('(') != -1:
                    raw_name = raw_name[:raw_name.rfind('(')]
                export_name = f'{file_name}_{raw_name}'    
                print(f'file exports "{raw_name}" as "{export_name}" ')
                exports[raw_name] = export_name

    code_lines: list[str] = [];
    num_imports = 0
    for line in lines:
        if line.startswith('import'):
            continue

        line = line.replace('export default ', '').replace('export ', '')

        for name, full_name in imports.items():
            replaced_line = re.sub(rf'(^|(?<= |_|-|\(|\{{|\-|\+)){name}(?=\(|\)| |\.|;|\[|\}})', full_name, line)
            if replaced_line != line:
                line = replaced_line
                num_imports += 1

        code_lines.append(line)

    # print(f'replaced {num_imports} imports\n')
    print('')

    output_lines: list[str] = [f'/** src/{file_name.replace('_', '/')}.ts **/\n']
    for full_name in exports.values():
        output_lines.append(f'var {full_name};\n')
    output_lines.append('(()=>{\n')

    output_lines.extend([f'    {line}' for line in code_lines])

    for name, full_name in exports.items():
        # print(f'{name}, {full_name}')
        output_lines.append(f'    {full_name} = {name};\n')
    output_lines.append('})();\n')

    return output_lines

leading_lines = []
trailing_lines = []

if OUTFILE_PATH.exists():
    print('loading previous build...')
    html_lines = []
    with open(OUTFILE_PATH) as file:
        html_lines = file.readlines()

    buffer = ''
    while buffer != '<script type>(()=>{\n' and len(html_lines) > 0:
        buffer = html_lines.pop(0)
        leading_lines.append(buffer)

    # consume and erase old code
    while len(html_lines) > 1 and html_lines[0] != '})();</script>\n':
        html_lines.pop(0)

    trailing_lines = html_lines
else:
    print('no build file exists, creating it')
    leading_lines = [f'{str}\n' for str in DEFAULT_HTML_START.split('\n')][1:]
    trailing_lines = [f'{str}\n' for str in DEFAULT_HTML_END.split('\n')][1:]
    

print('loading new build files...')
JS_FOLDER = (root_path / JS_FOLDER).resolve()
js_files: list[tuple[str, Path]] = []
for filename in LOAD_ORDER:
    full_path = ( JS_FOLDER / f'{filename}.js' ).resolve()
    if not full_path.exists():
        print(f'build file {filename} does not exist')
    else:
        js_files.append((filename.replace('/', '_'), full_path))

print(f'found {len(js_files)} build files')

print('parsing build files...')
code_lines = [];
for path in js_files:
    with open(path[1]) as file:
        lines = file.readlines()
        code_lines.extend(parse_code_file(path[0], lines))
        code_lines.append('\n')
code_lines = code_lines[:-1]

print('writing new code...')
with open(OUTFILE_PATH, 'w') as file:
    file.write(''.join(leading_lines))
    file.write(''.join(code_lines) + '\n')
    file.write(''.join(trailing_lines))

print('build completed!')