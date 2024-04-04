class Feature:
    '''
    Represents a single feature in a Genbank file.
    '''
    def __init__(self, feature_type: str, location: tuple, qualifiers: dict):
        self.feature_type = feature_type  # gene, CDS, etc.
        self.location = location  # (int start, int end, bool complement)
        self.qualifiers = qualifiers  # {str key: str/int value, ...}
    
    def get_type(self):
        return self.feature_type
    
    def get_location(self):
        return self.location
    
    def get_qualifiers(self):
        return self.qualifiers

    def get_locus_tag(self):
        return self.qualifiers.get('locus_tag', 'Unknown')
    
    def convert_to_dict(self):
        return {'type': self.feature_type, 'location': self.location, 'qualifiers': self.qualifiers}
