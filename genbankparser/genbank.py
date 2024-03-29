from feature import Feature
from feature_set import FeatureSet



class Genbank(object):
    def __init__(self, filename):
        self.filename = filename
        self.records = []
        self.origin = None
        self._parse()

    def _parse(self):
        with open(self.filename) as f:
            pass
            

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def __iter__(self):
        return iter(self.records)

    def __repr__(self):
        return '<Genbank file: {}>'.format(self.filename)
