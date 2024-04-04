class Feature:
    '''
    Represents a single feature in a Genbank file.
    '''
    def __init__(self, feature_type, location, qualifiers):
        self.feature_type = feature_type  # gene, CDS, etc.
        self.location = location  # (int start, int end, bool complement)
        self.qualifiers = qualifiers  # {str key: str/int value}
