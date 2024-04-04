import re
import logging
from feature import Feature
from feature_set import FeatureSet



class Genbank(object):
    '''
    A parser for Genbank files.
    '''
    
    # add parse states
    STATE_INITIAL = 0
    STATE_LOCUS = STATE_INITIAL + 1
    STATE_DEFINITION = STATE_LOCUS + 1
    STATE_ACCESSION = STATE_DEFINITION + 1
    STATE_VERSION = STATE_ACCESSION + 1
    STATE_DBLINK = STATE_VERSION + 1
    STATE_KEYWORDS = STATE_DBLINK + 1
    STATE_SOURCE = STATE_KEYWORDS + 1
    STATE_REFERENCE = STATE_SOURCE + 1
    STATE_COMMENT = STATE_REFERENCE + 1
    STATE_FEATURES = STATE_COMMENT + 1
    STATE_ORIGIN = STATE_FEATURES + 1
    
    # 没有子项的状态
    NO_SUB_STATES = (STATE_LOCUS, STATE_DEFINITION, STATE_ACCESSION, STATE_VERSION, STATE_DBLINK, STATE_KEYWORDS)
    
    
    # indentations for different parts of the file
    GENBANK_INDENT = 12  # base indentation
    
    FEATURE_KEY_INDENT = 5
    FEATURE_QUALIFIER_INDENT = 21
    
    def __init__(self, filepath, debug=False):
        # set up logging
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        self.filepath = filepath
        self.records = []
        self.origin = None
        
        self.parse_state = self.STATE_INITIAL
        self._parse()

    def _parse(self):
        with open(self.filepath) as f:
            for line in f:
                if line[0] != ' ':  # state end
                    if self.parse_state in self.NO_SUB_STATES:
                        self._parse_nosub_info(self.parse_state, info)    
                    self.parse_state = self.STATE_INITIAL
                
                # 直接添加到记录中
                if self.parse_state in self.NO_SUB_STATES:
                    info += line[self.GENBANK_INDENT:].rstrip('\n') + " "
                    continue
                
                if line.startswith('LOCUS'):
                    self.parse_state = self.STATE_LOCUS
                    info = line[self.GENBANK_INDENT:].rstrip('\n') + " "
                elif line.startswith('DEFINITION'):
                    self.parse_state = self.STATE_DEFINITION
                    info = line[self.GENBANK_INDENT:].rstrip('\n') + " "
                elif line.startswith('ACCESSION'):
                    self.parse_state = self.STATE_ACCESSION
                    info = line[self.GENBANK_INDENT:].rstrip('\n') + " "
                elif line.startswith('VERSION'):
                    self.parse_state = self.STATE_VERSION
                    info = line[self.GENBANK_INDENT:].rstrip('\n') + " "
                elif line.startswith('DBLINK'):
                    self.parse_state = self.STATE_DBLINK
                    info = line[self.GENBANK_INDENT:].rstrip('\n') + " "
            
    def _parse_nosub_info(self, state: int, info: str):
        if state == self.STATE_LOCUS:
            logging.debug('Parsing LOCUS')
            logging.debug(info)
        elif state == self.STATE_DEFINITION:
            logging.debug('Parsing DEFINITION')
            logging.debug(info)
        elif state == self.STATE_ACCESSION:
            logging.debug('Parsing ACCESSION')
            logging.debug(info)
        elif state == self.STATE_VERSION:
            logging.debug('Parsing VERSION')
            logging.debug(info)
        elif state == self.STATE_DBLINK:
            logging.debug('Parsing DBLINK')
            logging.debug(info)
        elif state == self.STATE_KEYWORDS:
            logging.debug('Parsing KEYWORDS')
            logging.debug(info)
        else:
            logging.error('Unknown state: {}'.format(state))
        logging.debug('\n')
    
    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def __iter__(self):
        return iter(self.records)

    def __repr__(self):
        return '<Genbank file: {}>'.format(self.filepath)




# temp test, to be removed
if __name__ == '__main__':
    import os
    gb_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'sequence.gb')
    Genbank(gb_path, debug=True)
