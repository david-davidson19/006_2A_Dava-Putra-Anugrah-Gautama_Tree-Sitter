(string) @string
["and" "or" "not"] @keyword
["in" "contains"] @keyword
["=" "!=" ">" "<" ">=" "<="] @function
(number) @number
(boolean) @type
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)