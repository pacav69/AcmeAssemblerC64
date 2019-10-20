//----------------------------------------------------------
//				Description
//----------------------------------------------------------

//----------------------------------------------------------
rla
sre 
define
adc
//----------------------------------------------------------
// Code for creating the breakpoint file sent to Vice.
//----------------------------------------------------------
.var _useBinFolderForBreakpoints = cmdLineVars.get("usebin") == "true"
.var _createDebugFiles = cmdLineVars.get("afo") == "true"
.print "File creation " + [_createDebugFiles
 ? "enabled (creating breakpoint file)"
 : "disabled (no breakpoint file created)"]
.var brkFile
.if(_createDebugFiles) {
 .if(_useBinFolderForBreakpoints)
 .eval brkFile = createFile("bin/breakpoints.txt")
 else
 .eval brkFile = createFile("breakpoints.txt")
}
.macro break() {
.if(_createDebugFiles) {
 .eval brkFile.writeln("break " + toHexString(*))
 }
}
//------------------------------------------------------