import sublime, sublime_plugin, sys

# Some Atom scopes are different from Sublime Text
# https://gist.github.com/idleberg/fca633438329cc5ae327
SCOPES = [
    [ "source.c++", ".source.cpp" ],
    [ "source.java-props", ".source.java-properties" ],
    [ "source.objc++", ".source.objcpp" ],
    [ "source.php", ".source.html.php" ],
    [ "source.scss", ".source.css.scss" ],
    [ "source.todo", ".text.todo" ],
    [ "source.markdown", ".source.gfm" ]
]

# Automatic conversion, based on scope
class AutomizrCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        scope = self.view.scope_name(self.view.sel()[0].a)

        if "source.json" in scope or "source.sublimecompletions" in scope: 
            print("Atomizr: JSON detected, trying to convert")
            self.view.run_command('subl_to_atom')
        elif "source.coffee" in scope:
            print("Atomizr: CoffeeScript detected, trying to convert")
            self.view.run_command('atom_to_subl')
        elif "text.xml" in scope:
            print("Atomizr: XML detected, trying to convert")
            self.view.run_command('subl_snippets_to_atom')
        elif "text.plain" in scope:
            sublime.error_message("Atomizr: Automatic conversion requires a supported CoffeeScript package to be installed")
        else:
            sublime.error_message("Atomizr: Unsupported scope, aborting")

# Converts Sublime Text into Atom snippets
class SublToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        scope = self.view.scope_name(self.view.sel()[0].a)

        if "source.json" in scope or "source.sublimecompletions" in scope: 
            print("Atomizr: JSON detected, trying to convert")
            self.view.run_command('subl_completions_to_atom')
        elif "text.xml" in scope:
            print("Atomizr: XML detected, trying to convert")
            self.view.run_command('subl_snippets_to_atom')

# Converts Sublime Text completions into Atom snippets
class SublCompletionsToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            data = json.loads(selection)
        except ValueError:
            sublime.error_message("Atomizr: Invalid JSON")
            return

        # but is it a Sublime Text completion?
        try:
            # get scope, convert if necessary
            for subl, atom in SCOPES:
                if data['scope'] == subl:
                    scope = atom
                    break
                else:
                    scope = "." + data['scope']

            completions = data['completions']
        except:
            sublime.error_message("Atomizr: Not a Sublime Text completions file")
            return

        array = {}

        for item in completions:
            body = Helper.add_trailing_tabstop(item['contents'])
            try:
                array[item['trigger']] = {'prefix': item['trigger'], 'body':  body}
            except KeyError:
                pass

        atom = {scope: (array)}

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, cson.dumps(atom, sort_keys=True, indent=4))

        # set syntax to CSON, requires Better CoffeeScript package
        package = Helper.get_coffee()
        if package is not False:
            self.view.set_syntax_file(package)

# Converts Sublime Text completions into Atom snippets
class SublSnippetsToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, xmltodict

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            xml = xmltodict.parse(selection)
        except:
            sublime.error_message("Atomizr: Invalid XML, aborting conversion")
            return

        body = xml['snippet']['content']
        scope = xml['snippet']['scope']
        prefix = xml['snippet']['tabTrigger']

        # <description> is optional
        try:
            xml['snippet']['description']
        except:
            description = prefix

        body = Helper.add_trailing_tabstop(body)
        
        atom = {scope: { description: { "prefix": prefix, "body": body} } }

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, cson.dumps(atom, sort_keys=True, indent=2))

        # set syntax to CSON, requires Better CoffeeScript package
        package = Helper.get_coffee()
        if package is not False:
            self.view.set_syntax_file(package)

# Converts Atom snippets into Sublime Text completions
class AtomToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            data = cson.loads(selection)
        except:
            sublime.error_message("Atomizr: Invalid CSON, aborting conversion")
            return

        completions = []

        # but is it an Atom snippet?
        try:
            # get scope, convert if necessary
            for key in data.keys():
                for subl, atom in SCOPES:
                    if key == atom:
                        scope = subl
                        break
                    else:
                        scope = key.lstrip(".")

                for item in (data[key]):
                    body = Helper.remove_trailing_tabstop(data[key][item]["body"])
                    completions.append( {"trigger": data[key][item]["prefix"], "contents": body} )
        except:
            sublime.error_message("Atomizr: Not an Atom snippet file")
            return

        

        subl = {"scope": scope, "completions": completions}

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(subl, sort_keys=False, indent=2, separators=(',', ': ')))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

# Convert Atom format
class AtomToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        scope = self.view.scope_name(self.view.sel()[0].a)

        if "source.json" in scope: 
            print("Atomizr: JSON detected, trying to convert to CSON")
            self.view.run_command('atom_json_to_cson')
        elif "source.coffee" in scope:
            print("Atomizr: CSON detected, trying to convert to JSON")
            self.view.run_command('atom_cson_to_json')
        else:
            sublime.error_message("Atomizr: Unsupported scope, aborting")

# Converts Atom snippets (CSON into JSON)
class AtomCsonToJsonCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            data = cson.loads(selection)
        except:
            sublime.error_message("Atomizr: Invalid CSON, aborting conversion")
            return

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

# Converts Atom snippets (JSON into CSON)
class AtomJsonToCsonCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            data = json.loads(selection)
        except:
            sublime.error_message("Atomizr: Invalid JSON, aborting conversion")
            return

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, cson.dumps(data, sort_keys=True, indent=2))

        # set syntax to CSON, requires Better CoffeeScript package
        package = Helper.get_coffee()
        if package is not False:
            self.view.set_syntax_file(package)

# Helper functions
class Helper():

    def add_trailing_tabstop(input):
        import re

        m = re.search(r'\$\d+$', input)

        if m is not None:
            # nothing to do here
            return input

        stops = re.findall(r'\${?(\d+)', input)
        if len(stops) > 0:
            stops.sort()
            highest = int(stops[-1]) + 1
            return input + "$" + str(highest)

        return input + "$1"

    def remove_trailing_tabstop(input):
        import re

        m = re.search(r'\$\d+$', input)

        if m is None:
            # nothing to do here
            return input

        # remove tabstop
        return re.sub(r'\$\d+$', "", input)

    def get_coffee():
        import os

        # package locations
        locations = [sublime.installed_packages_path(), sublime.packages_path()]

        # supported packages
        packages = ["Better CoffeeScript", "CoffeeScript", "IcedCoffeeScript"]

        # iterate over packages locations
        for location in locations:
            # iterate over packages installed with Package Control
            for package in packages:
                if os.path.isfile(location + "/" + package + ".sublime-package") is True:
                    if package is "IcedCoffeeScript":
                        return "Packages/IcedCoffeeScript/Syntaxes/IcedCoffeeScript.tmLanguage"
                    else:
                        return "Packages/" + package + "/CoffeeScript.tmLanguage"

        sublime.error_message("Atomizr: Automatic conversion requires a supported CoffeeScript package to be installed")
        return False