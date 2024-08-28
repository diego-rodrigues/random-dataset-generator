# Random Dataset Generator

This project creates a dataset with random data according to a predefined schema.

## 🖊 Usage

To generate a set of random records, run the Python script with:
```shell
python random-dataset-generator.py [-h] [-i filename] [-o filename]
```
```
options:
  -h, --help    show this help message and exit
  -i filename, --input filename
                Use this flag to indicate the input file containing
                tables schemas. (default: input-schema.txt)
  -o filename, --output filename
                Use this flag to indicate the output file 
                containing generated records. (default:
                generated_records.json)
```

This will generate a file (`generated_records.json`) containing JSON lines, according to a predefined schema in a file (like [input-schema.txt](input-schema.txt)).

In each line, attribute, datatype, and nullability are specified (separated by space) according to the structure:

`attribute_name datatype(params?) N?K?` 

## 🧾 Table of Contents
- [Random Dataset Generator](#random-dataset-generator)
  - [🖊 Usage](#-usage)
  - [🧾 Table of Contents](#-table-of-contents)
  - [🔠 Data Types](#-data-types)
  - [📎 Usage example](#-usage-example)
  - [📎📝 Output example](#-output-example)
  - [🧑‍💻 Developer information](#-developer-information)
    - [🐍 Python environment](#-python-environment)

## 🔠 Data Types

- `attribute_name` is the name of the attribute, it cannot contain spaces

- `datatype(params?)` it the desired datatype. Some parameters can be specified (most parameters are optional). Accepted datatypes values are:
  - Numeric types:
    - `autoinc(start,step)`: auto incremental integer. It starts at `start` and the value increases by `step`. The block `(start,step)` is optional, if not specified, it assumes value `(1,1)`.
      
    - `int(min,max)`: a random integer value from `min` to `max`, inclusive. The block `(min,max)` is optional, if not specified, it assumes value `(0,100)`.

    - `number(min,max)`: same as `int`.

    - `float(min,max)`: a random float value from `min` to `max`, inclusive. Decimal points are also random between 1 and 5. The block `(min,max)` is optional, if not specified, it assumes value `(0,100)`.
    
    - `precision(decimals,min,max)`: a random float value from `min` to `max` inclusive, it will have `decimals` decimal points. The `decimals` argument is mandatory. The block `(min,max)` is optional, if not specified, it assumes value `(0,10)`. 

  - Text types:
    - `string(min,max)`: a random string with random lenght from `min` to `max`, inclusive. The block `(min,max)` is optional, if not specified, they assume values `(4,10)`.

    - `varchar(min,max)`: same as `string`.

    - `tokens(values...)`: selects randomly one of the provided `values` (comma-separated list without spaces).

  - Datetime types:
    - `datetime(start,end)`: generates a random date/time value from `start` to `end` dates, inclusive. Parameters must be in the format `yyyyy-mm-dd`.  The block `(start,end)` is optional, if not specified, it assumes values `(1970-01-01,TODAY)`. Generated date time is in format `dd/mm/yyyy HH:mm:ss`

    - `formatted_datetime(format,start,end)`: generates a formatted random date/time value from `start` to `end` dates, inclusive. Parameters must be in the format `yyyyy-mm-dd`.  The block `(start,end)` is optional, if not specified, it assumes values `(1970-01-01,TODAY)`. `format` is mandatory.

    Date formats can be seen the the [Python docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

  - Boolean types:
    - `boolean(chance_true)`: generates a random boolean with `chance_true` chance of generating `True` value. The block `(chance_true)` is optional, if not specified, it assumes value `(0.5)`.

  - Key type:
    - `foreign(key_source)`: it generates a value according to `key_source`. The parameter `key_source` must be in the format `[table_name].[attribute_name]` and the source table must be already defined in the [schema-input.txt](schema-input.txt) file.

- `N?`: nullability option. If provided, the value has a 10% chance of being `null`. If the option `K` (key) is also used, `N` is ignored as keys
        can't be `null`.
- `K?`: key option. If provided, the value is treated as a primary key. Which means no repeated values will be generated. It also enables the field to
        be used as a foreign key source.


## 📎 Usage example

* (Optionally) create and activate a Python environment:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

* Install the requirements:
```bash
pip install -r requirements.txt
```

* Create a schema definition file (`input-schema.txt`):
```
TableA 7
# This is a comment, this line is ignored

AutoId AUTOINC(1,3) K
Identifier STRING(20) K
Some_Code STRING(2,5) N
Account_ID INT

TableB 5

ID AUTOINC
ID_EVEN AUTOINC(2,2)
FKeyAttribute FOREIGN(TableA.AutoId) K
FKeyAtt__Repeat FOREIGN(TableA.Identifier) 
```

* Run the script
```bash
python random_dataset_generator.py -i input-schema.txt -o generated_records.json
```

## 📎📝 Output example

```json
{"AutoId": 1, "Identifier": "VBdZl26m4H", "Some_Code": "mRc", "Account_ID": 92}
{"AutoId": 4, "Identifier": "KsIUR", "Some_Code": "af", "Account_ID": 86}
{"AutoId": 7, "Identifier": "lZlNqyinj", "Some_Code": "1Zk", "Account_ID": 49}
{"AutoId": 10, "Identifier": "h6nw0F4Fa", "Some_Code": "3O", "Account_ID": 13}
{"AutoId": 13, "Identifier": "jMAjorzKNV", "Some_Code": "IS", "Account_ID": 53}
{"AutoId": 16, "Identifier": "0Hw7i", "Some_Code": "6Ao", "Account_ID": 47}
{"AutoId": 19, "Identifier": "4dYAB8hSW", "Some_Code": "WBd", "Account_ID": 25}
{"ID": 1, "ID_EVEN": 2, "FKeyAttribute": 4, "FKeyAtt__Repeat": "VBdZl26m4H"}
{"ID": 2, "ID_EVEN": 4, "FKeyAttribute": 13, "FKeyAtt__Repeat": "KsIUR"}
{"ID": 3, "ID_EVEN": 6, "FKeyAttribute": 1, "FKeyAtt__Repeat": "VBdZl26m4H"}
{"ID": 4, "ID_EVEN": 8, "FKeyAttribute": 7, "FKeyAtt__Repeat": "KsIUR"}
{"ID": 5, "ID_EVEN": 10, "FKeyAttribute": 16, "FKeyAtt__Repeat": "h6nw0F4Fa"}
```

## 🧑‍💻 Developer information

### 🐍 Python environment

Create and activate a Python environment with:
```bash
virtualenv -p /opt/homebrew/bin/python3.10 env3.10
env3.10/bin/activate
```
