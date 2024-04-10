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
pytest tests/test_fasta.py
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
    
    ????
    
    ```
