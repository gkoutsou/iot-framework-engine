__author__ = 'ehonlia'

import re

# Solr/Lucene special characters: + - ! ( ) { } [ ] ^ " ~ * ? : \
# There are also operators && and ||, but we're just going to escape
# the individual ampersand and pipe chars.
# Also, we're not going to escape backslashes!
# http://lucene.apache.org/java/2_9_1/queryparsersyntax.html#Escaping+Special+Characters
__ESCAPE_CHARS_RE = re.compile(r'(?<!\\)(?P<char>[&|+\-!(){}[\]^"~*?:])')


def lucene_escape(value):
    r"""Escape un-escaped special characters and return escaped value.

    >>> lucene_escape(r'foo+') == r'foo\+'
    True
    >>> lucene_escape(r'foo\+') == r'foo\+'
    True
    >>> lucene_escape(r'foo\\+') == r'foo\\+'
    True
    """
    return __ESCAPE_CHARS_RE.sub(r'\\\g<char>', value)
