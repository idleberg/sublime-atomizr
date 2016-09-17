import sublime, sublime_plugin

SUBL_GENERATOR = "Generated with Atomizr - https://github.com/idleberg/sublime-atomizr"
ATOM_GENERATOR = "# %s\n" % SUBL_GENERATOR
XML_GENERATOR = "<!-- %s -->\n" % SUBL_GENERATOR

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
            sublime.error_message("Atomizr\n\nAutomatic conversion requires a supported CoffeeScript package to be installed")
        else:
            sublime.error_message("Atomizr\n\nUnsupported scope, aborting")

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
            sublime.error_message("Atomizr\n\nNot a Sublime Text completions file")

# Converts Sublime Text completions into Atom snippets
class SublCompletionsToAtomCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        data = read_subl_completions(input)
        if data is False:
            return

        output = write_atom_snippets(data)

        # Get CSON settings
        sort_keys = loadConfig().get("csonSortKeys") or True
        indent = loadConfig().get("csonIndent") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, ATOM_GENERATOR + cson.dumps(output, sort_keys=sort_keys, indent=indent))

        # set syntax to CSON, requires Better CoffeeScript package
        package = get_coffee()
        if package is not False:
            self.view.set_syntax_file(package)

        rename_file(self, "cson")

# Converts Sublime Text completions into Atom snippets
class SublSnippetsToAtomCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        import cson, xmltodict

        input = self.view.substr(sublime.Region(0, self.view.size()))
        data = read_subl_snippet(input)
        if data is False:
            return

        output = write_atom_snippets(data)

        # Get CSON settings
        sort_keys = loadConfig().get("csonSortKeys") or True
        indent = loadConfig().get("csonIndent") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, ATOM_GENERATOR + cson.dumps(output, sort_keys=sort_keys, indent=indent))

        # set syntax to CSON, requires Better CoffeeScript package
        package = get_coffee()
        if package is not False:
            self.view.set_syntax_file(package)

        rename_file(self, "cson")

# Converts Atom snippets into Sublime Text completions
class AtomToSublCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))
        data = read_atom_snippet(input)
        if data is False:
            return

        output = write_subl_completions(data)

        sort_keys = loadConfig().get("jsonSortKeys") or True
        indent = loadConfig().get("jsonIndent") or 2

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        rename_file(self, "sublime-completions")

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
            sublime.error_message("Atomizr\n\nUnsupported scope, aborting")

# Converts Atom snippets into Visual Studio Code snippets
class AtomToVscodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))
        data = read_atom_snippet(input)
        if data is False:
            return

        output = write_vscode_snippets(data)

        sort_keys = loadConfig().get("jsonSortKeys") or True
        indent = loadConfig().get("jsonIndent") or 2

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        rename_file(self, "json")

# Converts Sublime Text snippets into Visual Studio Code snippets
class SublToVscodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import cson, json

        scope = self.view.scope_name(self.view.sel()[0].a)

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        if "source.json" in scope or "source.sublimecompletions" in scope: 
            print("Atomizr: JSON detected, trying to convert")
            data = read_subl_completions(input)
        elif "text.xml" in scope:
            print("Atomizr: XML detected, trying to convert")
            data = read_subl_snippet(input)
        else:
            sublime.error_message("Atomizr\n\nNot a Sublime Text completions file")

        # data = read_subl_snippet(input)
        if data is False:
            return

        output = write_vscode_snippets(data)

        sort_keys = loadConfig().get("jsonSortKeys") or True
        indent = loadConfig().get("jsonIndent") or 2

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(output, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        rename_file(self, "json")

        # Converts Sublime Text snippets into Sublime Text completions
class SublJsonToXml(sublime_plugin.TextCommand):

    def run(self, edit):
        import json
        from lxml import etree

        # read data from view
        input = self.view.substr(sublime.Region(0, self.view.size()))

        data = read_subl_completions(input)

        output = write_subl_snippet(data)
        if output is False:
            return

        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, XML_GENERATOR + output)

        # set syntax to XML
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/XML/XML.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/XML/XML.tmLanguage')

        rename_file(self, "sublime-snippet")

# Converts Sublime Text snippets into Sublime Text completions
class SublXmlToJson(sublime_plugin.TextCommand):

    def run(self, edit):
        import json, xmltodict

        # read data from view
        selection = self.view.substr(sublime.Region(0, self.view.size()))

        # interprete and validate data
        try:
            xml = xmltodict.parse(selection)
        except:
            sublime.error_message("Atomizr\n\nInvalid XML, aborting conversion")
            return

        contents = xml['snippet']['content']
        scope = xml['snippet']['scope']
        trigger = xml['snippet']['tabTrigger']

        # <description> is optional
        try:
            description = xml['snippet']['description']
            trigger = trigger + "\t" + description
        except:
            pass

        contents = add_trailing_tabstop(contents)

        subl = {
            "#": SUBL_GENERATOR,
            "scope": scope,
            "completions": [
                {
                    "trigger": trigger,
                    "contents": contents
                }
            ]
        }

        sort_keys = loadConfig().get("jsonSortKeys") or True
        indent = loadConfig().get("jsonIndent") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(subl, sort_keys=sort_keys, indent=indent))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        rename_file(self, "sublime-completions")

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
            sublime.error_message("Atomizr\n\nInvalid CSON, aborting conversion")
            return

        sort_keys = loadConfig().get("jsonSortKeys") or False
        indent = loadConfig().get("jsonIndent") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, json.dumps(data, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

        # set syntax to JSON
        if sublime.version() >= "3103":
            self.view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        else:
            self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        rename_file(self, "json")

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
            sublime.error_message("Atomizr\n\nInvalid JSON, aborting conversion")
            return

        sort_keys = loadConfig().get("csonSortKeys") or True
        indent = loadConfig().get("csonIndent") or 2

        # write converted data to view
        selection = sublime.Region(0, self.view.size())
        self.view.replace(edit, selection, cson.dumps(data, sort_keys=sort_keys, indent=indent))

        # set syntax to CSON, requires Better CoffeeScript package
        package = get_coffee()
        if package is not False:
            self.view.set_syntax_file(package)

        rename_file(self, "cson")

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
            sublime.error_message("Atomizr\n\nUnsupported scope, aborting")

# Helper functions
def read_atom_snippet(input):
    import cson
    # interprete and validate data
    try:
        data = cson.loads(input)
    except:
        sublime.error_message("Atomizr\n\nInvalid CSON, aborting conversion")
        return False

    completions = []
    scope_replacements = loadConfig().get("scopeReplacements") or True

    # but is it an Atom snippet?
    try:
        for key in data.keys():
            # get scope, convert if necessary
            for subl, atom in scope_replacements:
                if key == atom:
                    scope = subl
                    break
                else:
                    scope = key.lstrip(".")

            # split tab-separated description
            for item in (data[key]):
                if item != data[key][item]["prefix"]:
                    description = item
                trigger = data[key][item]["prefix"]

                contents = remove_trailing_tabstop(data[key][item]["body"])
                if description is None:
                    completions.append( {"trigger": trigger, "contents": contents} )
                else:
                    completions.append( {"trigger": trigger, "contents": contents, "description": description} )

    except:
        sublime.error_message("Atomizr\n\nNot an Atom snippet file")
        return False

    output = {
        "scope": scope,
        "completions": completions
    }

    return output

def read_subl_completions(input):
    import json, sys

    # interprete and validate data
    try:
        data = json.loads(input)
    except ValueError:
        sublime.error_message("Atomizr\n\nInvalid JSON")
        return False

    scope_replacements = loadConfig().get("scopeReplacements") or True

    output = {}
    # but is it a Sublime Text completion?
    try:
        # get scope, convert if necessary
        for subl, atom in scope_replacements:
            if data['scope'] == subl:
                output["scope"] = atom
                break
            else:
                output["scope"] = data['scope']

    except:
        sublime.error_message("Atomizr\n\nNot a Sublime Text completions file")
        return False
    
    output["completions"] = data['completions']
    i = 0

    for item in output["completions"]:
        
        completion = {}

        # Split tab-separated description
        if "\t" in item['trigger']:
            tabs = item['trigger'].split("\t")

            if len(tabs) > 2:
                sublime.message_dialog("Atomizr: Conversion aborted, a trigger contains multiple tabs.")
                print("Atomizr: Conversion aborted, trigger '%s' contains multiple tabs." % item["trigger"].replace("\t", "\\t"))
                return False

            completion["trigger"] = tabs[0]
            completion["description"] = tabs[-1]
        else:
            completion["trigger"] = item['trigger']
            completion["description"] = item['trigger']

        completion["contents"] = add_trailing_tabstop(item['contents'])

        output["completions"][i] = completion
        i += 1

    return output

def read_subl_snippet(input):
    import xmltodict

    # interprete and validate data
    try:
        xml = xmltodict.parse(input)
    except:
        sublime.error_message("Atomizr\n\nInvalid XML, aborting conversion")
        return False

    scope = xml['snippet']['scope']
    trigger = xml['snippet']['tabTrigger']

    # <description> is optional
    try:
        description = xml['snippet']['description']
    except:
        description = xml['snippet']['tabTrigger']

    contents = add_trailing_tabstop(xml['snippet']['content'])

    output = {
        "scope": scope, 
        "completions": [
            {
                "trigger": trigger,
                "description": description,
                "contents": contents,
            }
        ]
    }

    return output

def write_atom_snippets(input):
    snippets = {}

    scope = input["scope"]

    if scope[0] != ".":
        scope = "." + scope

    for snippet in input["completions"]:
        prefix = snippet["trigger"]
        description = snippet["description"]
        body = snippet["contents"]

        try:
            snippets[description] = {'prefix': prefix, 'body':  body}
        except KeyError:
            pass

    output = {
        scope: (snippets)
    }

    return output

def write_vscode_snippets(input):
    output = {}

    for snippet in input["completions"]:
        prefix = snippet["trigger"]
        description = snippet["description"]
        body = snippet["contents"]

        try:
            output[prefix] = {'prefix': prefix, 'body':  body, 'description': description}
        except KeyError:
            pass

    return output

def write_subl_completions(input):

    output = {
        "#": SUBL_GENERATOR,
        "scope": input["scope"],
        "completions": input["completions"]
    }

    return output

def write_subl_snippet(input):
    from lxml import etree

    completions = input["completions"][0]

    data = etree.Element("snippet")
    content = etree.SubElement(data, "content")
    content.text = etree.CDATA(input["completions"][0]["contents"])
    tabTrigger = etree.SubElement(data, "tabTrigger")
    tabTrigger.text = input["completions"][0]['trigger']
    scope = etree.SubElement(data, "scope")
    scope.text = input["scope"]

    if input['completions'][0]['description']:
        description = etree.SubElement(data, "description")
        description.text = input["completions"][0]["description"]

    output = etree.tostring(data, pretty_print=True, encoding="utf-8").decode('utf-8')

    return output

def loadConfig():
    return sublime.load_settings('Atomizr.sublime-settings')

def isIgnored(package):
    settings = sublime.load_settings('Preferences.sublime-settings').get("ignored_packages")
    if package in settings:
        return True
    return False

def rename_file(self, extension):
    if loadConfig().get("renameFiles") != True:
        return

    import os

    inputFile = self.view.window().active_view().file_name()
    parentDir = os.path.dirname(inputFile)
    baseName = os.path.splitext(os.path.basename(inputFile))[0]
    fileName = baseName + "." + extension
    outputFile = os.path.join(parentDir, fileName)
    os.rename(inputFile, outputFile)
    
    self.view.set_name(fileName)
    self.view.retarget(outputFile)
    self.view.window().run_command("save")

def add_trailing_tabstop(input):
    import re

    m = re.search(r'\$\d+$', input)

    if m is not None or loadConfig().get("addTrailingTabstops") == False:
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

    if m is None or loadConfig().get("removeTrailingTabstops") == False:
        # nothing to do here
        return input

    # remove tabstop
    return re.sub(r'\$\d+$', "", input)

def get_coffee():
    import os

    # package locations
    locations = [sublime.installed_packages_path(), sublime.packages_path()]

    # supported packages
    packages = ["Better CoffeeScript", "CoffeeScript", "IcedCoffeeScript", "Mongoose CoffeeScript"]

    # iterate over packages locations
    for location in locations:
        # iterate over packages installed with Package Control
        for package in packages:
            # is "ignored_package"?
            if isIgnored(package) == True:
                continue

            if os.path.isfile(location + "/" + package + ".sublime-package") is True:
                if package is "IcedCoffeeScript":
                    return "Packages/IcedCoffeeScript/Syntaxes/IcedCoffeeScript.tmLanguage"
                elif package is "Mongoose CoffeeScript":
                    return "Packages/Mongoose CoffeeScript/CoffeeScript.tmLanguage"
                else:
                    return "Packages/" + package + "/CoffeeScript.tmLanguage"

    sublime.error_message("Atomizr\n\nAutomatic conversion requires a supported CoffeeScript package to be installed")
    return False
