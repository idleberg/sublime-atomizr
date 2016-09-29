import sublime

GENERATOR = "Generated with Atomizr - https://github.com/idleberg/sublime-atomizr"

class SublimeText():

    def read_json(input):
        """Reads Sublime Text completions (JSON), returns object"""
        import json, sys

        # interprete and validate data
        try:
            data = json.loads(input)
        except ValueError:
            sublime.error_message("Atomizr\n\nInvalid JSON")
            return False

        scope_replacements = sublime.load_settings('Atomizr.sublime-settings').get("scopeReplacements")

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

            if "trigger" not in item and "contents" not in item:
                print("Atomizr: Skipping " + str(item))
                continue
            
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

            completion["contents"] = item['contents']

            output["completions"][i] = completion
            i += 1

        return output

    def read_xml(input):
        """Reads Sublime Text snippets (Plist), returns object"""
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
        if 'description' in xml['snippet']:
            description = xml['snippet']['description']

        contents = xml['snippet']['content']

        if "description" in xml["snippet"]:
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
        else:
            output = {
                "scope": scope, 
                "completions": [
                    {
                        "trigger": trigger,
                        "contents": contents,
                    }
                ]
            }

        return output

    def write_json(input):
        """Writes Sublime Text completions (JSON)"""

        # create tab-separated description
        for completion in input["completions"]:
            if "trigger" not in completion and "contents" not in completion:
                continue

            if "description" in completion:
                completion['trigger'] = completion['trigger'] + "\t" + completion["description"]
                completion.pop("description", None)

        output = {
            "#": GENERATOR,
            "scope": input["scope"],
            "completions": input["completions"]
        }

        return output

    def write_xml(input):
        """Writes Sublime Text snippets (Plist)"""
        from lxml import etree

        completions = input["completions"][0]

        data = etree.Element("snippet")
        content = etree.SubElement(data, "content")
        content.text = etree.CDATA(input["completions"][0]["contents"])
        tabTrigger = etree.SubElement(data, "tabTrigger")
        tabTrigger.text = input["completions"][0]['trigger']
        scope = etree.SubElement(data, "scope")
        scope.text = input["scope"]

        if 'description' in input['completions'][0]:
            description = etree.SubElement(data, "description")
            description.text = input["completions"][0]["description"]

        output = etree.tostring(data, pretty_print=True, encoding="utf-8").decode('utf-8')

        return output
