(string) @string
["and" "or" "not"] @keyword
["in" "contains"] @keyword
["=" "!=" ">" "<" ">=" "<="] @operator
(number) @number
(boolean) @constant.builtin
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)
