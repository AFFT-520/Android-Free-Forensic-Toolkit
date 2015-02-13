#!/bin/bash

# This script is automatically generated. Do not make manual changes, or it will be overwritten at next regeneration

sudo /opt/afft/extractor/facebook/extract.sh $1
sudo /opt/afft/extractor/mms-sms/extract.sh $1
sudo /opt/afft/extractor/gmail/extract.sh $1
sudo /opt/afft/extractor/whatsapp/extract.sh $1
sudo /opt/afft/extractor/call-log/extract.sh $1
sudo /opt/afft/extractor/skype/extract.sh $1
sudo /opt/afft/extractor/contacts/extract.sh $1
sudo chown -R $USER $1
