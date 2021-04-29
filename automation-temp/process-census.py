'''

Steps 1 and 2 of automation.md
Download of shapefiles?

'''

#GEO_ID and NAME is same

# Delete Margin columns, i.e. check for an M
delete_columns = \
    'B03002_009E', 'B03002_010E', 'B03002_019E', 'B03002_020E', 'B03002_021E',

rename_columns = {\
    'B03002_001E': 'TOTPOP',
    'B03002_002E': 'NH_WHITE',
    'B03002_003E': 'NH_BLACK',
    'B03002_004E': 'NH_AMIN',
    'B03002_005E': 'NH_ASIAN',
    'B03002_006E': 'NH_NHPI',
    'B03002_007E': 'NH_OTHER',
    'B03002_008E': 'NH_2MORE',
    'B03002_011E': 'HISP',
    'B03002_012E': 'H_WHITE',
    'B03002_013E': 'H_BLACK',
    'B03002_014E': 'H_AMIN',
    'B03002_015E': 'H_ASIAN',
    'B03002_016E': 'H_NHPI',
    'B03002_017E': 'H_OTHER',
    'B03002_018E': 'H_2MORE'}

# Download B03002, ACS20195Y 
# Remove margin of error columns
# Truncate GEO_ID to right 12 characters
# After creating csv, make csvt to help QGIS with datatypes