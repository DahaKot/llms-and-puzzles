import re


def replace_spans(template, span_dict):
    text = template
    for k, v in span_dict.items():
        text = text.replace(k, v)
    return text


def normalize_unicode(s):
    for x in re.findall(r"\\u([\da-f]{4})", s):
        s = s.replace(f"\\u{x}", chr(int(x, 16)))
    return s
