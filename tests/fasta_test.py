import pytest
from fasta import Fasta

my_instance = Fasta('sequence.gb')        # 创建Fasta()实例

def test_organism():
    result = my_instance.find_organism()
    assert result == 'Saccharomyces cerevisiae S288C'

def test_chromosome():
    result = my_instance.find_chromosome()
    assert result == 'chromosome I'

def test_dna_info():
    result_list = my_instance.dna_info()
    sliced_list = result_list[:3] + result_list[-3:]        # 由于原结果过长，难以编写test期望答案，故进行头尾切割
    test_list = ['complement(1807..2169)\n', 'gene PAU8\n', 'locus YAL068C\n', '225460..226863\n', 'gene PHO11\n', 'locus YAR071W\n']
    assert sliced_list == test_list

def test_find_seq():
    result_list = my_instance.find_dna_seq()
    sliced_list = result_list[:1] + result_list[-1:]        # 由于原结果过长，难以编写test期望答案，故进行头尾切割
    test_list = ['        1 ccacaccaca cccacacacc cacacaccac accacacacc acaccacacc cacacacaca', '   230161 ggtgtgggtg tgggtgtggt gtggtgtgtg ggtgtggtgt gggtgtggtg tgtgtggg']
    assert sliced_list == test_list

def dna_list():
    result_list = my_instance.nucleic_acid_list('dna_filter.txt')
    sliced_list = result_list[:10] + result_list[-10:]
    test_list = ['c', 'c', 'a', 'c', 'a', 'c', 'c', 'a', 'c', 'a', 't', 'g', 't', 'g', 't', 'g', 't', 'g', 'g', 'g']
    assert sliced_list == test_list