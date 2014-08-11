__author__ = 'ehonlia'

JSON = 'application/json'

mimetype_map = {
    'xml': 'text/xml',
    'json-ld': JSON,
    'n3': 'text/plain',
    None: 'text/xml'
}


def correct_format(output_format):
    if output_format is None:
        corrected_output_format = 'n3'
    else:
        corrected_output_format = output_format

    return corrected_output_format
