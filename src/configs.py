from datetime import datetime

# Settings of default values for random generator
MIN_STRING_LENGTH = 4
MAX_STRING_LENGTH = 10
MIN_NUMBER = 0
MAX_NUMBER = 100
MIN_PRECISION_NUMBER = 0
MAX_PRECISION_NUMBER = 10
MIN_RANDOM_DATE = datetime(1970, 1, 1)
MAX_RANDOM_DATE = datetime.today()
DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
AUTOINC_START = 1
AUTOINC_STEP = 1

# size of contents when printing table details on console
PRINT_LINE_SIZE = 45

# number of tries generating disctinct values
MAX_TRIES_GEN_RAND = 5

# Chance of a nullable attribute of being null
CHANCE_RANDOM_NULL = 0.10
