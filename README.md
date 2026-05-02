# culdcept_saturn_tools

Tools for Sega Saturn's game  "Culdcept" : translation and hacks.

## Repo content

It contains scripts to extract japanese text and reinject it after translation. It also contains elements to start a card editor.

I decided to interupt this project following the announcement of "Culdcept The First", part of Saturn Tribute series. Cheers and thanksto the company and developers that revived and translated these old games.

Still, I learned a lot about saturn hacking and here you will find scripts and notes that I produced.

My intial motivation was to translate this 4-player game, and I also wanted to explore how python deals with bytes manipulation. For the latter the conclusion is that "it's ok" but not the most documented possibility. I also had lots of fun using regexp based byte pattern fishing. 🤪

## Features

The scripts allow to run the following tasks:

* Shift-JIS script extractions as json   outputs
  * Main scenario
  * Characters Taunts
  * Tutorials
  * Cards / items
  * Help script
  * Shrine effects
* Optionnal extraction of card statistics

* Translated text injection :
  * Will parse json files for translated fields and ignore untranslated fields.
  * Patches the "DT0" file previously extracted from the disc image (it contains all texts).
  * Makes basic tests to verify that translation can fit (in terms of required bytes, see below for current limitations)
  * Then a patch can be built by reinjecting this file into the disc image using Sega Saturn Patcher (confirmed working with version x.xx).


## What remained to be done / current limitations :

* Extraction of non-shiftJIS texts is not yet implemented.
* Zero graphic hacks
* No work on variable font width hacks
* Card statistics can be extracted, but I did not write the lines necessary to reinject them after modification. Be aware that developping a card editor tool seems a relatively easy task.
* Offset tables re-computations
  * currently, translation has to fit into a restrained number of bytes (the inital japanese translation). Allowing longer translated texts will require the addition of updated offset tables computations. That should be easy for main scenario, taunts and tutorials. As far as i can tell, these text blocks do not contain specific pointers to other elements. But the data structure is more complex for the tutorials, cards, etc... and table updtes will require a deeper analysis before updating them.

## Usage

Be aware that two disc versions are referenced by Redump. All scripts should be applied to the following disc, whichvis v1.04: 
(Redump entry)[http://redump.org/disc/53088/]

I did not test if the offsets are still valid for the other version 2.0. Scripts may require some updates at least in terms of offsets.

1) From the disc image, extract the DT0 file.

2) Update the variable `_DTO` in the `meta.py` file with the path to your extracted DT0 file.

3) run any of the following scripts to extract texts from the corresponding section, an output directory with one to many json files will be generated.
  * `scenario_extraction.py` (one json per scenario block)
  * `help_script_extraction.py` (one json for all)
  * `cards_extraction.py` (one json for all ; a bool variable also allows to extract card statistics to the json)
  * `tutorials_extraction.py` (one json for all)
  * `taunts_extraction.py` (one json per opponent)
  * `shrine effects.py` (one json for all)

4) in the json files, the only insteresting fields for trabslation are `text_original` (what was extracted) and `text_translated` (empty, add translation there). Do not modify the other fields, they will be used for patching.

5) The `ruler_helper` fields shows to you how many characters are available per line (`-` is a character, `|` is line return). Its only purpose is for helping in the algnement of translated text, using any basic text editor.

6) The repository contains a "dirty" translation for demonstration. It is limited to the start of the scenario, the taunts of the 1st opponent, some parts of the tutorial, and very few cards.

7) After filling some field `text_translated`, run the script `patcher.py`. It will detect all translated fields and inject the corresponding text. If a translated field generates too many bytes compared to what could be injected, it will highlight the corresponding field and request for a shorter text modification (and how much it should be reduced).

## Documentation

The headers of all `*_extraction.py` files will describe how is encoded the text data and the corresponding byte-level structures.

It also describes how offset tables and pointers are working . They can differ a lot from one type of object to the other (scenario, taunts, cards...), explaining this targeted approach.

I also started a tutorial in segaxtreme forum, hoping it will serve newcomers into the task of translation: https://segaxtreme.net/threads/translating-culdcept-tutorials-notes-whatever.25559/

## Acknowlegments 

Big thanks to the Segaxtreme community and its Discord members for advices. Thanks to Malenko for his inspiring tutorials.


