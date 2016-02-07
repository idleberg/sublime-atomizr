import sublime, sublime_plugin

class AtomizrCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import json
        
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        try:
            data = json.loads(selection)
        except ValueError:
            sublime.error_message("No valid JSON")

        scope = "." + data['scope']
        completions = data['completions']

        array = {}

        for item in completions:
            try:
                array[item['trigger']] = {'prefix': item['trigger'], 'body':  item['contents']}
            except KeyError:
                pass
            ˆ

        atom = {scope: (array)}

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(atom, sort_keys=True, indent=4, separators=(',', ': ')))
