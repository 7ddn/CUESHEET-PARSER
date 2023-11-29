from pathlib import PosixPath
import os
import re
def fill_content_to_parsed_cue(content, parsed_cue):
    # Content should have format of title-composer pairs, optionally with disk title
    # The number of pairs should match number of items in parsed_cue
    if not 'tracks' in content:
        raise Exception('No Information is Given')
    if len(content['tracks']) != len(parsed_cue['tracks']):
        raise Exception('Number of given information do not match given cue')
    if 'TITLE' in content:
        parsed_cue['TITLE'] = content['TITLE']
    existing_composer = set()
    for track_info, track in zip(content['tracks'], parsed_cue['tracks']):
        track['TITLE'] = track_info['TITLE']
        track['PERFORMER'] = track_info['PERFORMER']
        existing_composer.add(track_info['PERFORMER'])
    if len(existing_composer) == 1:
        parsed_cue['PERFORMER'] = existing_composer.pop()
    else:
        parsed_cue['PERFORMER'] = 'Various Artists'

    return parsed_cue


def save_parsed_cue_to_cue_sheet(parsed_cue, filename = None, filedir:PosixPath = None, rename = False):
    if filename is None:
        if 'TITLE' in parsed_cue and 'PERFORMER' in parsed_cue:
            filename = f'{parsed_cue["PERFORMER"]} - {parsed_cue["TITLE"]}.cue'
        else:
            filename = 'filled.cue'
    if filedir is not None:
        filename = str(filedir.joinpath(filename))
    with open(filename, 'w') as f:
        for key in parsed_cue:
            if key != 'tracks' and key != 'FILE':
                f.write(f'{key} {parsed_cue[key]}\r\n')
        title = f'{parsed_cue["PERFORMER"]} - {parsed_cue["TITLE"]}'
        originTitle = parsed_cue["FILE"]["title"]
        originWavName = f'{originTitle}.{parsed_cue["FILE"]["format"]}'
        wavName = f'{title}.{parsed_cue["FILE"]["format"]}'
        if rename:
            os.rename(str(filedir.joinpath(originWavName)), str(filedir.joinpath(wavName)))
        f.write(f'FILE "{wavName}" {parsed_cue["FILE"]["kind"]}\r\n')
        for track in parsed_cue['tracks']:
            f.write(f'  {track["id"]}\r\n')
            for key in track:
                if key == 'id':
                    continue
                if re.match(r'[0-9][0-9]\:[0-5][0-9]\:[0-9][0-9]', track[key]):
                    f.write(f'    {key} {track[key]}\r\n')
                else:
                    f.write(f'    {key} "{track[key]}"\r\n')
        f.close()



