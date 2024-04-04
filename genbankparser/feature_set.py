from feature import Feature
###### unused


class FeatureSet:
    '''
    Represents a list of features of one Genbank record.
    '''
    def __init__(self):
        self.featureset = []

    def add_feature(self, feature: dict):
        self.featureset.append(feature)

    def get_features(self):
        return self.featureset
