#!/usr/bin/env python3

import sys
import html


def translate_markdown(lines, printer):
    in_quote = False
    quote = []
    for line in lines:
        line = line.rstrip()
        quote_line = line.startswith('> ') or line == '>'
        if not in_quote and quote_line:
            in_quote = True
        elif in_quote and not quote_line:
            in_quote = False
            translate_quote(quote, printer)
            quote = []

        if in_quote:
            quote.append(line)
        else:
            printer(line)

    if in_quote:
        translate_quote(quote, printer)


def translate_quote(lines, printer):
    assert len(lines) > 0
    pruned_lines = [strip_quoting(line) for line in lines]
    is_poetry = pruned_lines[-1].startswith('=')
    if is_poetry:
        printer('<blockquote class="poetry">')
    else:
        printer('<blockquote>')

    for line in pruned_lines:
        if line.startswith('- ') or line.startswith('= '):
            printer('<cite>' + line[2:] + '</cite>')
        elif line == '=':
            continue
        elif line.startswith('  '):
            printer('<p class="indent">' + line[2:] + '</p>')
        elif line != '':
            printer('<p>' + line + '</p>')
        elif line == '' and is_poetry:
            printer('<br>')
    printer('</blockquote>')


def strip_quoting(line):
    if line.startswith('> '):
        return line[2:]
    elif line == '>':
        return line[1:]
    else:
        raise ValueError()


if __name__ == "__main__":
    translate_markdown(sys.stdin, print)
