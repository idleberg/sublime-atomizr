import sublime, sublime_plugin

# Converts Sublime Text completions into Atom snippets
class SublToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import json
        
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        try:
            data = json.loads(selection)
        except ValueError:
            sublime.error_message("Error: No valid JSON")

        scope = "." + data['scope']
        completions = data['completions']

        array = {}

        for item in completions:
            try:
                array[item['trigger']] = {'prefix': item['trigger'], 'body':  item['contents']}
            except KeyError:
                pass

        atom = {scope: (array)}

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(atom, sort_keys=True, indent=4, separators=(',', ': ')))


# TODO: Converts Atom snippets into Sublime Text completions
class AtomToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json
        
        selection = self.view.substr(sublime.Region(0, self.view.size()))

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
        
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        try:
            data = cson.loads(selection)
        except:
            sublime.error_message("Error: No valid CSON")

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
