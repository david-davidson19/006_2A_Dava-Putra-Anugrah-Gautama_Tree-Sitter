/**
 * @file Filter grammar for tree-sitter
 * @author Dava Putra Anugrah Gautama
 * @license MIT
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

export default grammar({
  name: "filter",
  extras: $ => [/\s/],

  // 4b
  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison,        // dasar (langkah 2-3)
      $.and_expression,    // 4b
      $.or_expression,     // 4c
      $.parenthesized,     // 4d
      $.not_expression,    // 4e
      $.in_expression,     // 4f
      $.contains_expression // 4g
    ),

    // 4b
    and_expression: $ => prec.left(2, seq(
      field('left', $._expr),
      'and',
      field('right', $._expr),
    )),

    // 4c
    or_expression: $ => prec.left(1, seq(
      field('left', $._expr),
      'or',
      field('right', $._expr),
    )),

    // 4d
    parenthesized: $ => seq('(', $._expr, ')'),

    // 4e
    not_expression: $ => prec(3, seq('not', field('operand', $._expr))),
    
    _value: $ => choice($.string, $.number, $.boolean),

    // 4a
    comparison: $ => seq(
      field('field', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('value', $._value),
    ),
  
    in_expression: $ => seq(
      field('field', $.identifier),
      'in',
      '(',
      field('value', $._value),
      repeat(seq(',', field('value', $._value))),
      ')',
    ),

    contains_expression: $ => seq(
      field('field', $.identifier),
      'contains',
      field('value', $.string),
    ),

    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,

    string: $ => /"[^"]*"/,

    // 4a
    number: $ => /\d+/,

    // 4e
    boolean: $ => choice('true', 'false'),
  },
});