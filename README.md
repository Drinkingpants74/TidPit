# TidPit

## Table of Contents:
* [Releases Page](https://github.com/Drinkingpants74/TidPit/releases)
* [Quick Start](https://github.com/Drinkingpants74/TidPit/tree/main#quick-start)
* [What Is TidPit](https://github.com/Drinkingpants74/TidPit/tree/main#what-is-tidpit)
* [Available Modules](https://github.com/Drinkingpants74/TidPit/tree/main#available-modules)
* [Upcoming Modules](https://github.com/Drinkingpants74/TidPit/tree/main#upcoming-modules)
* [LongShot Modules](https://github.com/Drinkingpants74/TidPit/tree/main#longshot-modules)
* [Can I Create My Own Modules](https://github.com/Drinkingpants74/TidPit/tree/main#can-i-create-my-own-module)
* [Upcoming Features/Changes](https://github.com/Drinkingpants74/TidPit/tree/main#upcoming-featureschanges)
* [Installation Instructions](https://github.com/Drinkingpants74/TidPit/tree/main#install)


## Quick Start:
Download a [release from here](https://github.com/Drinkingpants74/TidPit/releases).

_While it's Downloading, install the Dependencies:_
```
pip install gnews sportsdataverse requests pillow
```
_Then Run:_
```
python3 setup.py
```
_Then Run:_
```
python3 output.py
```

## What Is TidPit:
TidPit is a Python Project that uses TKInter to create a rotating display of information.
It's _designed_ to be run on a Raspberry Pi, but it _can_ run on anything that supports Python.


## Available Modules:
1. Clock
2. News
3. Sports (NFL, NBA, CFB, CBB)

More Modules will be added as time goes on.

## Upcoming Modules:
In No Particular Order:
* Photo Scroller/Viewer
* Inspirational Quotes

## LongShot Modules:
* Weather

## Can I Create My Own Module?
Yep. The best part about TidPit is that it's scalable. To create a new module, follow the Instructions
in both the _Template Instructions_ and _template.py_ files, inside the "templates" folder.

Also, if you do make a new Module share it with the class! I'd love to see what you can make, and if it's stable enough,
(and with permission), I'll add it as an official option.

## Upcoming Features/Changes:
* Customization Options:
  * News:
    * Topic Exclusions/Selection
    * Text Color
    * Background Color
  * Sports:
    * Background Color
    * Text Color
* More Modules [See Above](https://github.com/Drinkingpants74/TidPit/tree/main#upcoming-modules)


## Install:
Some modules have dependency requirements. You do not need every dependency, just the ones
necessary for the Modules you want to use.

### Dependencies:
Clock:
* None

News:
* [GNews](https://github.com/ranahaani/GNews)
```
pip install gnews
```

Sports:
* [Sports Dataverse](https://github.com/sportsdataverse/sportsdataverse-py)
* Requests
* Pillow
```
pip install sportsdataverse requests pillow
```

### Setup:
After the Dependencies are installed, simply run _setup.py_.
```
python3 setup.py
```
This will Display an Interface where you can Customize your displays
and choose which Modules you want to use.

Then Run the Generated File:
```
python3 output.py
```
