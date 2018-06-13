#!/usr/bin/env python3

import argparse
import csv
from bson.objectid import ObjectId
from pymongo import MongoClient


class ImportCsv:
    '''Import data from csvfile into MongoDb database in tree structure with parent references'''

    field_ignore = ('END_GRADE', 'DESCRIPTION')

    @property
    def field_map(self):
        ''' Map special fields to processors'''
        return {
            'GRADE': self._get_grade_doc,
            'FULL_CODE': self._get_tag_doc
        }

    def __init__(self, csvfile: str, database: str, collection: str, client: MongoClient):
        self.csvfile = csvfile
        self.db = client[database]
        self.collection = self.db[collection]
        self.insert_count = 0
        super().__init__()

    def _prepare_node_doc(self, field_name, row):
        if field_name in self.field_map:
            return self.field_map.get(field_name)(row)
        return {'name': row.get(field_name)}

    def _get_grade_doc(self, row):
        grade = row.get('GRADE')
        grade_end = row.get('END_GRADE')
        is_grade_pk = grade.lower() == 'pk'
        grade_name = f'Grade {grade_end}' if is_grade_pk else f'Grade {grade}-{grade_end}'
        return {'name': grade_name}

    def _get_tag_doc(self, row):
        return {'name': row.get('FULL_CODE'),
                'description': row.get('DESCRIPTION')}

    def _getid_or_insert(self, new_doc: dict, parent: ObjectId) -> ObjectId:
        new_doc.update({'parent': parent})
        document = self.collection.find_one(new_doc, {'_id': 1})
        if not document:
            # insert new one and return ID
            self.insert_count += 1
            return self.collection.insert_one(new_doc).inserted_id
        # Just return ID of existed document
        return document.get('_id')

    def run(self) -> None:
        ''' Run import'''
        print('Importing data...')
        # open file for reading
        with open(self.csvfile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # set parent to None for new row
                parent = None
                for key in row.keys():
                    if key in self.field_ignore:
                        continue
                    doc = self._prepare_node_doc(key, row)
                    parent = self._getid_or_insert(new_doc=doc, parent=parent)
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
