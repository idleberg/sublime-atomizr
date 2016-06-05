import sublime, sublime_plugin, sys

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

        if "source.json" in scope: 
            print("Atomizr: JSON detected, trying to convert")
            self.view.run_command('subl_to_atom')
        elif "source.coffee" in scope:
            print("Atomizr: CoffeeScript detected, trying to convert")
            self.view.run_command('atom_to_subl')
        elif "text.xml" in scope:
            print("Atomizr: XML detected, trying to convert")
            self.view.run_command('subl_snip_to_atom')
        elif "text.plain" in scope:
            sublime.error_message("Atomizr: Automatic conversion requires the 'Better CoffeeScript' package to be installed")
        else:
            sublime.error_message("Atomizr: Unsupported scope, aborting")

# Converts Sublime Text completions into Atom snippets
class SublToAtomCommand(sublime_plugin.TextCommand):

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
            try:
                array[item['trigger']] = {'prefix': item['trigger'], 'body':  item['contents']}
            except KeyError:
                pass

        atom = {scope: (array)}

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, cson.dumps(atom, sort_keys=True, indent=4, separators=(',', ': ')))

        # set syntax to CSON, requires Better CoffeeScript package
        self.view.set_syntax_file("Packages/Better CoffeeScript/CoffeeScript.tmLanguage")

# Converts Sublime Text completions into Atom snippets
class SublSnipToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, xmltodict

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # xmltodict.parse(selection)
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

        atom = {scope: { description: { "prefix": prefix, "body": body} } }

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, cson.dumps(atom, sort_keys=True, indent=2, separators=(',', ': ')))

        # set syntax to CSON, requires Better CoffeeScript package
        self.view.set_syntax_file("Packages/Better CoffeeScript/CoffeeScript.tmLanguage")

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
                    completions.append( {"trigger": data[key][item]["prefix"], "contents": data[key][item]["body"]} )
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

# Converts Atom snippets (CSON into JSON)
class AtomToAtomCommand(sublime_plugin.TextCommand):

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
