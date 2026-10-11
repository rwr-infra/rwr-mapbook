@echo off
rem NOTE: keep this file ASCII-only. cmd.exe parses .bat files with the console
rem code page, so non-ASCII lines next to "chcp 65001" get shredded into bogus
rem commands. English comments only.
rem
rem Mobile / narrow-screen preview: a device frame that renders the site at real
rem phone widths (the page's own media queries apply -- it is not a scaled desktop
rem page). Requires the desktop preview to be running already: start.bat.
rem Different port? Open mobile.html with ?port=8010, or set it in the page's URL box.

start "" "%~dp0mobile.html"
