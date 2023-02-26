from Django_AT.AT.dashboard.utils import merge_dicts

def test_merge_dicts():
    # Test with empty list
    assert merge_dicts([]) == {}

    # Test with one dictionary
    input_list = [{'a': 1, 'b': 2}]
    expected_output = {'a': [1], 'b': [2]}
    assert merge_dicts(input_list) == expected_output

    # Test with multiple dictionaries
    input_list = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
    expected_output = {'a': [1, 3], 'b': [2, 4]}
    assert merge_dicts(input_list) == expected_output

    # Test with missing keys
    input_list = [{'a': 1, 'b': 2}, {'b': 4}]
    expected_output = {'a': [1, None], 'b': [2, 4]}
    assert merge_dicts(input_list) == expected_output

    # Test with extra keys
    input_list = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4, 'c': 5}]
    expected_output = {'a': [1, 3], 'b': [2, 4], 'c': [None, 5]}
    assert merge_dicts(input_list) == expected_output
