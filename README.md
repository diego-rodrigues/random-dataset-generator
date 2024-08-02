# Random Dataset Generator

This project creates a dataset with random data according to a predefined schema.

To generate a set of random records, run the Python script with:
```shell
python random_dataset_generator.py
```

This will generate a file (`generated_records.json`) containing JSON lines, according to a predefined schema in a file ([input-schema.txt](input-schema.txt)).

In each line, attribute, datatype, and nullability are specified (separated by space) according to the structure:

`attribute_name datatype(params?) N?K?` 

## 🧾 Table of Contents
- [Random Dataset Generator](#random-dataset-generator)
  - [🧾 Table of Contents](#-table-of-contents)
  - [🔠 Data Types](#-data-types)
  - [📎 Example](#-example)
  - [Developer information](#developer-information)
    - [Python environment](#python-environment)

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


## 📎 Example

Schema definition examples:
```
TableA 5
# This is a comment, this line is ignored

AutoId AUTOINC(1,3)
Identifier STRING(20) NK
Some_Code STRING(2,5) N
Account_ID INT

TableB 5

ID AUTOINC
ID2 AUTOINC(2,2)
premium_str PREMIUM K
FKeyAttribute FOREIGN(TableC.AutoId) K
FKeyAtt__Repeat FOREIGN(TableC.Identifier) 

TableA 3

ID AUTOINC(0,2)
PREMIUM_FK FOREIGN_PREMIUM(TableB.premium_str)
```

## Developer information

### Python environment

Create and activate a Python environment with:
```bash
virtualenv -p /opt/homebrew/bin/python3.10 env3.10
env3.10/bin/activate
```
