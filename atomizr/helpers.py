import sublime

class Helpers():

    def rename_file(self, extension):
        if sublime.load_settings('Atomizr.sublime-settings').get("renameFiles") != True:
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

        if m is not None or sublime.load_settings('Atomizr.sublime-settings').get("addTrailingTabstops") == False:
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

        if m is None or sublime.load_settings('Atomizr.sublime-settings').get("removeTrailingTabstops") == False:
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
                settings = sublime.load_settings('Preferences.sublime-settings').get("ignored_packages")
                if package in settings:
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
