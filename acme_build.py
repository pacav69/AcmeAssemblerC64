import sublime, sublime_plugin 
import os 
import platform 
import glob
import shutil
import json

# This file is based on work from:
# https://github.com/STealthy-and-haSTy/SublimeScraps/blob/master/build_enhancements/custom_build_variables.py
#
# Huge thanks to OdatNurd!!
 
# List of variable names we want to support 
custom_var_list = [ "acme_compile_args",
                    "acme_compile_debug_additional_args",
                    "acme_run_command_c64debugger",
                    "acme_debug_command_c64debugger",
                    "acme_run_command_x64",
                    "acme_debug_command_x64",
                    "acme_run_path",
                    "acme_emulator_run_path",
                    "acme_debug_path",
                    "acme_jar_path",
                    "acme_args",
                    "acme_run_args",
                    "acme_debug_args",
                    "acme_startup_file_path",
                    "acme_breakpoint_filename",
                    "acme_compiled_filename",
                    "acme_output_path",
                    "default_prebuild_path",
                    "default_postbuild_path"]

vars_to_expand_list = [ 
                        "acme_compiled_filename",
                        "acme_args",
                        "acme_run_args",
                        "acme_debug_args",
                        "acme_compile_args",
                        "acme_run_command_x64",
                        "acme_debug_command_x64",
                        "acme_run_command_c64debugger",
                        "acme_debug_command_c64debugger",
                        ]

class acmeBuildCommand(sublime_plugin.WindowCommand):
    """
    Provide custom build variables to a build system, such as a value that needs
    to be specific to a current project.
    """
    def createExecDict(self, sourceDict, buildMode, settings):
        global custom_var_list, vars_to_expand_list

        try:
            # Save path variable from expansion
            tmpPath = sourceDict.pop('path', None)

            # Variables to expand; start with defaults, then add ours.
            variables = self.window.extract_variables()
            variables.update(self.getFilenameVariables(buildMode, settings, variables))

            # Create the command
            acmeCommand = acmeCommandFactory(settings).createCommand(variables, buildMode)
            sourceDict['shell_cmd'] = acmeCommand.CommandText

            # Add pre and post variables
            extendedDict = acmeCommand.updateEnvVars(sourceDict)

            for custom_var in custom_var_list:
                variables[custom_var] = settings.getSetting(custom_var)

            # Expand variables (mutiple times to support variables in Variables)
            for x in range(2):
                variables_to_expand = {k: v for k, v in variables.items() if k in vars_to_expand_list}
                variables = self.mergeDictionaries(variables, sublime.expand_variables (variables_to_expand, variables))

            # Create arguments to return by expanding variables in the
            # arguments given.
            args = sublime.expand_variables (extendedDict, variables)

        # Reset path to unexpanded and add path addition from settings
            args['path'] = self.getPathDelimiter().join(filter(None, [settings.getSetting("acme_path"), tmpPath]))

            envSetting = settings.getSetting("acme_env")
            if envSetting:
                args['env'].update(envSetting)
        except Exception as ex:
            sourceDict['shell_cmd'] = "echo %s" % ex
            return sourceDict

        return args

    def getFilenameVariables(self, buildMode, settings, variables):
        useStartup = 'startup' in buildMode
        fileToBuild = settings.getSetting("acme_startup_file_path") if useStartup else variables["file_base_name"]
        fileToBuildPath = "%s/%s.%s" % (variables["file_path"], fileToBuild, variables["file_extension"])
        buildAnnotations = self.parseAnnotations(fileToBuildPath)
        fileToRunAnnotation = buildAnnotations.get("file-to-run") if buildAnnotations else None
        return {
            "build_file_base_name": fileToBuild,
            "start_filename" : fileToRunAnnotation if fileToRunAnnotation else settings.getSetting("acme_compiled_filename")
            }

    def parseAnnotations (self, filename):
        with open(filename, 'r') as handle:
            firstline = handle.readline().strip()
        try:
            return (json.loads("{%s}" % firstline[2:].strip().split("@acme-build", 1)[1]) 
                    if firstline.startswith("//") and "@acme-build" in firstline 
                    else {})
        except ValueError as err:
            raise ValueError("Could not parse build annotations: %s" % err)

    def getPathDelimiter(self):
        return ";" if platform.system()=='Windows' else ":" 

    def emptyFolder(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def mergeDictionaries(self, x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

    def run(self, **kwargs):
        settings = SublimeSettings(self)
        if not settings.isLoaded(): 
            errorMessage = "Settings could not be loaded, please restart Sublime Text."
            sublime.error_message(errorMessage) 
            print(errorMessage)
            return

        outputFolder = settings.getSetting("acme_output_path")

        # os.makedirs() caused trouble with Python versions < 3.4.1 (see https://docs.python.org/3/library/os.html#os.makedirs);
        # to avoid abortion (on UNIX-systems) here, we simply wrap the call with a try-except
        # (the output-directory will be generated anyway via the output-parameter in the compile-command)
        try:
            os.makedirs(outputFolder, exist_ok=True)
        except:
            pass

        if settings.getSettingAsBool("acme_empty_bin_folder_before_build") and os.path.isdir(outputFolder):
            self.emptyFolder(outputFolder)

        self.window.run_command('exec', self.createExecDict(kwargs, kwargs.pop('buildmode'), settings))

class SublimeSettings():
    def __init__(self, parentCommand):
        # Get the project specific settings
        project_data = parentCommand.window.project_data()
        self.__project_settings = (project_data or {}).get('settings', {})

        # Get the view specific settings
        self.__view_settings = parentCommand.window.active_view().settings()

    def isLoaded(self):
        return self.__getSetting("acme_output_path") != None

    def getSetting(self, settingKey):
        setting = self.__getSetting(settingKey)
        return setting if setting else ""

    def __getSetting(self, settingKey): 
        return self.__view_settings.get(settingKey, self.__project_settings.get(settingKey, None))

    def getSettingAsBool(self, settingKey): 
        return self.getSetting(settingKey).lower() == "true"

class acmeCommand():
    def __init__(self, commandText, hasPreCommand, hasPostCommand, buildMode):
        self.__commandText = commandText
        self.__hasPreCommand = hasPreCommand
        self.__hasPostCommand = hasPostCommand
        self.__buildMode = buildMode

    @property
    def CommandText(self):
        return self.__commandText

    def updateEnvVars(self, sourceDict):
        if not self.__hasPreCommand and not self.__hasPostCommand: return sourceDict
        prePostEnvVars = {
            "acme_buildmode": self.__buildMode,
            "acme_file": "${build_file_base_name}.${file_extension}",
            "acme_file_path": "${file_path}",
            "acme_prg_file": "${file_path}/${acme_output_path}/${acme_compiled_filename}",
            "acme_bin_folder": "${file_path}/${acme_output_path}",
            }
        sourceDict.get('env').update(prePostEnvVars)
        return sourceDict

class acmeCommandFactory():
    def __init__(self, settings):
        self.__settings = settings
 
    def createCommand(self, variables, buildMode): 
        return self.createMakeCommand(variables, buildMode) if buildMode=="make" else self.createacmeCommand(variables, buildMode)

    def createMakeCommand(self, variables, buildMode): 
        makeCommand = self.getRunScriptStatement("make", "default_make_path")
        makeCommand = makeCommand if makeCommand else "echo Make file not found. Place a file named make.%s in ${file_path}%s" % (self.getExt(), " or %s." % (self.__settings.getSetting("default_make_path")) if self.__settings.getSetting("default_make_path") else ".")
        return acmeCommand(makeCommand, True, False, buildMode)

    def createacmeCommand(self, variables, buildMode): 
        # javaCommand = "java -cp \"${acme_jar_path}\"" if self.__settings.getSetting("acme_jar_path") else "java"  
        javaCommand = "acme"
          # \"${acme_jar_path}\"" if self.__settings.getSetting("acme_jar_path") else "java"  

        # ompileCommand = javaCommand+" cml.acme.acmeembler ${acme_compile_args} "
        compileCommand = javaCommand+" ${acme_compile_args} "

        compileDebugCommandAdd = "${acme_compile_debug_additional_args}"

        runCommand = "${acme_run_command_x64}" 
        if "c64debugger" in self.__settings.getSetting("acme_run_path").lower():
            runCommand = "${acme_run_command_c64debugger}" 

        debugCommand = "${acme_debug_command_x64}"
        if "c64debugger" in self.__settings.getSetting("acme_debug_path").lower():
            debugCommand = "${acme_debug_command_c64debugger}" 

        useRun = 'run' in buildMode
        useDebug = 'debug' in buildMode

        command =  " ".join([compileCommand, compileDebugCommandAdd, "&&", self.createMonCommandsStatement()]) if useDebug else compileCommand

        preBuildScript = self.getRunScriptStatement("prebuild", "default_prebuild_path")
        postBuildScript = self.getRunScriptStatement("postbuild", "default_postbuild_path")

        if preBuildScript:
            command = " ".join([preBuildScript, "&&", command])
        if postBuildScript:
            command = " ".join([command, "&&", postBuildScript])
        if useDebug:
            command = " ".join([command, "&&", debugCommand])
        elif useRun:
            command = " ".join([command, "&&", runCommand])

        return acmeCommand(command.strip(), preBuildScript != None, postBuildScript != None, buildMode)

    def getExt(self): 
        return "bat" if platform.system()=='Windows' else "sh" 

    def getRunScriptStatement(self, scriptFilename, defaultScriptPathSetting):
        defaultScriptCommand = "%s/%s.%s" % (self.__settings.getSetting(defaultScriptPathSetting), scriptFilename, self.getExt())
        hasDefaultScriptCommand = glob.glob(defaultScriptCommand)
        scriptCommand = "%s.%s" % (scriptFilename, self.getExt())
        hasScriptCommand = glob.glob(scriptCommand)
        return "%s \"%s\"" % ("call" if platform.system()=='Windows' else ".", (scriptCommand if hasScriptCommand else defaultScriptCommand)) if hasScriptCommand or hasDefaultScriptCommand else None 
 
    def createMonCommandsStatement(self):
        if platform.system()=='Windows':
            return "copy /Y \"${acme_output_path}\\\\${build_file_base_name}.vs\" + \"${acme_output_path}\\\\${acme_breakpoint_filename}\" \"${acme_output_path}\\\\${build_file_base_name}_MonCommands.mon\""
        else:
            return "[ -f \"${acme_output_path}/${acme_breakpoint_filename}\" ] && cat \"${acme_output_path}/${build_file_base_name}.vs\" \"${acme_output_path}/${acme_breakpoint_filename}\" > \"${acme_output_path}/${build_file_base_name}_MonCommands.mon\" || cat \"${acme_output_path}/${build_file_base_name}.vs\" > \"${acme_output_path}/${build_file_base_name}_MonCommands.mon\""