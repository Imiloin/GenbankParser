# GenbankParser

GenBank 是一个综合性的公共序列数据库，由美国国立生物技术信息中心（NCBI）维护，是生物信息学研究中最重要的数据库之一。

本项目构建了 `genbankparser` python package，可以解析 `.gb` 格式的 Genbank 文件，提取其中的特征，并输出相应的 FASTA 文件。



## Installation From Source Code

建议使用 python 3.8+ 版本。

#### Clone this repo

```bash
git clone https://github.com/Imiloin/GenbankParser.git
cd GenbankParser
```

#### Setup

```bash
pip install -e .
```

#### Run pytest

```bash
pytest tests/
```



## Usage

+ 读取一个 Genbank 文件，并导出其中的特征
    ```python
    from genbankparser.genbank import Genbank

    
    gb = Genbank(<path_to_genbank_file>)
    
    # 打印 Genbank 文件中的信息
    print(gb.locus)
    print(gb.definition)
    # ...
    print(gb.comment)
    
    # 导出 Genbank 文件中的特征为 json 格式
    gb.export_features_to_json()  # 在 Genbank 文件所在目录下生成一个 json 文件
    ```

+ 根据 Genbank 文件的内容，导出相应的 FASTA 文件
    ```python
    from genbankparser.fasta import Fasta

    
    fasta = Fasta(<path_to_genbank_file>)
    
    # 打印 Genbank 文件中的物种信息
    print(fasta.find_organism())
    
    # 打印 Genbank 文件中的染色体序号信息
    print(fasta.find_chromosome())
    
    ''' 
    打印 Genbank 文件中的dna序列信息，包括核酸序列在全序列上的定位、基因id、基因座id
    同时将这些信息保存到 `reduced_dna_info.txt` 中
    '''
    print(fasta.dna_info())
    
    # 打印 Genbank 文件中包含全核酸序列的行,同时将这些行保存到 `dna_filter.txt` 中
    print(fasta.find_dna_seq())
    
    # 提取 Genbank 文件中核酸序列行的碱基信息，打印碱基序列列表（nucleic_acid_list）
    print(fasta.nucleic_acid_list(<path_to_dna_filter.txt>))
    
    # 打印列表格式的 fasta 文件，同时创建 Genbank 文件的 fasta 格式文件
    print(fasta.fasta_file(<path_to_reduced_dna_info.txt>, <path_to_create_fasta_file>, nucleic_acid_list))
    
    # 直接根据 Genbank 文件创建 fasta 格式文件 `fasta_rev.txt`
    fasta = Fasta(<path_to_genbank_file>)
    ```
