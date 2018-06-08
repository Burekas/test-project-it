from bson.objectid import ObjectId
from backend.app import utils
from string import Template


def test_json_encoder():
    first_id = ObjectId()
    second_id = ObjectId()
    test_obj = [{'_id': first_id}, {'_id': second_id}]
    # make sure that ObjectId's are converted to strings
    tpl = Template('[{"_id": "$first_id"}, {"_id": "$second_id"}]')
    expected = tpl.substitute(first_id=str(first_id), second_id=str(second_id))
    encoded = utils.JSONEncoder().encode(test_obj)
    assert expected == encoded
