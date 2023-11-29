import argparse
import Modules.ParseContent as pc
import Modules.CUEBuilder as cb
import Modules.ParseCUE as pCue
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('cue_dir', help = 'path of cue to fill')
parser.add_argument('con_dir', help = 'path of content to fill')
parser.add_argument('--save_name', help = 'optional, name of saved cue, default is performer - album title')
parser.add_argument('--save_dir', help = 'optional, default same as directory of given cue')

args = parser.parse_args()
if args.save_dir is None:
    args.save_dir = Path(args.cue_dir).parent.absolute()

parsed_cue = pCue.parse(args.cue_dir)
content = pc.parse(args.con_dir)
filled = cb.fill_content_to_parsed_cue(content, parsed_cue)
cb.save_parsed_cue_to_cue_sheet(filled, args.save_name, args.save_dir)