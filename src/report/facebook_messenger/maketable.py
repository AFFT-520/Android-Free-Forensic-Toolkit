#!/usr/bin/env python

import report.facebook_messenger.maketable_messages, report.facebook_messenger.maketable_contacts, getopt, sys


def makereport(case, timeline):
	report.facebook_messenger.maketable_contacts.makereport(case)
	report.facebook_messenger.maketable_messages.makereport(case, timeline)

