#!/bin/bash

echo "#!/bin/bash" > /opt/afft/extractor/extractor.sh
echo "" >> /opt/afft/extractor/extractor.sh
echo "# This script is automatically generated. Do not make manual changes, or it will be overwritten at next regeneration" >> /opt/afft/extractor/extractor.sh
echo "" >> /opt/afft/extractor/extractor.sh
find /opt/afft/extractor -name extract.sh -exec echo "sudo {} \$1" >> /opt/afft/extractor/extractor.sh \;
echo "sudo chown -R \$USER \$1" >> /opt/afft/extractor/extractor.sh

