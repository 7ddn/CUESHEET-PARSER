"""
Generates a cue file based on a track list.
"""

__author__ = 'Kar Epker'
__copyright__ = '2016, karepker@gmail.com (Kar Epker)'

import datetime
import logging
import sys
import time

def parse_track_string(track):
    """Parses a track string and returns the name and time."""
    # Parse the relevant information out of the tracks.
    track = track.rstrip()
    track_info = track.split('\t')
    if len(track_info) < 4:
        raise ValueError(
                'Not enough fields for track {}, skipping.'.format(track))

    name = track_info[1]
    time_string = track_info[3]
    logger.debug('Got name %s and time %s.', name, time_string)

    # Read the time portion of the string
    total_seconds = 0
    split_time_string = time_string.split(':')
    if len(split_time_string) > 3:
        raise ValueError(
                'Skipping track {} with unparseable time.'.format(track))

    time_parts = ['0'] * (3 - len(split_time_string)) + split_time_string
    hours, minutes, seconds = time_parts
    try:
        total_seconds = (int(hours) * 60 * 60 + int(minutes) * 60 +
                          int(seconds))
    # Invalid time value
    except ValueError:
        raise ValueError(
            'Skipping track {} with unparseable time.'.format(track))

    logger.debug('Parsed %d seconds for track "%s".', total_seconds, track)

    return name, datetime.timedelta(seconds=total_seconds)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    start = datetime.timedelta(seconds=50)
    track_times = []
    names = []
    for track in sys.stdin:
        try:
            name, track_time = parse_track_string(track)
            names.append(name)
            track_times.append(track_time)
        except ValueError as v:
            logger.error(v)

    accumulated_time = start
    for track_index, name_and_track in enumerate(zip(names, track_times)):
        name, track = name_and_track
        minutes = int(accumulated_time.total_seconds() / 60)
        seconds = int(accumulated_time.total_seconds() % 60)
        print('  TRACK {:02} AUDIO'.format(track_index))
        print('    TITLE {}'.format(name))
        print('    INDEX 01 {:02d}:{:02d}:00'.format(minutes, seconds))
        accumulated_time += track
