import sublime
from .helpers import Helpers

class Atom():

    def read_cson(input):
        """Reads Atom snippets (CSON)"""
        import cson

        # interprete and validate data
        try:
            data = cson.loads(input)
        except:
            sublime.error_message("Atomizr\n\nInvalid CSON, aborting conversion")
            return False

        completions = []
        scope_replacements = sublime.load_settings('Atomizr.sublime-settings').get("scopeReplacements") or True

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

                # add description, if available
                for item in (data[key]):
                    trigger = data[key][item]["prefix"]
                    description = None
                    
                    if "description" in data[key][item]:
                        description = data[key][item]["description"]
                    else:
                        if item != trigger:
                            description = item

                    contents = Helpers.remove_trailing_tabstop(data[key][item]["body"])
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

    def write_cson(input):
        """Writes Atom snippets (CSON)"""
        snippets = {}

        scope = input["scope"]

        if scope[0] != ".":
            scope = "." + scope

        for snippet in input["completions"]:
            if "trigger" not in snippet and "contents" not in snippet:
                continue

            prefix = snippet["trigger"]
            if "description" in snippet:
                description = snippet["description"]
            else:
                description = snippet["trigger"]
            body = snippet["contents"]

            try:
                snippets[description] = {'prefix': prefix, 'body':  body}
            except KeyError:
                pass

        output = {
            scope: (snippets)
        }

        return output
