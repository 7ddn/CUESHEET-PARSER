import os
import json
import chardet
from shlex import split


def split_cue_to_dict(splitted):
    temp = {}

    # First get everything other than track info
    for idx, line in enumerate(splitted):
        if 'FILE' in line:
            break
        items = split(line)
        content = f'\"{items[-1]}\"'
        title = ' '.join(items[:-1]) if len(items) > 2 else items[0]
        temp[title] = content


    file_info = ' '.join(split(splitted[idx])[1:]).rsplit(' ', 1)
    title = file_info[0].rsplit('.', 1)[0]
    audio_format = file_info[0].rsplit('.' ,1)[-1]
    audio_kind = file_info[-1]
    temp['FILE'] = {'title':title, 'format':audio_format, 'kind':audio_kind}
    idx += 1
    tracks = []
    while idx < len(splitted):
        # idx = id, idx+1 = title, idx+2 = performer, idx+3 = composer
        # idx+4 = start_time

        track = {}
        track['id'] = splitted[idx].strip()
        idx += 1
        for i in range(3):
            line = splitted[idx + i]
            items = split(line)
            value = f'{items[-1]}'
            title = ' '.join(items[:-1]) if len(items) > 2 else items[0]
            track[title] = value
        idx += 3
        # print(idx)
        if 'INDEX 00' in splitted[idx]:
            track['INDEX 00'] = split(splitted[idx])[-1]
            idx += 1
        track['INDEX 01'] = split(splitted[idx])[-1]
        idx += 1
        tracks.append(track)
    temp['tracks'] = tracks
    return temp


def parse(filepath=None, rawdata=None):
    if filepath is not None:
        rawdata = open(filepath, "rb").read()
    elif rawdata is None:
        raise Exception('No Data Given')

    encoding = chardet.detect(rawdata)['encoding']
    splitted = rawdata.decode(encoding).splitlines()
    if splitted[-1] == '':
        splitted = splitted[:-1]
    return split_cue_to_dict(splitted)

