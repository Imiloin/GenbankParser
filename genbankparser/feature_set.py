from genbankparser.feature import Feature



class FeatureSet:
    def __init__(self):
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)

    def get_features(self):
        return self.features
