import sublime, sublime_plugin
from .helpers import Helpers

class VsCode():

    def read_json(input):
        """Reads Visual Studio Code snippets, returns object"""
        import json

        # interprete and validate data
        try:
            data = json.loads(input)
        except:
            sublime.error_message("Atomizr\n\nInvalid JSON, aborting conversion")
            return False

        completions = []

        # but is it a Visual Studio snippet?
        try:
            for k in data:
                prefix = data[k]["prefix"]
                if "description" in data[k]:
                    description = data[k]["description"]
                body = data[k]["body"]

                contents = Helpers.remove_trailing_tabstop(data[k]["body"])
                if "description" in data[k]:
                    completions.append( {"trigger": prefix, "contents": body, "description": description} )
                else:
                    completions.append( {"trigger": prefix, "contents": body} )

        except:
            sublime.error_message("Atomizr\n\nNot a Visual Studio Code snippet file")
            return False

        output = {
            "scope": "source",
            "completions": completions
        }

        return output

    def write_json(input):
        """Writes Visual Studio Code snippets, returns object"""
        output = {}

        for snippet in input["completions"]:
            if "trigger" not in snippet and "contents" not in snippet:
                continue

            prefix = snippet["trigger"]
            if "description" in snippet:
                description = snippet["description"]
            body = snippet["contents"]

            try:
                if "description" in snippet:
                    output[prefix] = {'prefix': prefix, 'body':  body, 'description': description}
                else:
                    output[prefix] = {'prefix': prefix, 'body':  body}

            except KeyError:
                pass

        return output