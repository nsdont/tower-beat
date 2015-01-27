#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import consts

TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" \
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.github.mailto1587.tower-beat</string>
    <key>ProgramArguments</key>
    <array>
        <string>python</string>
        <string>{script_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Minute</key>
        <integer>00</integer>
        <key>Hour</key>
        <integer>22</integer>
    </dict>
</dict>
</plist>"""


def main():
    script_path = os.path.join(consts.BASE_DIR, 'beatit.py')
    print TEMPLATE.format(script_path=script_path)

if __name__ == '__main__':
    main()
