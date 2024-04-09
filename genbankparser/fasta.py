import os
import re

class Fasta:
    # 把genbank格式的文件转换为FASTA格式，其中信息栏包括基因座ID，核酸序列始末位置（c表示互补链），物种信息及染色体序号，最后得到的结果位于`fasta_rev.txt`中
    def __init__(self, file_path):
        self.file_path = file_path
        self.dir_path = os.path.dirname(os.path.abspath(file_path))
        self.find_dna_seq()
        self.dna_info()
        self.organism = self.find_organism()
        self.chromosome = self.find_chromosome()
        script_path = os.path.abspath(file_path)        # sequence.gb地址
        dir_path = os.path.dirname(script_path)     # sequence.gb上级目录地址
        fasta_path = f'{dir_path}/fasta.txt'        # FASTA格式的文件，但信息行和核酸序列顺序颠倒
        fasta_rev_path = f'{dir_path}/fasta_rev.txt'        # 信息行和核酸序列顺序正常的FASTA文件（最终结果，除此结果外其他文件不会输出）
        filter_path = f'{dir_path}/dna_filter.txt'      # 筛选原genbank文件中的整段核酸序列，保存进文件
        reduced_path = f'{dir_path}/reduced_gene_info.txt'      # 存储gene相关信息，且去除重复行

        nucleic_acid = self.nucleic_acid_list(filter_path)       # 用于按顺序保存所有核酸信息，一个base作为一个元素
    
        self.fasta_file(reduced_path, fasta_path, nucleic_acid)
        
        with open(fasta_path, 'r') as f:
            with open(fasta_rev_path, 'w') as rev:
                tmp = ''        # 保存核酸序列行，将前后两行进行对换
                for line in f:
                    if tmp:
                        rev.write(line + '\n')
                        rev.write(tmp + '\n')
                        tmp = ''
                    else:
                        tmp = line
        
        os.remove(fasta_path)
        os.remove(filter_path)
        os.remove(reduced_path)
    
    def find_organism(self):
        """从`sequence.gb`中找到匹配的物种名称，显示于fasta格式文件中信息行"""
        file_path = self.file_path
        organism_pat = '(?<=ORGANISM\s{2}).+$'
        organism_repat = re.compile(organism_pat)
        with open(file_path, 'r') as f:
            org = ''
            for line in f:
                search = organism_repat.search(line)
                if search:
                    org = search.group()
            return org
    
    def find_chromosome(self):
        """从`sequence.gb`中找到匹配的染色体序号，显示于fasta格式文件中信息行"""
        file_path = self.file_path
        chromosome_pat = 'chromosome\s\w'
        chromosome_repat = re.compile(chromosome_pat)
        with open(file_path, 'r') as f:
            first_line = f.readline()
            second_line = f.readline()
            search = chromosome_repat.search(second_line)
            if search:
                chromo = search.group()
                return chromo
            else:
                return None
    
    def dna_info(self):
        """从`sequence.gb`中找到dna信息，包括序列定位，gene，locus_tag等，删除重复，保存于reduced_gene_info.txt文件中，返回列表中每行信息为一个元素"""
        file_path = self.file_path       # 找到位于同一目录下的`sequence.gb`文件
        gene_info_path = f'{self.dir_path}/gene_info.txt'
        with open(file_path, 'r') as f:
            with open(gene_info_path, 'w') as dna_info:
                info_position_pat = '(?<=gene\s{12})(complement\()?\d+\.{2}\d+(\))?'        # 匹配gene的位置信息
                info_position_repat = re.compile(info_position_pat)
                info_name_pat = '(?<=\/gene=")\w+(?=")'     # 匹配gene的gene_name信息
                info_name_repat = re.compile(info_name_pat)
                info_locus_pat = '(?<=\/locus_tag=")\w+-?\w+(?=")'       # 匹配gene的locus_tag信息
                info_locus_repat = re.compile(info_locus_pat)
                for line in f:
                    line = line.rstrip()
                    search1 = info_position_repat.search(line)
                    if search1:
                        matched_content = search1.group()
                        dna_info.write(matched_content + '\n')
                    search2 = info_name_repat.search(line)
                    if search2:
                        matched_content = search2.group()
                        dna_info.write('gene ' + matched_content + '\n')
                    search3 = info_locus_repat.search(line)
                    if search3:
                        matched_content = search3.group()
                        dna_info.write('locus ' + matched_content + '\n')

        # 由于gene_name和locus_tag存在重复，创建`reduced_gene_info`文件，去除`gene_info`中的重复行
        reduced_path = f'{self.dir_path}/reduced_gene_info.txt'
        recent_lines = []
        result = []
        with open(gene_info_path, 'r') as f:
            with open(reduced_path, 'w') as reduced_info:
                for line in f:
                    if line not in recent_lines:
                        reduced_info.write(line)
                        result.append(line)
                    
                    if recent_lines.count(line.rstrip()) < 3:
                        recent_lines.append(line)
                    else:
                        recent_lines.pop(0)
                        recent_lines.append(line)
        
        os.remove(gene_info_path)
        return result

    def find_dna_seq(self):
        """从`sequence.gb`中找到整段核酸序列信息，并保存于dna_filter.txt文件中，返回列表中源文件每一行为一个元素"""
        file_path = self.file_path       # 找到位于同一目录下的`sequence.gb`文件
        filter_path = f'{self.dir_path}/dna_filter.txt'      # 在相同目录下创建`dna_filter.txt`，用于保存genbank文件末尾的一长串核酸序列
        result = []
        with open(file_path, 'r') as f:
            with open(filter_path, 'w') as dna_filter:
                dna_seq_pat = '\d+(\s[atcg]{10})+'
                repat_dna_seq = re.compile(dna_seq_pat)
                for line in f:
                    line = line.rstrip()
                    search = repat_dna_seq.search(line)
                    if search:
                        dna_filter.write(line + '\n')
                        result.append(line)
        return result
    
    def nucleic_acid_list(self, path):
        """将dna序列中的每个碱基作为一个元素保存于列表中，:param:path为从源文件中提取的整段核酸序列信息的文件地址，返回核酸列表"""
        nucleic_acid = []       # 用于按顺序保存所有核酸信息，一个base作为一个元素
        filter_path = path
        with open(filter_path, 'r') as f:
            nucleic_pat = '([actg]+\s)+[atcg]*$'
            nucleic_repat = re.compile(nucleic_pat)
            for line in f:
                line = line.rstrip()
                search_nucleic = nucleic_repat.search(line)
                if search_nucleic:
                    matched_content = search_nucleic.group()
                    for char in matched_content:
                        if char != ' ':     # 去除原文件中的空格
                            nucleic_acid.append(char)
        return nucleic_acid
    
    def fasta_file(self, path1, path2, nucleic_acid):
        """将已有信息写为fasta格式，写入fasta.txt文件中，:param:path1为核酸序列信息文件，:param:path2为所要书写的fasta文件地址，返回列表中fasta.txt的每一行作为一个元素，此函数输出次序中核酸序列行和信息行将互换，需后续操作"""
        with open(path1, 'r') as f:
            with open(path2, 'w') as fas:
                locus_pat = '(?<=locus\s)\w+'       # 匹配locus_tag
                locus_repat = re.compile(locus_pat)
                position_pat1 = '(?<=complement\()\d+\.{2}\d+'      # 匹配互补链（complement）的核酸定位信息
                position_pat2 = '\d+\.\.\d+'        # 匹配非互补链的核酸定位信息
                position_repat1 = re.compile(position_pat1)
                position_repat2 = re.compile(position_pat2)
                info = []
                result = []
                for line in f:
                    search_pat1 = position_repat1.search(line)
                    search_pat2 = position_repat2.search(line)
                    search_locus = locus_repat.search(line)
                    if search_pat1:
                        matched_content = search_pat1.group()
                        num1_pat = '\d+(?=\.\.)'        # 匹配核酸定位信息中的第一个数字
                        num2_pat = '(?<=\.\.)\d+'       # 匹配核酸定位信息中的第二个数字
                        num1_repat = re.compile(num1_pat)
                        num2_repat = re.compile(num2_pat)
                        search1 = num1_repat.search(line)
                        num1 = int(search1.group())
                        search2 = num2_repat.search(line)
                        num2 = int(search2.group())
                        info.append(f"c{num1}-{num2}")      # 信息行中写入定位信息
                        tmp = nucleic_acid[num1-1:num2]     # 在全部核酸信息list中进行切割
                        tmp.reverse()       # 反向
                        tmp_str = ''.join(tmp)
                        table = str.maketrans('atcg', 'tagc')       # 互补
                        sequence = tmp_str.translate(table)
                        fas.write(sequence)
                        result.append(sequence)
                    elif search_pat2:
                        matched_content = search_pat2.group()
                        num1_pat = '\d+(?=\.\.)'        # 匹配核酸定位信息中的第一个数字
                        num2_pat = '(?<=\.\.)\d+'       # 匹配核酸定位信息中的第二个数字
                        num1_repat = re.compile(num1_pat)
                        num2_repat = re.compile(num2_pat)
                        search1 = num1_repat.search(line)
                        num1 = int(search1.group())
                        search2 = num2_repat.search(line)
                        num2 = int(search2.group())
                        info.append(f"{num1}-{num2}")       # 信息行中写入定位信息
                        tmp = nucleic_acid[num1-1:num2]     # 在全部核酸信息list中进行切割
                        sequence = ''.join(tmp)
                        fas.write(sequence)
                        result.append(sequence)
                    if search_locus:
                        matched_content = search_locus.group()      # 得到locus_tag
                        info.insert(0, '>')
                        info.insert(1, f"{matched_content}:")
                        info.append(f'\t[organism={self.organism}]\t[chromosome={self.chromosome}]')
                        info_line = ''.join(info)       # 更新信息行中的locus，organism，chromosome信息
                        fas.write('\n' + info_line + '\n')      # 信息行写入
                        result.append(info_line)
                        info = []       # 信息行清空
        return result