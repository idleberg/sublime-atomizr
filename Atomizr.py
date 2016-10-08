import sublime, sublime_plugin

from .atomizr.atom import Atom
from .atomizr.sublime_text import SublimeText
from .atomizr.vscode import VsCode
from .atomizr.helpers import Helpers

GENERATOR = "Generated with Atomizr - https://github.com/idleberg/sublime-atomizr"
ATOM_GENERATOR = "# %s\n" % GENERATOR
XML_GENERATOR = "<!-- %s -->\n" % GENERATOR

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
            sublime.message_dialog("Atomizr\n\nAutomatic conversion requires a supported CoffeeScript package to be installed")
        else:
            sublime.message_dialog("Atomizr\n\nUnsupported scope, aborting")

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
            sublime.message_dialog("Atomizr\n\nUnsupported scope, aborting")

# Converts Atom snippets into Sublime Text completions
class AtomToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))
        data = Atom.read_cson(input)
        if data is False:
            return

        output = SublimeText.write_json(data)

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
        indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        Helpers.set_json(self)
        Helpers.rename_file(self, "sublime-completions")

        # Reset selection
        Helpers.reset_selection(self)

# Converts Atom snippets (CSON into JSON)
class AtomCsonToJsonCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            data = cson.loads(selection)
        except BaseException as e:
            sublime.message_dialog("Atomizr\n\nInvalid CSON, aborting conversion. See console for details.")
            print(e)

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or False
        indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(data, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        Helpers.set_json(self)
        Helpers.rename_file(self, "json")

        # Reset selection
        Helpers.reset_selection(self)

# Converts Atom snippets (JSON into CSON)
class AtomJsonToCsonCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            data = json.loads(selection)
        except BaseException as e:
            sublime.message_dialog("Atomizr\n\nInvalid JSON, aborting conversion. See console for details.")
            print(e)

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("cson_sort_keys") or True
        indent = sublime.load_settings('Atomizr.sublime-settings').get("cson_indentation") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, ATOM_GENERATOR + cson.dumps(data, sort_keys=sort_keys, indent=indent))

        # set syntax to CSON, requires supported CoffeeScript package
        if Helpers.get_coffee(self) is True:
            Helpers.rename_file(self, "cson")

        # Reset selection
        Helpers.reset_selection(self)

# Converts Atom snippets into Visual Studio Code snippets
class AtomToVscodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        try:
            data = cson.loads(input)
        except BaseException as e:
            sublime.message_dialog("Atomizr\n\nInvalid CSON, aborting conversion. See console for details.")
            print(e)

        for key in data.keys():
            if key[0] != ".":
                sublime.message_dialog("Atomizr\n\nNot an Atom snippet file")
                return
            output = data[key]

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
        indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        Helpers.set_json(self)
        Helpers.rename_file(self, "json")

        # Reset selection
        Helpers.reset_selection(self)

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
        else:
            sublime.message_dialog("Atomizr\n\nNot a Sublime Text completions file")

# Converts Sublime Text completions into Atom snippets
class SublCompletionsToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        data = SublimeText.read_json(input)
        if data is False:
            return

        output = Atom.write_cson(data)

        json_snippets = sublime.load_settings('Atomizr.sublime-settings').get("atom_json_snippets") or False

        if json_snippets is True:

            sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
            indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

            # set syntax to JSON
            Helpers.set_json(self)
            Helpers.rename_file(self, "json")
        else:
            # Get CSON settings
            sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("cson_sort_keys") or True
            indent = sublime.load_settings('Atomizr.sublime-settings').get("cson_indentation") or 2

            # write converted data to view
            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, ATOM_GENERATOR + cson.dumps(output, sort_keys=sort_keys, indent=indent))

            # set syntax to CSON, requires supported CoffeeScript package
            if Helpers.get_coffee(self) is True:
                Helpers.rename_file(self, "cson")

        # Reset selection
        Helpers.reset_selection(self)

# Converts Sublime Text completions into Atom snippets
class SublSnippetsToAtomCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        import cson, xmltodict

        input = self.view.substr(sublime.Region(0, self.view.size()))
        data = SublimeText.read_xml(input)
        if data is False:
            return

        output = Atom.write_cson(data)

        json_snippets = sublime.load_settings('Atomizr.sublime-settings').get("atom_json_snippets") or False

        if json_snippets is True:

            sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
            indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

            # set syntax to JSON
            Helpers.set_json(self)
            Helpers.rename_file(self, "json")
        else:
            # Get CSON settings
            sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("cson_sort_keys") or True
            indent = sublime.load_settings('Atomizr.sublime-settings').get("cson_indentation") or 2

            # write converted data to view
            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, ATOM_GENERATOR + cson.dumps(output, sort_keys=sort_keys, indent=indent))

            # set syntax to CSON, requires supported CoffeeScript package
            if Helpers.get_coffee(self) is True:
                Helpers.rename_file(self, "cson")

        # Reset selection
        Helpers.reset_selection(self)

# Convert Atom format
class SublToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        scope = self.view.scope_name(self.view.sel()[0].a)

        if "source.json" in scope or "source.sublimecompletions" in scope:
            print("Atomizr: JSON detected, trying to convert to XML")
            self.view.run_command('subl_json_to_xml')
        elif "text.xml" in scope:
            print("Atomizr: XML detected, trying to convert to JSON")
            self.view.run_command('subl_xml_to_json')
        else:
            sublime.message_dialog("Atomizr\n\nUnsupported scope, aborting")

# Converts Sublime Text snippets into Sublime Text completions
class SublJsonToXml(sublime_plugin.TextCommand):

    def run(self, edit):
        import json
        from lxml import etree

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        data = SublimeText.read_json(input)

        output = SublimeText.write_xml(data)

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, XML_GENERATOR + output)

        # set syntax to XML
        Helpers.set_xml(self)
        Helpers.rename_file(self, "sublime-snippet")

        # Reset selection
        Helpers.reset_selection(self)

# Converts Sublime Text snippets into Sublime Text completions
class SublXmlToJson(sublime_plugin.TextCommand):

    def run(self, edit):
        import json, xmltodict

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        data = SublimeText.read_xml(input)
        if data is False:
            return

        output = SublimeText.write_json(data)

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
        indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent))

        # set syntax to JSON
        Helpers.set_json(self)
        Helpers.rename_file(self, "sublime-completions")

        # Reset selection
        Helpers.reset_selection(self)

# Converts Sublime Text snippets into Visual Studio Code snippets
class SublToVscodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        scope = self.view.scope_name(self.view.sel()[0].a)

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        if "source.json" in scope or "source.sublimecompletions" in scope: 
            print("Atomizr: JSON detected, trying to convert")
            data = SublimeText.read_json(input)
        elif "text.xml" in scope:
            print("Atomizr: XML detected, trying to convert")
            data = SublimeText.read_xml(input)
        else:
            sublime.message_dialog("Atomizr\n\nNot a Sublime Text completions file")

        if data is False:
            return

        output = VsCode.write_json(data)

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
        indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        Helpers.set_json(self)
        Helpers.rename_file(self, "sublime-completions")

        # Reset selection
        Helpers.reset_selection(self)

# Convert Visual Studio Code into Atom snippets
class VscodeToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import json, cson, sublime

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        try:
            data = json.loads(input)
        except BaseException as e:
            sublime.message_dialog("Atomizr\n\nInvalid JSON, aborting conversion. See console for details.")
            print(e)

        for key in data.keys():
            if key[0] == ".":
                sublime.message_dialog("Atomizr\n\nNot a Visual Studio Code snippet file")
                return

        if "completions" in data or "scope" in data:
            sublime.message_dialog("Atomizr\n\nNot a Visual Studio Code snippet file")
            return

        output = {
            ".source": data
        }

        json_snippets = sublime.load_settings('Atomizr.sublime-settings').get("atom_json_snippets") or False

        if json_snippets is True:
            # Get JSON settings
            sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
            indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

            # set syntax to JSON
            Helpers.set_json(self)
            Helpers.rename_file(self, "json")
        else:
            # Get CSON settings
            sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("cson_sort_keys") or True
            indent = sublime.load_settings('Atomizr.sublime-settings').get("cson_indentation") or 2

            # write converted data to view
            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, ATOM_GENERATOR + cson.dumps(output, sort_keys=sort_keys, indent=indent))

            # set syntax to CSON, requires supported CoffeeScript package
            if Helpers.get_coffee(self) is True:
                Helpers.rename_file(self, "cson")

        Helpers.select_scope(self, "atom", ATOM_GENERATOR)

# Convert Visual Studio Code into Atom snippets
class VscodeToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        data = VsCode.read_json(input)
        if data is False:
            return

        output = SublimeText.write_json(data)

        sort_keys = sublime.load_settings('Atomizr.sublime-settings').get("json_sort_keys") or True
        indent = sublime.load_settings('Atomizr.sublime-settings').get("json_indentation") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent))

        # set syntax to JSON
        Helpers.set_json(self)
        Helpers.rename_file(self, "sublime-completions")

        Helpers.select_scope(self, "sublime", None)
