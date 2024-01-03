# TidPit

## Table of Contents:
* [Quick Start](https://github.com/Drinkingpants74/TidPit/tree/main#quick-start)
* [What Is TidPit](https://github.com/Drinkingpants74/TidPit/tree/main#what-is-tidpit)
* [What Can It Do](https://github.com/Drinkingpants74/TidPit/tree/main#what-can-it-do)
* [Upcoming Modules](https://github.com/Drinkingpants74/TidPit/tree/main#upcoming-modules)
* [LongShot Modules](https://github.com/Drinkingpants74/TidPit/tree/main#longshot-modules)
* [Can I Create My Own Modules](https://github.com/Drinkingpants74/TidPit/tree/main#can-i-create-my-own-module)
* [Upcoming Features/Changes](https://github.com/Drinkingpants74/TidPit/tree/main#upcoming-featureschanges)
* [Installation Instructions](https://github.com/Drinkingpants74/TidPit/tree/main#install)


## Quick Start:
```
pip install gnews
```
```
python3 setup(GUI).py
```
__OR__
```
python3 setup(TUI).py
```
_THEN_
```
python3 output.py
```

## What Is TidPit:
TidPit is a Python Project that uses TKInter to create a rotating display of information.


## What Can It Do?
Currently, TidPit only has 2 Modules available:
1. Clock
2. News

More Modules will be added as time goes on.

## Upcoming Modules:
In No Particular Order:
* Weather
* Photo Scroller/Viewer
* Inspirational Quotes

## LongShot Modules:
* Sports Scores

## Can I Create My Own Module?
Yep. The best part about TidPit is that it's scalable. To create a new module, follow the Instructions
inside the "Template Instructions" file in the "template" foldder.

If you do make a new Module, share it with the class! I'd love to see what you can make, and if it's stable enough,
(and with permission), I'll add it as an official option.

## Upcoming Features/Changes:
* Customization Options
    * Clock:
        * Time Format
        * Text Color
        * Background Color
    * News:
        * Source Exclusions/Selection
        * Topic Exclusions/Selection
        * Text Color
        * Background Color
* More Modules [See Above](https://github.com/Drinkingpants74/TidPit/tree/main#upcoming-modules)


## Install:
Some modules have dependency requirements. They are:

Clock: None

News: [GNews](https://github.com/ranahaani/GNews)
```
pip install gnews
```

After the Dependencies are installed, simply run _setup(GUI).py_ or _setup(TUI).py_.
* GUI - Graphical Interface Setup
* TUI - Terminal Interface Setup
```
python3 setup(GUI).py
```
__OR__
```
python3 setup(TUI).py
```
Then Run the Generated File:
```
python3 output.py
```
