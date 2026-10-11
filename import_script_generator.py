'''
Generates the script tags for importing songs.
'''

from string import punctuation

# this is very much not the proper way to check if a module is installed, but the actual way is like
# 20 lines and not worth it for this
clip = None
try:
    import pyperclip
    print('pyperclip is installed, import scripts will be copied to clipboard\n')
    clip = pyperclip
except ImportError:
    pass

# songs, organized into "packs" that are in their own collapsible div with my justification for why
# they're all fine copyright-wise
SONGS = (
    (
        'Warriyo ft. Laura Brehm - Mortals',
        'Jim Yosef - Firefly',
        'DEAF KEV - Invincible',
        'Diviners ft. Philly K - Savannah'
    ),
    (
        'ROMA - NEURODIVERGENCE',
        'ROMA ft. Kasane Teto - DANCIN VIBES'
    ),
    (
        'Good Kid - Coffee',
        'Good Kid - Eastside',
        'Good Kid - Tornado'
    ),
    (
        'Meganeko - nano love',
    ),
    (
        'FLAVOR FOLEY ft. Feng Yi - WEIWARD ROMANCE',
        'FLAVOR FOLEY ft. Chis-A - Clover',
        'FLAVOR FOLEY ft. SF-A2 Miki - Human',
        'FLAVOR FOLEY ft. Eleanor Forte - weathergirl',
        'Isidore & Monochro Menace ft. Megurine Luka - FEEDBACK',
        'Monochro Menace ft. Kasane Teto - WHODUNIT',
        'worzy ft. Kasane Teto vs. Yi Xi - THE HEART OF WAR',
        'rai1367 - Rockabye',
        'Hobisu ft. Kasane Teto - I\'m No Scientist',
        'Alohaii ft. vally.exe - Luxury',
        'Alohaii ft. Nia Suzune - Magazines',
        'Alohaii ft. girl_dm_ - Souvenir',
        'Yowane ft. Kasane Teto - Blue Shift'
    )
)

BASE_TAGS = '''        <!-- fullName -->
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/internalName/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/internalName/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/internalName/chart.js"></script>
        <script type>
          AUDIO_STRINGS["internalName"] = internalName_audio;
          THUMBNAIL_STRINGS["internalName"] = internalName_thumbnail;
          CHART_STRINGS.push(internalName_chart);
        </script>
'''

remove_punctuation = str.maketrans('', '', punctuation)

def to_camel_case(s):
    return ''.join(t.title() for t in s.split())

tag_sets = []

for song_block in SONGS:
    tag_sets.append('      <div>')
    for song_name in song_block:
        parsed_name = song_name.replace(' & ', ' ')
        artist_name = ''
        if 'ft' in parsed_name:
            artist_name = parsed_name.split('ft')[0].strip()
        else:
            artist_name = parsed_name.split('-')[0].strip()
        
        track_name = parsed_name[parsed_name.find('-'):].strip()
    
        artist_name = artist_name.translate(remove_punctuation).lower()
        track_name = track_name.translate(remove_punctuation).lower()
    
        internal_name = f'{to_camel_case(artist_name)}{to_camel_case(track_name)}'
        internal_name = internal_name[0].lower() + internal_name[1:]
    
        print(f'{song_name}, {internal_name}')
    
        tag_sets.append(BASE_TAGS.replace('internalName', internal_name)
                                 .replace('fullName', song_name))
    tag_sets[-1] = tag_sets[-1][:-1] # strip off the trailing newline
    tag_sets.append('      </div>\n\n')

output = ('\n'.join(tag_sets)).strip()
# print(output)

if clip != None:
    clip.copy(output)