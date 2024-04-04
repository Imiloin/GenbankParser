from feature import Feature



class FeatureSet:
    '''
    Represents a set of features of one Genbank record.
    '''
    def __init__(self):
        self.features = {}

    def add_feature(self, feature: dict):
        self.features.update(feature)

    def get_features(self):
        return self.features
