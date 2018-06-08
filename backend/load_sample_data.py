#!/usr/bin/env python3

import argparse
import csv
from bson.objectid import ObjectId
from pymongo import MongoClient


class ImportCsv:
    '''Import data from csvfile into MongoDb database in tree structure with parent references'''

    def __init__(self, csvfile: str, database: str, collection: str, client: MongoClient):
        self.csvfile = csvfile
        self.db = client[database]
        self.collection = self.db[collection]
        self.insert_count = 0
        super().__init__()

    def _getid_or_insert(self, name: str, parent: ObjectId, extra_data: dict=None) -> ObjectId:
        # document data
        data = {'name': name, 'parent': parent}
        # add extra data if exists
        if extra_data:
            data.update(extra_data)
        # try to find
        document = self.collection.find_one(data, {'_id': 1})
        if not document:
            # insert new one and return ID
            self.insert_count += 1
            return self.collection.insert_one(data).inserted_id
        # Just return ID of existed document
        return document.get('_id')

    def run(self) -> None:
        ''' Run import'''
        print('Importing data...')
        # open file for reading
        with open(self.csvfile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # STANDARD
                # get_id or insert new standard
                standard_id = self._getid_or_insert(name=row.get('STANDARD'), parent=None)
                # GRADE
                # prepare name for grade
                grade = row.get('GRADE')
                grade_end = row.get('END_GRADE')
                is_grade_pk = grade.lower() == 'pk'
                grade_name = f'Grade {grade_end}' if is_grade_pk else f'Grade {grade}-{grade_end}'
                # get_id or insert new grade
                grade_id = self._getid_or_insert(name=grade_name, parent=standard_id)
                # LEARNING_DOMAIN
                learning_domain_id = self._getid_or_insert(name=row.get('LEARNING_DOMAIN'),
                                                           parent=grade_id)
                # TAG
                self._getid_or_insert(name=row.get('FULL_CODE'), parent=learning_domain_id,
                                      extra_data={'description': row.get('DESCRIPTION')})
        # create an index on parent field
        self.collection.create_index('parent')
        print(f'Inserted {self.insert_count} nodes\nDone.')


if __name__ == '__main__':
    # do not run when imported
    client = MongoClient('db', 27017)

    parser = argparse.ArgumentParser(description='Loads sample data into MongoDB database')
    parser.add_argument(
        'csvfile', nargs='?', default='sample_data/example-data.csv', help="path to csv file")
    parser.add_argument('database', nargs='?', default='testprojectdb', help='MongoDB database')
    parser.add_argument('collection', nargs='?', default='testcoll', help='MongoDB collection')
    args = parser.parse_args()
    ImportCsv(args.csvfile, args.database, args.collection, client).run()
