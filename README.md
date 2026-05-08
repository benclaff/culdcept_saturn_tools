# culdcept_saturn_tools

Tools for Sega Saturn's game  "Culdcept" : translation and hacks.

## Repo content

It contains scripts to extract japanese text and reinject them after translation into the disc image of the Sega Saturn's game  "Culdcept".
It also contains preliminary elements to build a card editor.

Be aware that two disc versions are referenced by Redump.
All scripts should be applied to the following disc, which is **v1.04** : 
(Redump entry)[http://redump.org/disc/53088/]

My intial motivation was to translate this game that has an untranslated 4-player option.
I also wanted to explore how python deals with bytes manipulation.
For the latter the conclusion is that "it's ok" but not the most documented possibility.
I also had lots of fun using regexp based byte pattern fishing. 🤪

**I decided to interupt this project following the announcement of "Culdcept The First", part of Saturn Tribute series.**
Bbest regards to the company and developers that revived and translated this old game.

Still, I learned a lot about saturn hacking and in this repository you will find everything that I produced.
I also upload a few json files containing  low quality translations, just as a Proof-Of-Concept.

## Features

The scripts allow to perform the following tasks:

* Shift-JIS script extractions to json-formatted outputs, which includes :
  * Main scenario
  * Characters Taunts
  * Tutorials
  * Cards / items
  * Help script
  * Shrine effects
* Optionnal extraction of card statistics

* Translated text re-injection :
  * By parsing the edited json files, the script will look for translated text blocks and ignore untranslated fields.
  * It will patch the **CULDCEPT.DT0** file, that should previously be extracted from the game disc image (this file contains all texts).
  * There is some basic tests to verify that translation can fit into the limited number of bytes (see below for current limitations)

 * Necessary post-process :
   * Once patche, the **CULDCEPT.DT0_patched** file that will generate the scrip should be :
     * renamed **CULDCEPT.DTO**
     * reinjected into the disc image using Sega Saturn Patcher (confirmed working with version 1.9.7872.1316).


## What remained to be done / current limitations :

* Extraction of non shift-JIS texts is not yet implemented.
* Zero graphic hacks.
* No work on variable font width hacks.
* No work on menu and name entry screens.
* Card statistics can be extracted, but I did not write the lines necessary to reinject them after modification. But developping a card editor tool seems a relatively easy task.
* Offset tables re-computations
  * Currently, translation has to fit into a restrained number of bytes coming from the original translation. 
  * Allowing longer translated texts is possible, but will require to implement offset tables updates computations. That should be easy for main scenario, taunts and tutorials, as far as i can tell because these text blocks do not contain specific pointers to other elements. But the data structure is more complex for the help script (e.g menus), cards, etc... and table/pointers updates will require a deeper analysis before allowing text extensions.

Finally,it worse mentionning that this game has only 3 files on the disc !

    * the bin file contains librairies and code, as well as the Fonts (the very last bytes).
    * the DT0 file contains texts, assets and other content data. A large proportion is sprites and tiles.
    * the DT1 file contains probably the videos and sound effects (not verified).

This makes difficult to shift bytes in DT0, because all offset tables from the file need to be updated? meaning that the whole file should be documented ?! (for instaed the very beginning has a table pointing to, as far as I can tell, subsections of assets (background tile, opponents texts and sprites interleaved...).

## Usage

Be aware that two disc versions are referenced by Redump. All scripts should be applied to the following disc, whichvis v1.04: 
(Redump entry)[http://redump.org/disc/53088/]

I did not test if the offsets are still valid for the other version 2.0. Scripts may require some updates at least in terms of offsets.

1) From the disc image, extract the **CULDCEPT.DT0** file.

2) Update the variable `_DTO` in the `meta.py` file with the path to your extracted DT0 file.

3) run any of the following scripts to extract texts from the corresponding sections. An output directory named `translations` with one to many json files will be generated.
  * `scenario_extraction.py` (one json per scenario block)
  * `help_script_extraction.py` (one json per block)
  * `cards_extraction.py` (one json for all ; a bool variable also allows to extract card statistics to the json)
  * `tutorials_extraction.py` (one json for all)
  * `taunts_extraction.py` (one json per opponent)
  * `shrine effects.py` (one json for all)

4) in the json files, the only insteresting fields for trabslation are `text_original` (what was extracted) and `text_translated` (empty, add translation there). Do not modify the other fields, they will be used for patching.

5) The `ruler_helper` fields shows to you how many characters are available per line (`-` is a character, `|` is line return). Its only purpose is for helping in the algnement of translated text, using any basic text editor.

6) The repository contains a "dirty" translation for demonstration. It is limited to the start of the scenario, the taunts of the 1st opponent, some parts of the help script (press L button in any menu to display some help), and very very few cards.

7) After filling some of the `text_translated` fields, run the script `patcher.py`. It will detect all translated fields and inject the corresponding text. If a translated field generates too many bytes compared to what could be injected, it will highlight the corresponding field and request for a shorter text modification (and how much it should be reduced).

## Documentation

The headers of all `*_extraction.py` files will describe how the tex is encoded and the corresponding byte-level structures.

They also describes how offset tables and pointers are working.
This can differ a lot from one type of object to the other (scenario, taunts, cards...), explaining my **by type of text** targeted approach.

I also started a tutorial in segaxtreme forum, hoping it will serve newcomers into the task of translation: https://segaxtreme.net/threads/translating-culdcept-tutorials-notes-whatever.25559/

## Acknowlegments 

Big thanks to the Segaxtreme community and its Discord members for advices.
Thanks to Malenko for his inspiring tutorials.
Thanks to KnightOfDragon for Sega Saturn Patcher.


