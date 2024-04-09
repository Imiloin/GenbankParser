import pytest
from genbankparser.feature import Feature 

@pytest.fixture
def example_feature():
    return Feature(
        feature_type='gene',
        location=(1807, 2169, True),
        qualifiers={
            'gene': 'PAU8',
            'locus_tag': 'YAL068C',
            'product': 'seripauperin PAU8'
        }
    )

def test_feature_initialization(example_feature):
    assert example_feature.feature_type == 'gene'
    assert example_feature.location == (1807, 2169, True)
    assert example_feature.qualifiers == {
        'gene': 'PAU8',
        'locus_tag': 'YAL068C',
        'product': 'seripauperin PAU8'
    }

def test_get_type(example_feature):
    assert example_feature.get_type() == 'gene'

def test_get_location(example_feature):
    assert example_feature.get_location() == (1807, 2169, True)

def test_get_qualifiers(example_feature):
    assert example_feature.get_qualifiers() == {
        'gene': 'PAU8',
        'locus_tag': 'YAL068C',
        'product': 'seripauperin PAU8'
    }

def test_get_locus_tag(example_feature):
    assert example_feature.get_locus_tag() == 'YAL068C'

def test_get_locus_tag_default():
    # Testing default locus_tag value when it's not provided
    feature_without_locus_tag = Feature('mRNA', (100, 200, False), {'gene': 'PAU9'})
    assert feature_without_locus_tag.get_locus_tag() == 'UnknownLocustag'

def test_convert_to_dict(example_feature):
    assert example_feature.convert_to_dict() == {
        'type': 'gene',
        'location': (1807, 2169, True),
        'qualifiers': {
            'gene': 'PAU8',
            'locus_tag': 'YAL068C',
            'product': 'seripauperin PAU8'
        }
    }
