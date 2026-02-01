
FILE_EXTENSION = "NC"

UNITS = "MM"

ROTARY_WRAP_Y = "Y"

SUBSTITUTE = "({)}"

+------------------------------------------------
+    Line terminating characters
+------------------------------------------------

LINE_ENDING = "[13][10]"

+------------------------------------------------
+    Block numbering
+------------------------------------------------

LINE_NUMBER_START     = 0
LINE_NUMBER_INCREMENT = 10
LINE_NUMBER_MAXIMUM = 999999

+================================================
+
+    Formating for variables
+
+================================================

VAR LINE_NUMBER = [N|A|N|1.0]
VAR SPINDLE_SPEED = [S|A|S|1.0]
VAR FEED_RATE = [F|C|F|1.1]
VAR X_POSITION = [X|A|X|1.3]
VAR Y_POSITION = [Y|A|Y|1.3]
VAR Z_POSITION = [Z|A|Z|1.3]
VAR X_HOME_POSITION = [XH|A|X|1.3]
VAR Y_HOME_POSITION = [YH|A|Y|1.3]
VAR Z_HOME_POSITION = [ZH|A|Z|1.3]
VAR SAFE_Z_HEIGHT = [SAFEZ|A|Z|1.3]
VAR WRAP_DIAMETER = [WRAP_DIA|A||1.3]

+================================================
+
+    Block definitions for toolpath output
+
+================================================

+---------------------------------------------------
+  Commands output at the start of the file
+---------------------------------------------------

begin HEADER

+"( [TP_FILENAME] )"
+"( File created: [DATE] - [TIME])"
+"( Laguna CNC Turner )"
+"( Material Size)"
+"( X= [XLENGTH], Z= [ZLENGTH])"
+"( Diameter = [WRAP_DIA] mm)"
+"( X Values are wrapped around the Y axis )"
+"( X Values are output as X )"
+"([FILE_NOTES])"
+"(Toolpaths used in this file:)"
+"([TOOLPATHS_OUTPUT])"
+"(Tools used in this file: )"
+"([TOOLS_USED])"
+"[N] G00G21G17G90G40G49G80"
+"[N] G71G91.1"
+"[N] T[T]M06"
+"[N] G00G43[ZH]H[T]"
"[N] M03"
+"[N](Toolpath:- [TOOLPATH_NAME])"
+"[N]([TOOLPATH_NOTES])"
+"[N] G94"
+"[N] G00 [YH] [XH] [ZH]"

+---------------------------------------------------
+  Commands output for rapid moves
+---------------------------------------------------

begin RAPID_MOVE

"[N] G00 [X] [Y] [Z]"


+---------------------------------------------------
+  Commands output for the first feed rate move
+---------------------------------------------------

begin FIRST_FEED_MOVE

"[N] G01 [X] [Y] [Z][F]"


+---------------------------------------------------
+  Commands output for feed rate moves
+---------------------------------------------------

begin FEED_MOVE

"[N] G01 [X] [Y] [Z]"


+---------------------------------------------------
+  Commands output for a new segment - toolpath
+  with same toolnumber but maybe different feedrates
+---------------------------------------------------

begin NEW_SEGMENT

+"[N] [S]M03"
+"([TOOLPATH_NAME])"
+"([TOOLPATH_NOTES])"

+---------------------------------------------------
+  Commands output at the end of the file
+---------------------------------------------------

begin FOOTER

+"[N] G00 [ZH]"
+"[N] G00 [YH] [XH]"
+"[N] M09"
"[N] M05"
"[N] M30"
+%
