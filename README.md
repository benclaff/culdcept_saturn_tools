# culdcept_saturn_tools

Tools for Sega Saturn's game  "Culcept" : translation and hacks.

## Repo content

It contains scripts to extract japanase text from the following disc: 
(Redump entry)[http://redump.org/disc/53088/]

I decided to interuot this project when "Culdcept The First" was annouced for the Saturn Tribute series. Cheers to the company and developers that revive and translate these old games.

I still learned a lot about saturn hacking and here you will find scripts and notes that I produced.

Be aware that two disc versions are referenced by Redump. I did not test if the offsets are similar in the other version and if scripts would require some updates.

## Features

The scripts allow to run the following tasks:

* Shift-JIS script extractions as json-editable   outputs
  * Main scenario
  * Characters Taunts
  * Tutorials
  * Cards / items
  * Help script
  * 

* Translated text injection
  * Patching of the DT0 file (that contains all texts).
  * Uses translations written in the json files 
  * A patch can then be build by reinjecting this file in the disc image using Sega Saturn Patcher (confirmed working with version x.xx).


## What remained to be done:

* Extraction of non-shiftJIS texts
* Variable font width hacks
* Offset tables updates
  * to allow longer translated texts (in terms of char lengths)

## Acknowlegments 

Big thanks to the Segaxtreme community and Discord for punctual advices. Many thanks to Malenko for his inspiring tutorials.


