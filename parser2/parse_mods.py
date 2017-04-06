"""Parses a mods.xml file from the daily CREC dumps.

"""

from __future__ import print_function

import argparse

from lxml import etree


DEFAULT_XML_NS = {'ns': 'http://www.loc.gov/mods/v3'}


def xpath_parse(root, paths, namespaces):
    """Takes an lxml ROOT or element corresponding to the mods.xml doc and
    produces, yanks out useful info, and returns it as a dict.

    PATHS is a dict of fieldname -> xpath query mappings. xpath_parse
    will return records that have the fieldnames with the query
    applied to the root.

    For instance, with PATHS={'foo': '//bar'}, xpath_parse will return
    {'foo': [all instances of bar elements]}.

    """

    results = {}
    for k, p in paths.items():
        value = root.xpath(p, namespaces=namespaces)
        results[k] = value

    return results


class OutputDestinationError(Exception):
    pass

def stdout_outputter(records):
    for r in records:
        print(r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Extract constituent records from mods.xml.",
    )
    parser.add_argument('--mods', type=str, required=True,
                        help="xml file to load")
    parser.add_argument('--out', type=str, default='-',
                        help="output destination (defaults to stdout)")
    args = parser.parse_args()

    if args.out == '-':
        outputter = stdout_outputter
    else:
        raise OutputDestinationError("unknown output destination %s" % args.out)
    tree = etree.parse(open(args.mods, 'r'))

    constituents = tree.xpath(
        '//ns:relatedItem[@type="constituent"]',
        namespaces=DEFAULT_XML_NS,
    )

    records = [
        xpath_parse(
            r,
            {
                'ID': 'string(@ID)',
                'title': 'string(ns:titleInfo/ns:title)',
                'title_part': 'string(ns:titleInfo/ns:partName)',
                'pdf_url': 'string(ns:location/ns:url[@displayLabel="PDF rendition"])',
                'html_url': 'string(ns:location/ns:url[@displayLabel="HTML rendition"])',
                'page_start': 'string(ns:part[@type="article"]/ns:extent/ns:start)',
                'page_end': 'string(ns:part[@type="article"]/ns:extent/ns:end)',
                'speakers': 'ns:name[@type="personal"]/ns:namePart/text()',
            },
            namespaces={'ns': 'http://www.loc.gov/mods/v3'},
        )
        for r in constituents
    ]

    outputter(records)
