'''
Python script to convert compiled Javascript into a copy-pasteable file for Khan Academy.
'''
from pathlib import Path
import re

OUTFILE_PATH = 'ka_build.html'
JS_FOLDER = './js_build/src'
# files in load order
LOAD_ORDER = [
    'audio/audio-player',
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
    <!-- song loading -->
    <script>
      var AUDIO_STRINGS = {};
      var THUMBNAIL_STRINGS = {};
      var CHART_STRINGS = [];
    </script>
    <!--
      Chart import format because I'll definitely forget (and I also think it's cool).

      To load the files, add these 3 script tags:
      <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/[song name]/audio.js"></script>
      <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/[song name]/thumbnail.js"></script>
      <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/[song name]/chart.js"></script>

      The song name is formatted as "[artist name][song name]" with no punctuation and in camel
      case. If the artist name includes "ft. x", don't include that part; if the artist is
      "[name 1] & [name 2]", use "[name 1][name 2]". For example, the song name for Eastside (by
      Good Kid) is "goodKidEastside".

      After the file loading script tags, add this script tag to add them to the lookup tables:
      <script type>
        AUDIO_STRINGS["[song name]"] = [song name]_audio;
        THUMBNAIL_STRINGS["[song name]"] = [song name]_thumbnail;
        CHART_STRINGS.push([song name]_chart);
      </script>

      NOTE: For 炜WARD ROMANCE, the song name uses the romanization of the Chinese character, so the
      song name is "flavorFoleyWeiwardRomance".
    -->

    <!--
      Div tag here so I can collapse all of these. If a song is commented out, it means that it's in
      my "maybe I should add this" playlist but hasn't been charted yet (this *does not* mean it's
      guaranteed to be charted eventually).

      GUARDIANS: All the copyright-related info is included here. I think all of these songs are
      safe, but contact me if you disagree and we'll work something out. Songs are listed in order
      of how sure I am that they're OK. Keep in mind that:
      - This is about as non-commercial as you can possibly get.
      - The only way to get the music data would be to go OFF of Khan Academy and download the files
        from my personal Github (so I'd say it's my problem if copyright becomes an issue).
    -->
    <div>
      <!--
        Mortals, Firefly, Invincible, and Savannah were released under NoCopyrightSounds.
      -->
      <div>
        <!-- Warriyo ft. Laura Brehm - Mortals -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/warriyoMortals/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/warriyoMortals/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/warriyoMortals/chart.js"></script>
        <script type>
          AUDIO_STRINGS["warriyoMortals"] = warriyoMortals_audio;
          THUMBNAIL_STRINGS["warriyoMortals"] = warriyoMortals_thumbnail;
          CHART_STRINGS.push(warriyoMortals_chart);
        </script> -->

        <!-- Jim Yosef - Firefly -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/jimYosefFirefly/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/jimYosefFirefly/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/jimYosefFirefly/chart.js"></script>
        <script type>
          AUDIO_STRINGS["jimYosefFirefly"] = jimYosefFirefly_audio;
          THUMBNAIL_STRINGS["jimYosefFirefly"] = jimYosefFirefly_thumbnail;
          CHART_STRINGS.push(jimYosefFirefly_chart);
        </script> -->

        <!-- DEAF KEV - Invincible -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/deafKevInvincible/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/deafKevInvincible/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/deafKevInvincible/chart.js"></script>
        <script type>
          AUDIO_STRINGS["deafKevInvincible"] = deafKevInvincible_audio;
          THUMBNAIL_STRINGS["deafKevInvincible"] = deafKevInvincible_thumbnail;
          CHART_STRINGS.push(deafKevInvincible_chart);
        </script> -->

        <!-- Diviners ft. Philly K - Savannah -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/divinersSavannah/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/divinersSavannah/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/divinersSavannah/chart.js"></script>
        <script type>
          AUDIO_STRINGS["divinersSavannah"] = divinersSavannah_audio;
          THUMBNAIL_STRINGS["divinersSavannah"] = divinersSavannah_thumbnail;
          CHART_STRINGS.push(divinersSavannah_chart);
        </script> -->
      </div>

      <!--
        From ROMA's YouTube channel description:
        ALL MY MUSIC IS 100% COPYRIGHT FREEEEEE DO WHATEVER YOU WANT, MAKE MONEY OFF OF IT GO BALLS 
        just dont claim my work as yours please c: 
        Lalala
      -->
      <div>
        <!-- ROMA - NEURODIVERGENCE -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/romaNeurodivergence/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/romaNeurodivergence/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/romaNeurodivergence/chart.js"></script>
        <script type>
          AUDIO_STRINGS["romaNeurodivergence"] = romaNeurodivergence_audio;
          THUMBNAIL_STRINGS["romaNeurodivergence"] = romaNeurodivergence_thumbnail;
          CHART_STRINGS.push(romaNeurodivergence_chart);
        </script> -->

        <!-- ROMA ft. Kasane Teto - DANCIN VIBES -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/romaDancinVibes/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/romaDancinVibes/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/romaDancinVibes/chart.js"></script>
        <script type>
          AUDIO_STRINGS["romaDancinVibes"] = romaDancinVibes_audio;
          THUMBNAIL_STRINGS["romaDancinVibes"] = romaDancinVibes_thumbnail;
          CHART_STRINGS.push(romaDancinVibes_chart);
        </script> -->
      </div>

      <!--
        Good Kid is Good Kid, they let anyone do anything (non-commercial) with their music as long
        as they're credited.
      -->
      <div>
        <!-- Good Kid - Coffee -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidCoffee/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidCoffee/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidCoffee/chart.js"></script>
        <script type>
          AUDIO_STRINGS["goodKidCoffee"] = goodKidCoffee_audio;
          THUMBNAIL_STRINGS["goodKidCoffee"] = goodKidCoffee_thumbnail;
          CHART_STRINGS.push(goodKidCoffee_chart);
        </script> -->

        <!-- Good Kid - Eastside -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidEastside/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidEastside/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidEastside/chart.js"></script>
        <script type>
          AUDIO_STRINGS["goodKidEastside"] = goodKidEastside_audio;
          THUMBNAIL_STRINGS["goodKidEastside"] = goodKidEastside_thumbnail;
          CHART_STRINGS.push(goodKidEastside_chart);
        </script> -->

        <!-- Good Kid - Tornado -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidTornado/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidTornado/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidTornado/chart.js"></script>
        <script type>
          AUDIO_STRINGS["goodKidTornado"] = goodKidTornado_audio;
          THUMBNAIL_STRINGS["goodKidTornado"] = goodKidTornado_thumbnail;
          CHART_STRINGS.push(goodKidTornado_chart);
        </script> -->

        <!-- Good Kid - From the Start -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidFromTheStart/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidFromTheStart/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/goodKidFromTheStart/chart.js"></script>
        <script type>
          AUDIO_STRINGS["goodKidFromTheStart"] = goodKidFromTheStart_audio;
          THUMBNAIL_STRINGS["goodKidFromTheStart"] = goodKidTFromTheStartthumbnail;
          CHART_STRINGS.push(goodKidFromTheStart_chart);
        </script> -->

        <!-- Good Kid - NoTimeToExplain -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/noTimeToExplain/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/noTimeToExplain/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/noTimeToExplain/chart.js"></script>
        <script type>
          AUDIO_STRINGS["noTimeToExplain"] = noTimeToExplain_audio;
          THUMBNAIL_STRINGS["noTimeToExplain"] = noTimeToExplain_thumbnail;
          CHART_STRINGS.push(noTimeToExplain_chart);
        </script> -->
      </div>

      <!--
        Quote from Meganeko: "For non-commercial, fan-made custom levels in games, it's okay to use
        my independent solo releases, with proper credit."

        I guess this technically isn't "fan-made" because I'm the one making the game, but I still
        think it's reasonable because I'm not using their music to do any marketing or things like
        that.
      -->
      <div>
        <!-- Meganeko - nano love -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/meganekoNanoLove/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/meganekoNanoLove/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/meganekoNanoLove/chart.js"></script>
        <script type>
          AUDIO_STRINGS["meganekoNanoLove"] = meganekoNanoLove_audio;
          THUMBNAIL_STRINGS["meganekoNanoLove"] = meganekoNanoLove_thumbnail;
          CHART_STRINGS.push(meganekoNanoLove_chart);
        </script> -->
      </div>

      <!--
        FLAVOR FOLEY, Isidore., MonochroMenace, rai1367, Hobisu, Alohaii, and Yowane haven't made
        blanket statements about rhythm games, but are all on the custom chart whitelist for
        UNBEATABLE (another rhythm game). This means that they've given permission for their music
        to be used in charts for a commercial release, so I think it's also reasonable to assume
        they'd be fine with using it here (also, most of them have said that any non-commercial use
        is fine, not just for UNBEATABLE charts).

        Extra notes:
        - If Hobisu and Yowane still aren't on the whitelist, it's because the whitelist hasn't been
          updated in who knows how many months at this point. I'm the one who contacted them and I'm
          more than willing to show you their responses.
        - The features on Alohaii's music (vally.exe, Nia Suzune, and girl_dm_) technically aren't
          whitelisted, but Alohaii stated that they are the only one who owns the rights to the
          music.
        - All other features are vocaloids and the whitelist obviously doesn't apply to them.
        - For what it's worth, UNBEATABLE charts (some made by me, some made by other people) using
          all of these songs have been released and none were taken down (and the UNBEATABLE team is
          *very* strict about the whitelist).
      -->
      <div>
        <!-- FLAVOR FOLEY ft. Feng Yi - 炜WARD ROMANCE -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyWeiwardRomance/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyWeiwardRomance/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyWeiwardRomance/chart.js"></script>
        <script type>
          AUDIO_STRINGS["flavorFoleyWeiwardRomance"] = flavorFoleyWeiwardRomance_audio;
          THUMBNAIL_STRINGS["flavorFoleyWeiwardRomance"] = flavorFoleyWeiwardRomance_thumbnail;
          CHART_STRINGS.push(flavorFoleyWeiwardRomance_chart);
        </script> -->

        <!-- FLAVOR FOLEY ft. Chis-A - Clover -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyClover/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyClover/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyClover/chart.js"></script>
        <script type>
          AUDIO_STRINGS["flavorFoleyClover"] = flavorFoleyAClover_audio;
          THUMBNAIL_STRINGS["flavorFoleyClover"] = flavorFoleyAClover_thumbnail;
          CHART_STRINGS.push(flavorFoleyAClover_chart);
        </script> -->

        <!-- FLAVOR FOLEY ft. SF-A2 Miki - Human -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyA2MikiHuman/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyA2MikiHuman/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyA2MikiHuman/chart.js"></script>
        <script type>
          AUDIO_STRINGS["flavorFoleyA2MikiHuman"] = flavorFoleyA2MikiHuman_audio;
          THUMBNAIL_STRINGS["flavorFoleyA2MikiHuman"] = flavorFoleyA2MikiHuman_thumbnail;
          CHART_STRINGS.push(flavorFoleyA2MikiHuman_chart);
        </script> -->

        <!-- FLAVOR FOLEY ft. Eleanor Forte - weathergirl -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyWeathergirl/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyWeathergirl/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/flavorFoleyWeathergirl/chart.js"></script>
        <script type>
          AUDIO_STRINGS["flavorFoleyWeathergirl"] = flavorFoleyWeathergirl_audio;
          THUMBNAIL_STRINGS["flavorFoleyWeathergirl"] = flavorFoleyWeathergirl_thumbnail;
          CHART_STRINGS.push(flavorFoleyWeathergirl_chart);
        </script> -->

        <!-- Isidore. & Monochro Menace ft. Megurine Luka - FEEDBACK -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/isidoreMonochroMenaceFeedback/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/isidoreMonochroMenaceFeedback/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/isidoreMonochroMenaceFeedback/chart.js"></script>
        <script type>
          AUDIO_STRINGS["isidoreMonochroMenaceFeedback"] = isidoreMonochroMenaceFeedback_audio;
          THUMBNAIL_STRINGS["isidoreMonochroMenaceFeedback"] = isidoreMonochroMenaceFeedback_thumbnail;
          CHART_STRINGS.push(isidoreMonochroMenaceFeedback_chart);
        </script> -->

        <!-- rai1367 - Rockabye -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/rai1367Rockabye/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/rai1367Rockabye/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/rai1367Rockabye/chart.js"></script>
        <script type>
          AUDIO_STRINGS["rai1367Rockabye"] = rai1367Rockabye_audio;
          THUMBNAIL_STRINGS["rai1367Rockabye"] = rai1367Rockabye_thumbnail;
          CHART_STRINGS.push(rai1367Rockabye_chart);
        </script> -->

        <!-- Hobisu ft. Kasane Teto - I'm No Scientist -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/hobisuImNoScientist/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/hobisuImNoScientist/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/hobisuImNoScientist/chart.js"></script>
        <script type>
          AUDIO_STRINGS["hobisuImNoScientist"] = hobisuImNoScientist_audio;
          THUMBNAIL_STRINGS["hobisuImNoScientist"] = hobisuImNoScientist_thumbnail;
          CHART_STRINGS.push(hobisuImNoScientist_chart);
        </script> -->

        <!-- Alohaii ft. vally.exe - Luxury -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiLuxury/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiLuxury/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiLuxury/chart.js"></script>
        <script type>
          AUDIO_STRINGS["alohaiiLuxury"] = alohaiiLuxury_audio;
          THUMBNAIL_STRINGS["alohaiiLuxury"] = alohaiiLuxury_thumbnail;
          CHART_STRINGS.push(alohaiiLuxury_chart);
        </script> -->

        <!-- Alohaii ft. Nia Suzune - Magazines -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiMagazines/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiMagazines/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiMagazines/chart.js"></script>
        <script type>
          AUDIO_STRINGS["alohaiiMagazines"] = alohaiiMagazines_audio;
          THUMBNAIL_STRINGS["alohaiiMagazines"] = alohaiiMagazines_thumbnail;
          CHART_STRINGS.push(alohaiiMagazines_chart);
        </script> -->

        <!-- Alohaii ft. girl_dm_ - Souvenir -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiSouvenir/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiSouvenir/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/alohaiiSouvenir/chart.js"></script>
        <script type>
          AUDIO_STRINGS["alohaiiSouvenir"] = alohaiiSouvenir_audio;
          THUMBNAIL_STRINGS["alohaiiSouvenir"] = alohaiiSouvenir_thumbnail;
          CHART_STRINGS.push(alohaiiSouvenir_chart);
        </script> -->

        <!-- Yowane ft. Kasane Teto - Blue Shift -->
        <!-- <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/yowaneBlueShift/audio.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/yowaneBlueShift/thumbnail.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/JustASideQuestNPC/ka-rhythm-game@main/yowaneBlueShift/chart.js"></script>
        <script type>
          AUDIO_STRINGS["yowaneBlueShift"] = yowaneBlueShift_audio;
          THUMBNAIL_STRINGS["yowaneBlueShift"] = yowaneBlueShift_thumbnail;
          CHART_STRINGS.push(yowaneBlueShift_chart);
        </script> -->
      </div>
    </div>
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