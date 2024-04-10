import re
import json
import logging
from genbankparser.feature import Feature
import os


class Genbank(object):
    """
    A parser for Genbank files.
    """

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
    NO_SUB_STATES = (
        STATE_LOCUS,
        STATE_DEFINITION,
        STATE_ACCESSION,
        STATE_VERSION,
        STATE_DBLINK,
        STATE_KEYWORDS,
        STATE_COMMENT,
    )

    # indentations for different parts of the file
    GENBANK_INDENT = 12  # base indentation

    FEATURE_KEY_INDENT = 5
    FEATURE_QUALIFIER_INDENT = 21

    # regular expressions for parsing
    VARNAME = r"[a-zA-Z0-9_]+"
    FEATURE_KEY_SPACES = " " * FEATURE_KEY_INDENT
    FEATURE_QUALIFIER_SPACES = " " * FEATURE_QUALIFIER_INDENT

    FEATURE_START0 = r"{}({})\s+(\d+)\.\.(\d+)".format(FEATURE_KEY_SPACES, VARNAME)
    FEATURE_START0 = re.compile(
        FEATURE_START0
    )  # feature key, start, end (no complement)
    FEATURE_START1 = r"{}({})\s+complement\((\d+)\.\.(\d+)\)".format(
        FEATURE_KEY_SPACES, VARNAME
    )
    FEATURE_START1 = re.compile(FEATURE_START1)  # feature key, start, end (complement)
    FEATURE_QUALIFIER = r"{}/({})=(.+)".format(FEATURE_QUALIFIER_SPACES, VARNAME)
    FEATURE_QUALIFIER = re.compile(
        FEATURE_QUALIFIER
    )  # qualifier key, value (may be multiple lines)
    FEATURE_QUALIFIER_CONT = r"{}(.+)".format(FEATURE_QUALIFIER_SPACES)
    FEATURE_QUALIFIER_CONT = re.compile(
        FEATURE_QUALIFIER_CONT
    )  # continuation of a qualifier value

    def __init__(self, filepath, debug=False):
        self.locus = None
        self.definition = None
        self.accession = None
        self.version = None
        self.keywords = None
        self.comment = None
        self.reference = None
        self.dnlink = None
        self.length = 0

        # set up logging
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        self.filepath = filepath
        self.features = {}  # {locus_tag: FeatureList, ...}
        self.origin = None

        self.parse_state = self.STATE_INITIAL
        self.parse_annotation = False
        self._parse()

    def _parse(self):
        with open(self.filepath) as f:
            feature_type = None
            feature_location = None
            feature_qualifier_key = None
            feature_qualifier_value = None
            feature_qualifiers = {}
            for line in f:
                if line[0] != " ":  # state end, new state start
                    if self.parse_state in self.NO_SUB_STATES:
                        self._parse_nosub_info(self.parse_state, info)
                    self.parse_state = self.STATE_INITIAL

                # 无子项状态下，直接添加行内容到info记录中
                if self.parse_state in self.NO_SUB_STATES:
                    if line.isspace():
                        info += "\n"
                        continue

                    if line[self.GENBANK_INDENT : self.GENBANK_INDENT + 2] == "##":
                        # Annotation START/END
                        self.parse_annotation = not (self.parse_annotation)

                    if not (self.parse_annotation):
                        info += line[self.GENBANK_INDENT :].rstrip("\n") + " "
                    else:
                        info += line[self.GENBANK_INDENT :]
                    continue

                # 根据行首切换状态
                if line.startswith("LOCUS"):
                    self.parse_state = self.STATE_LOCUS
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("DEFINITION"):
                    self.parse_state = self.STATE_DEFINITION
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("ACCESSION"):
                    self.parse_state = self.STATE_ACCESSION
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("VERSION"):
                    self.parse_state = self.STATE_VERSION
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("DBLINK"):
                    self.parse_state = self.STATE_DBLINK
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("KEYWORDS"):
                    self.parse_state = self.STATE_KEYWORDS
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("COMMENT"):
                    self.parse_state = self.STATE_COMMENT
                    info = line[self.GENBANK_INDENT :].rstrip("\n") + " "
                elif line.startswith("REFERENCE"):
                    self.parse_state = self.STATE_REFERENCE
                    # to be implemented
                elif line.startswith("FEATURES"):
                    self.parse_state = self.STATE_FEATURES
                elif line.startswith("ORIGIN"):
                    # 先将最后一个feature添加到features中
                    # add last qualifier to the qualifiers dict
                    if feature_qualifier_key is not None:
                        feature_qualifiers[feature_qualifier_key] = (
                            feature_qualifier_value.strip('"')
                        )  # delete the leading and trailing double quotes
                    # add last feature to the features list
                    if feature_type is not None:
                        last_feature = Feature(
                            feature_type, feature_location, feature_qualifiers
                        )
                        if last_feature.get_locus_tag() in self.features:
                            self.features[last_feature.get_locus_tag()].append(
                                last_feature.convert_to_dict()
                            )
                        else:
                            self.features[last_feature.get_locus_tag()] = [
                                last_feature.convert_to_dict()
                            ]
                        feature_qualifier_key = None
                        feature_qualifiers = {}

                    self.parse_state = self.STATE_ORIGIN
                    continue

                if self.parse_state == self.STATE_REFERENCE:
                    # to be implemented
                    pass
                elif self.parse_state == self.STATE_FEATURES:
                    # check if the line is a new feature
                    match_feature_start0 = self.FEATURE_START0.match(line)
                    match_feature_start1 = self.FEATURE_START1.match(line)
                    if match_feature_start0 or match_feature_start1:
                        # add last qualifier to the qualifiers dict
                        if feature_qualifier_key is not None:
                            feature_qualifiers[feature_qualifier_key] = (
                                feature_qualifier_value.strip('"')
                            )  # delete the leading and trailing double quotes
                        # add last feature to the features list
                        if feature_type is not None:
                            last_feature = Feature(
                                feature_type, feature_location, feature_qualifiers
                            )
                            if last_feature.get_locus_tag() in self.features:
                                self.features[last_feature.get_locus_tag()].append(
                                    last_feature.convert_to_dict()
                                )
                            else:
                                self.features[last_feature.get_locus_tag()] = [
                                    last_feature.convert_to_dict()
                                ]
                            feature_qualifier_key = None
                            feature_qualifiers = {}

                        if match_feature_start0:
                            logging.debug(match_feature_start0.groups())
                            feature_type = match_feature_start0.group(1)
                            feature_location = (
                                int(match_feature_start0.group(2)),
                                int(match_feature_start0.group(3)),
                                False,
                            )
                            continue
                        elif match_feature_start1:
                            logging.debug(match_feature_start1.groups())
                            feature_type = match_feature_start1.group(1)
                            feature_location = (
                                int(match_feature_start1.group(2)),
                                int(match_feature_start1.group(3)),
                                True,
                            )
                            continue

                    # check if the line is a new feature qualifier
                    match_feature_qualifier = self.FEATURE_QUALIFIER.match(line)
                    if match_feature_qualifier:
                        # add last qualifier to the qualifiers dict
                        if feature_qualifier_key is not None:
                            feature_qualifiers[feature_qualifier_key] = (
                                feature_qualifier_value.strip('"')
                            )  # delete the leading and trailing double quotes
                        logging.debug(match_feature_qualifier.groups())
                        feature_qualifier_key = match_feature_qualifier.group(1)
                        feature_qualifier_value = match_feature_qualifier.group(2)
                        continue

                    # check if the line is a continuation of the last feature qualifier
                    match_feature_qualifier_cont = self.FEATURE_QUALIFIER_CONT.match(
                        line
                    )
                    if match_feature_qualifier_cont:
                        logging.debug(match_feature_qualifier_cont.groups())
                        if feature_qualifier_key == "translation":
                            feature_qualifier_value += (
                                match_feature_qualifier_cont.group(1)
                            )
                        else:
                            feature_qualifier_value += (
                                " " + match_feature_qualifier_cont.group(1)
                            )
                        continue
                elif self.parse_state == self.STATE_ORIGIN:
                    # to be implemented
                    pass

    def _parse_nosub_info(self, state: int, info: str):
        # 解析无子项的信息
        # 暂时不进行parse，只进行debug输出
        if state == self.STATE_LOCUS:
            logging.debug("Parsing LOCUS")
            logging.debug(info)
            locus_parts = info.split()  # 将info按空格分割为多个字段
            self.locus = locus_parts[0]
            self.length = int(locus_parts[1])
        elif state == self.STATE_DEFINITION:
            logging.debug("Parsing DEFINITION")
            logging.debug(info)
            self.definition = info.strip()
        elif state == self.STATE_ACCESSION:
            logging.debug("Parsing ACCESSION")
            logging.debug(info)
            self.accession = info.strip()
        elif state == self.STATE_VERSION:
            logging.debug("Parsing VERSION")
            logging.debug(info)
            self.version = info.strip()
        elif state == self.STATE_DBLINK:
            logging.debug("Parsing DBLINK")
            logging.debug(info)
            self.dblink = info.strip()
        elif state == self.STATE_KEYWORDS:
            logging.debug("Parsing KEYWORDS")
            logging.debug(info)
            self.keywords = info.strip()
        elif state == self.STATE_COMMENT:
            logging.debug("Parsing COMMENT")
            logging.debug(info)
            self.comment = info.strip()
        else:
            logging.error("Unknown state: {}".format(state))
        logging.debug("\n")

    def export_features_to_json(self):
        filename = os.path.basename(self.filepath)
        filename = os.path.splitext(filename)[0] + ".json"
        directory = os.path.dirname(self.filepath)
        export_path = os.path.join(directory, filename)

        with open(export_path, "w") as f:
            json.dump(self.features, f, indent=4)

    def __repr__(self):
        return "<Genbank file: {}>".format(self.filepath)
