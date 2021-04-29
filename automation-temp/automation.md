# Automation  
For use with Block Groups

### 1. Collect data
    * Download B03002 from ACS 2019 or new decennial, etc.
    * Download shapefiles for relevant unit
  
### 2. Process CSV data (LibreOffice for now)
    * Remove not needed columns
    * Rename columns

### 3. Merge (QGIS for now)
    * Select relevant Block Groups for District
    * Merge shapefile data with processed csv data

### 4. Create YML
    * Be careful of indentation

### 5. Apply districtr-process
    * Check work
    * Copy output.json into distrctr:/assets/data/modules/State.json
    * Edit distrctr:/assets/data/landing_pages.json

### 6. Apply districtr-process upload to mapbox

### 7. Check deployment