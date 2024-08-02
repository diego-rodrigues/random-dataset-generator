
pattern_str_int = '(varchar|string|number|int|float)(?:\((-?\d+),(-?\d+)\))?'
pattern_tokens = '(tokens)(?:\((.+)\))'
pattern_precision = '(precision)\((\d+)(?:,(-?\d+)(?:,(-?\d+))?)?\)'
pattern_bool = '(boolean)(?:\((\d+\.\d+)\))?'
pattern_datetime = '(datetime)(?:\((\d{4}-\d{2}-\d{2}),\s*(\d{4}-\d{2}-\d{2})\))?'
pattern_formatted_datetime = '(formatted_datetime)\(([A-z|\%|\/|\-|\:]+)(?:,(\d{4}-\d{2}-\d{2}),\s*(\d{4}-\d{2}-\d{2}))?\)'
pattern_autoinc = '(autoinc)(?:\((-?\d+),(-?\d+)\))?'
pattern_foreign = '(foreign)(?:\((\w+)\.(\w+)\))'
