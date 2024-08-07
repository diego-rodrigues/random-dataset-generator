import src.data_types as dt

pattern_str_int = '({}|{}|{}|{}|{})(?:\((-?\d+),(-?\d+)\))?'.format(dt.VOC_VARCHAR, dt.VOC_STRING, dt.VOC_INT, dt.VOC_NUMBER, dt.VOC_FLOAT)
pattern_tokens = '({})(?:\((.+)\))'.format(dt.VOC_TOKENS)
pattern_precision = '({})\((\d+)(?:,(-?\d+)(?:,(-?\d+))?)?\)'.format(dt.VOC_PRECISION)
pattern_bool = '({})(?:\((\d+\.\d+)\))?'.format(dt.VOC_BOOLEAN)
pattern_datetime = '('+dt.VOC_DATETIME+')(?:\((\d{4}-\d{2}-\d{2}),\s*(\d{4}-\d{2}-\d{2})\))?'
pattern_formatted_datetime = '('+dt.VOC_FORM_DATETIME+')\(([A-z|\%|\/|\-|\:]+)(?:,(\d{4}-\d{2}-\d{2}),\s*(\d{4}-\d{2}-\d{2}))?\)'
pattern_autoinc = '({})(?:\((-?\d+),(-?\d+)\))?'.format(dt.VOC_AUTOINC)
pattern_foreign = '({})(?:\((\w+)\.(\w+)\))'.format(dt.VOC_FOREIGN)

all_patterns = '(?:{})|(?:{})|(?:{})|(?:{})|(?:{})|(?:{})|(?:{})|(?:{})'\
    .format(pattern_str_int,pattern_tokens,pattern_precision,pattern_bool,\
            pattern_datetime,pattern_formatted_datetime,pattern_autoinc,pattern_foreign)
