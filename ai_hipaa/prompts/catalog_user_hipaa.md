# User
Generate python code.
- Employ python openpyxl module to read from input xlsx file.
- Employ python json module to write OSCAL catalog in JSON format.

The python code should require these arguments:
- Argument "--input" is "the path to the consumed xlsx file".
- Argument "--output" is "the path to the produced OSCAL catalog file".
- Argument "--title" is "the title of the produced OSCAL catalog".
- Argument "--version" is "the version of the produced OSCAL catalog".
- Argument "--oscal-version" is "the oscal-version of the produced OSCAL catalog".

## Objectives of the python code.
For OSCAL catalog with respect to "metadata":
- Use argument value "title" for "title".
- Use argument value "version" for version".
- Use argument value "oscal-version" for "oscal-version".
- Use the current-date-and-time for "last-modified".

## Transformation guidelines for xlsx to OSCAL json
For OSCAL catalog:
- xlsx column names can be found in row 1.
- Each group should have an "id".
    - Use prefix "group-" concatenated to string representation of group level for top level groups.
    - Use parent group id value concatenated to "." concatenated to integer starting from "1" and increasing by 1 for each subsequent group.
- Use non-empty values found under xlsx column "B" for OSCAL level 1 group.
    - split the text at the first ":".
    - use the first half of the text for level 1 group "title".
    - create a level 1 group "part".
        - for part "id" use the value of leve1 1 group "id" concatenated to "_desc".
        - for part "name" use "description".
        - for part "prose" use the second half of the text.
- Use non-empty values found under xlsx column "A" for OSCAL level 1 group property "value".
    - set property "name" to the value of the xlsx column name in lower case with whitespace replaced with "-".
    - set property "remarks" to the value of the xlsx column name.
- Use non-empty values found under xlsx column "D" for OSCAL level 2 group "title".
    - split the text at the first ":".
    - use the first half of the text for level 2 group "title".
    - create a level 2 group "part".
        - for part "id" use the value of leve1 2 group "id" concatenated to "_desc".
        - for part "name" use "description".
        - for part "prose" use the second half of the text.
- Use non-empty values found under xlsx column "C" for OSCAL level 2 group property "value".
    - set property "name" to the value of the xlsx column name in lower case with whitespace replaced with "-".
    - set property "remarks" to the value of the xlsx column name.
- Use non-empty values found under xlsx column "E" for OSCAL control "title" within level 2 group.
    - The row should be ignored when the column "E" text is "Implementation Specification (Required)".
- Use a program generated value for OSCAL control "id".
    - Use prefix "hipaa-" concatenated to string representation of integer value.
    - Use integer value of "001" with leading zeros included for first OSCAL control.
    - Each subsequent OSCAL control uses the next integer value.
- Each OSCAL control has zero or more "parts".
- Add 1 OSCAL control part for each non-empty value found under xlsx column "F".
    - Use control "id" value concatenated with "_smt" for value of part "id".
    - Use "statement" for value of part "name".
    - Use the xlsx column "F" value for value of part "prose".
- Add 1 OSCAL control part for each non-empty value found under xlsx column "G".
    - Use control "id" value concatenated with "_qst" for value of part "id".
    - Use "sample_questions" for value of part "name".
    - Use the xlsx column "G" value for value of part "prose".
