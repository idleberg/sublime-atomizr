# Atomizr for Sublime Text

[![The MIT License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square)](http://opensource.org/licenses/MIT)
[![Package Control](https://packagecontrol.herokuapp.com/downloads/Atomizr.svg?style=flat-square)](https://packagecontrol.io/packages/Atomizr)
[![GitHub release](https://img.shields.io/github/release/idleberg/sublime-atomizr.svg?style=flat-square)](https://github.com/idleberg/sublime-atomizr/releases)
[![Travis](https://img.shields.io/travis/idleberg/sublime-atomizr.svg?style=flat-square)](https://travis-ci.org/idleberg/sublime-atomizr)

Convert Sublime Text completions into Atom (or Visual Studio Code) snippets, and vice versa.

Also available for [Atom](https://github.com/idleberg/atom-atomizr) and the [command line](https://github.com/idleberg/ruby-atomizr) (see the [comparison chart](https://gist.github.com/idleberg/db6833ee026d2cd7c043bba36733b701)).

## Installation

### Package Control

1. Make sure you already have [Package Control](https://packagecontrol.io/) installed
2. Choose *“Install Package”* from the Command Palette (<kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>p</kbd>)
3. Type *“Atomizr”* and press <kbd>Enter</kbd>
4. Repeat steps 2 and 3 to install *“Better CoffeeScript”*

With [auto_upgrade](http://wbond.net/sublime_packages/package_control/settings/) enabled, Package Control will keep all installed packages up-to-date!

### Manual installation

Since [package dependencies](https://packagecontrol.io/docs/dependencies) are handled by Package Control, manual installation is not advised! If you still want to install from source, you probably know what you are doing so we won’t cover that here.

## Usage

The [Command Palette](http://docs.sublimetext.info/en/latest/reference/command_palette.html) currently offers the following commands, each prefixed with “Atomizr”:

* Automatic conversion¹
* Convert Atom to Sublime Text
* Convert Atom to Visual Studio Code
* Convert Sublime Text to Atom
* Convert Sublime Text to Visual Studio Code
* Convert Visual Studio Code to Atom
* Convert Visual Studio Code to Sublime Text
* Toggle Atom format (CSON⟷JSON)
* Toggle Sublime Text format (XML⟷JSON)

¹⁾ converts Atom and Sublime Text only

**Note:** Since automatic conversion is based on scope, make sure the a supported CoffeeScript package is installed as well. Using [Better CoffeeScript](https://packagecontrol.io/packages/Better%20CoffeeScript) is recommended, though [CoffeeScript](https://packagecontrol.io/packages/CoffeeScript), [IcedCoffeeScript](https://packagecontrol.io/packages/IcedCoffeeScript) and [Mongoose CoffeeScript](https://packagecontrol.io/packages/Mongoose%20CoffeeScript) are also supported.

### Keyboard Shortcuts

*The following examples use the macOS shortcuts, for Linux or Windows use <kbd>Ctrl</kbd>+<kbd>Alt</kbd> as modifier rather than <kbd>Ctrl</kbd>*

Memorizing the keyboard shortcuts for conversion is easy. Just think of the <kbd>A</kbd> key for Atom, the <kbd>S</kbd> key for Sublime Text and the <kbd>V</kbd> key for Visual Studio Code:

Action                             | Mnemonic | Shortcut
-----------------------------------|----------|-----------------------------------------------------------
Atom to Sublime Text               | “A to S” | <kbd>Ctrl</kbd>+<kbd>A</kbd>, <kbd>Ctrl</kbd>+<kbd>S</kbd>
Atom to Visual Studio Code         | “A to V” | <kbd>Ctrl</kbd>+<kbd>A</kbd>, <kbd>Ctrl</kbd>+<kbd>V</kbd>
Sublime Text to Atom               | “S to A” | <kbd>Ctrl</kbd>+<kbd>S</kbd>, <kbd>Ctrl</kbd>+<kbd>A</kbd>
Sublime Text to Visual Studio Code | “S to V” | <kbd>Ctrl</kbd>+<kbd>S</kbd>, <kbd>Ctrl</kbd>+<kbd>V</kbd>
Visual Studio Code to Atom         | “V to A” | <kbd>Ctrl</kbd>+<kbd>V</kbd>, <kbd>Ctrl</kbd>+<kbd>A</kbd>
Visual Studio Code to Sublime Text | “V to S” | <kbd>Ctrl</kbd>+<kbd>V</kbd>, <kbd>Ctrl</kbd>+<kbd>S</kbd>
Atom to Atom                       | “A to A” | <kbd>Ctrl</kbd>+<kbd>A</kbd>, <kbd>Ctrl</kbd>+<kbd>A</kbd>
Sublime Text to Sublime Text       | “S to S” | <kbd>Ctrl</kbd>+<kbd>S</kbd>, <kbd>Ctrl</kbd>+<kbd>S</kbd>

For automatic conversion, press <kbd>Ctrl</kbd>+<kbd>C</kbd> twice.

### Settings

Some of the default conversion settings can be modified from the *Package Settings* menu:

* Rename target files (`boolean`)
* Add or remove trailing tab-stops (`boolean`)
* Indentation level (`int`)
* Sort keys (`boolean`)
* Scope replacement rules (`array`)

# License

This work is licensed under the [The MIT License](LICENSE).

## Donate

You are welcome support this project using [Flattr](https://flattr.com/submit/auto?user_id=idleberg&url=https://github.com/idleberg/sublime-atomizr) or Bitcoin `17CXJuPsmhuTzFV2k4RKYwpEHVjskJktRd`
