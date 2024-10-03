# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 11:16:09 2023

@author: mvvsk
"""

import fastf1
event = fastf1.get_event(2023, 'Austrian')

print(event.get_session_name(1))
print(event.get_session_name(2))
print(event.get_session_name(3))
print(event.get_session_name(4))
print(event.get_session_name(5))