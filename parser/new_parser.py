from __future__ import print_function

import argparse
import logging
from datetime import datetime
from datetime import timedelta

import boto3
import xmltodict
from botocore.exceptions import ClientError


CMD_LINE_DATE_FORMAT = '%Y-%m-%d'


def lambda_handler(event, context):
    pass


class CRECParser(object):

    MODS_S3_KEY_BASE_TEMPLATE = '{prefix}/%Y/%m/%d/mods/mods.xml'

    def __init__(self, s3_bucket, s3_prefix='capitolwords'):
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.mods_s3_key_template = self.MODS_S3_KEY_BASE_TEMPLATE.format(
            prefix=self.s3_prefix
        )
        self.s3 = boto3.client('s3')
        self.mods = None
        self.crec = None

    def load_mods_from_s3(self, dt=None):
        if dt is None:
            dt = datetime.utcnow() - timedelta(days=1)
        mods_s3_key = dt.strftime(self.mods_s3_key_template)
        logging.info('Reading mods.xml file from "{0}".'.format(mods_s3_key))
        response = self.s3.get_object(
            Bucket=self.s3_bucket,
            Key=mods_s3_key
        )
        self.mods = xmltodict.parse(response['Body'].read())['mods']
        return self.mods

    def load_mods_from_disk(self, filepath):
        doc = None
        with open(filepath) as f:
            raw_data = f.read()
            doc = xmltodict.parse(raw_data)
        self.mods = doc['mods']
        return self.mods

    def load_crec_from_s3(self, crec_s3_key):
        response = self.s3.get_object(
            Bucket=self.s3_bucket,
            Key=crec_s3_key,
        )
        self.crec = response['Body'].read()
        return self.crec

    def load_crec_from_disk(self, crec_path):
        with open(crec_path) as f:
            self.crec = f.read()
        return self.crec

    def get_crec_description(self, crec_id):
        relateds = []
        if self.mods is None:
            raise Exception('Mods file must be loaded first.')
        for related_item in self.mods['relatedItem']:
            if related_item['@ID'] == crec_id:
                relateds.append(related_item)
        return relateds

def main():
    parser = CRECParser(
        'use-this-bucket-to-test-your-bullshit',
        'capitolwords',
    )
    dt = datetime(2017, 2, 15)
    parser.load_mods_from_s3(dt=dt)
    crec_id = 'id-CREC-2017-02-15-pt1-PgD160'
    data = parser.get_crec_description(crec_id)
    return data

if __name__ == '__main__':
    parser = CRECParser(
        'use-this-bucket-to-test-your-bullshit',
        'capitolwords',
    )
    dt = datetime(2017, 2, 15)
    parser.load_mods_from_s3(dt=dt)

# capitolwords/2017/02/15/CREC-2017-02-15-pt1-PgD160.htm

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--mods_path',
    #     help='S3 key or local file path to the mods.xml file for this date.',
    # )
    # parser.add_argument(
    #     '--date',
    #     help='Use the mods.xml file in S3 for this date.',
    #     type=lambda d: datetime.strptime(d, CMD_LINE_DATE_FORMAT),
    # )
    # parser.add_argument(
    #     '--crec_path',
    #     help='S3 key or local file path to crec .html file to parse.',
    # )
    # parser.add_argument(
    #     '--pg_host',
    #     help='Hostname for postgres database.',
    #     default='localhost',
    # )
    # parser.add_argument(
    #     '--pg_port',
    #     help='Hostname for postgres database.',
    #     default=5432
    # )
    # parser.add_argument(
    #     '--pg_user',
    #     help='Postgres user name.'
    # )
    # parser.add_argument(
    #     '--pg_password',
    #     help='Postgres password.'
    # )
