# CUESHEET-PARSER
- Parse cuesheet to python dict object or save as json. Fill in track title and other information with given text in specific form.
- For use when buying a new CD but no info is in any database.

## Usage
~~~
1. Install Python
2. Python3 FillInfoToCUE.py -h for help
3. Works well under WSL2
~~~
## Format
- A Cue file with basic format is required, which can by generated by EAC or something alike.
- The content file should be available on some netshop, perhaps the one the CD is bought from, e.g. TANO*C Store.
- The content file should have a format like
~~~
'title' (some title) 
id (space or tab) performer - track name
other lines with such similar staff
...
~~~
- If the first line start with title it would be parsed as title.
- If there is any - in the track name it should not matter but if someone have a - in his/her name or their band name then the programme just f**k off and take anything after the first - as the track name
- Would provide some example and try to support some other format of content later (if I'm not too lazy to do), though I don't think there would be anyone other than myself using this script.
