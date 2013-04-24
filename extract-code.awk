#!/usr/bin/gawk -f

BEGIN { p = 0; }
/.begin.python/ { p = 1; }
/.end.python/ { p = 0; }
/^[^\\]/ { if (p == 1) { print ; } }
