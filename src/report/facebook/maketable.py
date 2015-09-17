#!/usr/bin/env python

import report.facebook.maketable_messages, report.facebook.maketable_contacts, getopt, sys

def makereport(case, timeline):
    report.facebook.maketable_contacts.makereport(case)
    report.facebook.maketable_messages.makereport(case, timeline)

