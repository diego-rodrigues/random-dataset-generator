
import src.data_generator as dg
import argparse
from src.configs import DEFAULT_FILE_INPUT, DEFAULT_FILE_OUTPUT

# parse_type("string(10)")                        # not-accepted: it will take default min, max values
# parse_type("string(10,20)")                     # it takes min as 10 and max as 20
# parse_type("int")                               # it takes default min as 0 and max as 100
# parse_type("int(33,5)")                         # it will revert min as 5 and max as 33
# parse_type("int(3,5)")                          # it takes min as 3 and max as 5
# parse_type("tokens(a,b,c,12)")                  # it uses randomly one of the 4 tokens provided
# parse_type("precision(10)")                     # it uses 10 decimal points, min as 0 and max as 10
# parse_type("precision(10,20,30)")               # it uses 10 decimal points, min as 20 and max as 30
# parse_type("precision(10,5,3)")                 # it uses 10 decimal points, min as 3 and max as 5
# parse_type("boolean")                           # it uses .5 chance of true
# parse_type("boolean(0.23)")                     # it uses .23 chance of true
# parse_type("boolean(1.23)")                     # it uses .5 chance of true
# parse_type("date(2020-02-20,2021-11-21)")       # it generates dates between the specified dates
# parse_type("date(2022-02-20,2021-11-21)")       # it generates dates between the specified dates
# parse_type("date")                              # it generates dates between 1970 and today
# parse_type("formatted_date(%m/%d/%Y,2020-02-20,2021-11-21)")
# parse_type("formatted_date(%m/%d/%Y,2022-02-20,2021-11-21)")
# parse_type("formatted_date(%m/%d/%Y)")          # it generates dates between 1970 and today
# parse_type("autoinc(1,10)")                     # it generates an incremental value starting at 1 and adding 10 each time
# parse_type("autoinc(-1,10)")                    # it generates an incremental value starting at -1 and adding 10 each time
# parse_type("autoinc(1,-10)")                    # it generates an incremental value starting at 1 and adding -10 each time
# parse_type("autoinc(10)")                       # not accepted: it generates an incremental value starting at 1 and adding 1 each time
# parse_type("autoinc")                           # it generates an incremental value starting at 1 and adding 1 each time
# parse_type("foreign(table.attribute)")          # it generates values from the pool of values from table.attribute
# allow null values with option N at the end of the line
# allow distinct values with option K at the end of the line

# date formats: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

def _create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Random Dataset Generator')
    parser.add_argument('-i', "--input", action='store', metavar='filename',
                        help="Use this flag to indicate the input file containing tables schemas. (default: {})".format(DEFAULT_FILE_INPUT),
                        default=DEFAULT_FILE_INPUT)
    parser.add_argument('-o', "--output", action='store', metavar='filename',
                        help="Use this flag to indicate the output file containing generated records. (default: {})".format(DEFAULT_FILE_OUTPUT),
                        default=DEFAULT_FILE_OUTPUT)
    return parser


def _parse_args(parser: argparse.ArgumentParser) -> tuple[str,str]:
    args = parser.parse_args()
    return args.input, args.output


if __name__ == "__main__":
    input, output = _parse_args(_create_arg_parser())
    dg.run(input, output)
