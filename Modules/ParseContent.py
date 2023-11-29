import chardet
import re


def parse(filepath=None, rawdata=None, composer_first = True):
    if filepath is not None:
        rawdata = open(filepath, "rb").read()
    elif rawdata is None:
        raise Exception('No Data Given')

    encoding = chardet.detect(rawdata)['encoding']
    splitted = rawdata.decode(encoding).splitlines()
    if splitted[-1] == '':
        splitted = splitted[:-1]
    content = {}
    if splitted[0].split(' ', 1)[0].lower() == 'title':
        content['TITLE'] = splitted[0].split(' ', 1)[-1]
        splitted = splitted[1:]
    tracks = []
    for track_info in splitted:
        track_info = re.split('[ \t]', track_info, maxsplit = 1)[-1]
        infos = track_info.split('-')
        track = {'PERFORMER': infos[0] if composer_first else infos[1],
                 'TITLE': infos[1] if composer_first else infos[0]}
        tracks.append(track)
    content['tracks'] = tracks
    return content