import sublime, sublime_plugin

# Converts Sublime Text completions into Atom snippets
class SublToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import json
        
        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate date
        try:
            data = json.loads(selection)
        except ValueError:
            sublime.error_message("Error: No valid JSON")

        # but is it a Sublime Text completion?
        try:
            scope = "." + data['scope']
            completions = data['completions']
        except:
            sublime.error_message("Error: No Sublime Text completions")

        array = {}

        for item in completions:
            try:
                array[item['trigger']] = {'prefix': item['trigger'], 'body':  item['contents']}
            except KeyError:
                pass

        atom = {scope: (array)}

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(atom, sort_keys=True, indent=4, separators=(',', ': ')))

# TODO: Converts Atom snippets into Sublime Text completions
class AtomToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json
        
        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate date
        try:
            data = cson.loads(selection)
        except:
            sublime.error_message("Error: No valid CSON")

        print("\nNot yet implemented, printing JSON instead:")
        print(json.dumps(data))

# Converts Atom snippets (CSON into JSON)
class AtomToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json
        
        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate date
        try:
            data = cson.loads(selection)
        except:
            sublime.error_message("Error: No valid CSON")

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
