# culdcept_saturn_tools

Tools for Sega Saturn's game  "Culcept" : translation and hacks.

## Repo content

It contains scripts to extract japanase text from the following disc: 
(Redump entry)[http://redump.org/disc/53088/]

I decided to interuot this project when "Culdcept The First" was announced for the Saturn Tribute series. Cheers to the company and developers that revive and translate these old games.

Still, I learned a lot about saturn hacking and here you will find scripts and notes that I produced. My intial motivation was to translate this 4-player game, and I also wanted to explore how python deals with bytes manipulation. For the latter the conclusion is that "it's ok". I also had fun using regexp-based bytes patterns fishing. 🤪

Be aware that two disc versions are referenced in by Redump. Current repo is valid for v1.04. I did not test if the offsets are similar in the other version 2.0. Scripts may require some updates at least in terms of offsets.

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

1) Update the variable `_DTO` in `meta.py` file with the absolute path to your DTO file extracted from the disc image.

2) run any of the following scripts to extract text from the corresponding section, a directory with one to many json files will be generated
  * scenario_extraction.py
  * help_script_extraction.py
  *

3) the most insteresting fields are `text_original` (what was extracted) and `text_translated` (empty, add translation there). The `helper` fields shows to you how many characters arz available per line (`-` is a character, `|` is line return). It is there just for helping in json edition using any basic text editor.

4) edit these fields throughout the files. The repository contains a "dirty" translation for demonstration. It is limites to the 1st minutes of the scenario, the taunts of the 1st opponent, some parts of the tutorial, very few cards.

5) After filling fields `text_translated`, run the `patcher.py`. It will detect all translated fields and inject the corresponding text. If a translated field generates to too many bytes compared to what could be injected, it will highlight the corresponding field and request for a shorter text modification (and indicate how much should be reduced).

## Documentation

The headers of all `*_extraction.py` files will describe how are encoded the text data and corresponding structures. It also describes how offset tables and pointers are working . They can differ a lot from one type of object to the other (scenario, taunts, cards...), explaining this targeted approach.

I also started a tutorial here, hoping it will serve newcomers into the task of translation: https://segaxtreme.net/threads/translating-culdcept-tutorials-notes-whatever.25559/

## Acknowlegments 

Big thanks to the Segaxtreme community and its Discord members for advices. Many thanks to Malenko for his inspiring tutorials.


