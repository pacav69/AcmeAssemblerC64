# Sublime Acme Assembler (C64)
![GitHub package.json version](https://img.shields.io/github/package-json/v/pacav69/AcmeAssemblerC64)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/pacav69/AcmeAssemblerC64?include_prereleases)
![GitHub manifest version](https://img.shields.io/github/manifest-json/v/pacav69/AcmeAssemblerC64)

Sublime Package for C64/CX16 6502 assembly development using the Acme Assembler, contains language configuration/syntax coloring, build system and some snippets. Support for OSX, Windows and Linux.
Requires Sublime Text, version 3 is supported. 

The cx16 emulator is used for development.

Below is a quick start guide.

# Installation: OSX

* install sublime text

    brew cask install sublime-text

* requires [homebrew ](https://brew.sh/) installed

    brew install acme

* download and install [Commander X16 emulator](https://github.com/commanderx16/x16-emulator/releases)
extract the files
copy folder to Applications folder

* download this repo 
extract the files
copy AcmeAssemblerC64 folder to /Users/[username]/Library/Application Support/Sublime Text 3/Packages folder, replace [username] with login name.

# Installation: Windows

* download and install Commander X16 emulator 

* download this repo 
extract the files
copy AcmeAssemblerC64 folder to c:.../applications/Sublime Text 3/Packages folder.

# Installation: Linux

* download and install Commander X16 emulator 

* download this repo 
extract the files
copy AcmeAssemblerC64 folder to .../applications/Sublime Text 3/Packages folder.

# Develop, build and run

* Open a Acme Assembler code file in Sublime text. Example code file 

 * Press `F7` key to start Build and Run (see below for more build options)

* If you get error saying java is not recognized as an internal or external command, ensure java is installed and add the path to your java binaries folder to the PATH environment variable

# Details, Build System


Action&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Shortcut macOS | Shortcut Windows | Description
:--|:--|:--|:--
Other build variants (listed below) | `cmd+Shift+P` | `Ctrl+Shift+P` | Shows the list of the following variants
Build | `Command+Shift+P`  | `Control+Shift+P` | Compiles the __current__ file.
Build and Run | `F7` | `F7` | Compiles the __current file__ and runs it using the Vice emulator.
Build and Debug | `Shift+F7` | `Shift+F7` | Compiles the __current file__ and runs it using the Vice emulator. This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.
Build Startup | `Command+Shift+B` | `Ctrl+Shift+B` | Compiles __a file with name Startup.asm__ in the same folder as the current file. Handy if you have several code files included in a main runnable file. The filename can be configured via `Acme_startup_file_path` setting.
Build and Run Startup | `F5` | `F5` | Compiles __a file with name Startup.asm__ in the same folder as the current file, and runs it using the Vice emulator. Handy if you have several code files included in a main runnable file. The filename can be configured via `Acme_startup_file_path` setting.
Build and Debug Startup | `Shift+F5` | `Shift+F5` | Compiles __a file with name Startup.asm__ in the same folder as the current file, and runs it using the Vice emulator. Handy if you have several code files included in a main runnable file. __This option allows the creation of a file containing breakpoints, which is sent to the Vice emulator for debugging.__ The filename can be configured via `Acme_startup_file_path` setting.
Make | `F8` | `F8` | Invokes a script called `make.bat` for Windows, `make.sh` for macOS (configurable through the `default_make_path` setting).


The following (relevant?) environment variables will be available in the make script:

# Variable | Info
:--|:--
`Acme_file` | Filename of active file when command was triggered
`Acme_file_path` | Full path active file when command was triggered
`Acme_prg_file` | Full path for suggested prg file name, for active file when command was triggered
`Acme_bin_folder` | Path to current output folder (`bin` by default or specified by `Acme_output_path` setting)

"acme_emulator_run_path": "/Applications/x16emu_mac-r33/x16emu" | path to emulator


# Pre/post-build

There's a way to execute custom scripts before/after the build.

## Variable | Info
:--|:--
* `default_prebuild_path` | Full path to the `.bat` or `.sh` script file that will be executed __before__ the build.

* `default_postbuild_path` | Full path to the `.bat` or `.sh` script file that will be executed __after__ the build. Useful for file compression etc.


# AcmeTooltips

This plugin makes working with Acme Assembler easier by displaying various helpful tooltip information. Tooltips database can be extended to provide more c64 related info. So far rudimentary help files with Acme Assembler directives, illegal opcodes, VIC registers and SID registers are ready. This plugin was added by Roman Dobosz (Gryf/Elysium) and Krzysztof Dabrowski (Brush/Elysium)

# Other documentation
Navigate to Preferences/Package Settings/AcmeAssemblerC64 and select the 

* Acme Quick Ref - this is a quick reference text on Acme Assembler.

* 65C02 Opcodes.html - right click and slect open in browser.

# Configuration

Navigate to Preferences/Package Settings/AcmeAssemblerC64 and select the configuration file to edit. Currently you can configure:

	"css_file": "AcmeAssemblerC64/css/default.css"

This is a file that has the css file used to style the tooltips.

    "help_directories": ["AcmeAssemblerC64/helpdb"],

This defines the directory where json formatted help files are located. Feel free to drop in your own.

    "scopes": ["source.assembly.AcmeAssembler"],

This definies in which scopes the plugin should work. So far it will fire up only in Acme Assembler scope.

    "log_level": "warning"

For the debugging purposes you can increase the log level to info or debug, open Python console (ctrl-\`) and observe what is going on and what problems the plugin has. If you report a bug, please use "debug" level and make sure you copy paste the whole output.

# Contribute

## Making changes

Fork repo, make changes and submit pull requests.

# Local development

Just clone repo into Sublime package folder and you can test the package "live" during development.

## IT Development:

p.s:
I **LOVE** coffee! Buy me a coffee at:   

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XWQDNV85QA9RC&source=url)



This plugin was originally created by //Swoffa of Noice


## Support

<img src="https://vangogh.teespring.com/v3/image/SugZ-DRGZXUTuSzfrFtaOU3TAUQ/800/800.jpg" width="100px"  height="100px">

[Help support by buying some merchandise](https://cavtronics-3.creator-spring.com/)

