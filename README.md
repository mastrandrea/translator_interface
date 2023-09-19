# translator_interface

Test of translator implementation for NAIL

Conversion of a string with event variables described in a base format to specific format of the input dataset.


## Status

Base example working. Implementation of full fledge tests is in progress.

## Base format

Each variable can be represented in the following data model:

  Object[index].feature

Variables describing quantities with a single occurrence per event (e.g. Run number) can be described as:

 Event[0].Run_number


## Target format

The target format is the data format used for the representation of the input data (e.g. NANOAOD by CMS).
Example conversion from Base format to Target format:

 (e1) Obj[ind].feat -> Obj_feat[ind]


## Strategy

The data format conversion is implemented through 2 python classes:
 - translator.py       class responsible for the parsing of the expressions in the Base format
 - dictionary calss    (e.g. interfaceDictionary.py) class implementing the naming of the Base format features in the Target format, and the specific composition rules for the {object, index, feature} elements in the Target format (e.g. (e1) for NANOAOD)

The interface for a specific target data format can be realized re-implementing just the dictionary class (i.e. a specific dictionary for each target data format).


## Run the test:

python test_translation.py

Test string can be changed in the test_translation.py file.