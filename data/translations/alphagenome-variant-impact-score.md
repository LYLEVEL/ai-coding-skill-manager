# 阿尔法基因组变异影响（AVI）分析

使用AlphaGenome变异影响（AVI）对遗传变异进行评分和优先排序
模型通过“脚本/脚本”alphagenome_atlas_avi.py。

> [!重要] **仅限研究使用及临床安全规则**：阿尔法基因组
> AVI 技能及其底层的AlphaGenome模型/图谱**纯属研究
>工具**。访问输出需要AlphaGenome API密钥，且该密钥受以下条件约束。
>禁止临床使用的服务。
>
> 1. **无医疗建议或临床诊断**：你**绝不能**提供
>医疗建议、临床诊断、疾病管理策略，或
>基于该技能或
>α基因组图谱。
> 2. **严格分子与功能框架**：高AVI分数反映
> **预测分子/功能影响**（例如，剪接中断，
>转录因子结合的改变，染色质可及性
>变更，或编码后果）。把所有发现都按分子层面来描述
>机制和生物学注释——绝不作为临床诊断或
>医学结论。
> 3. **无诊断飞跃**：绝不要对高功能影响外推
>临床疾病因果、渗透率或患者预后。如果
>问临床或诊断问题时，要明确说明
> AlphaGenome 是一个研究工具，答案应限制在预测范围内
>分子和功能效应。

> [!重要提示] **请始终使用AlphaGenome GENCODE v46 GTF
>（“scripts/alphagenome_atlas_avi.py gtf”）用于基因注释**：当
>检索基因模型、转录本ID、外显子坐标、CDS/UTR区域，或
>接头的供体/受体边界，**始终使用内置的
>“scripts/alphagenome_atlas_avi.py gtf”命令**。不要**不要**进行外部查询
> 来源（例如 Ensembl REST API、UCSC、外部 GTF 数据库或 NCBI）
>基因注释或转录坐标。这确保了注释
>匹配分数和网站。

--------------------------------------------------------------------------------

## 先修条件

使用“uv run”运行“脚本/alphagenome_atlas_avi.py”：

```bash
# Display CLI help:
uv run scripts/alphagenome_atlas_avi.py --help
```

> [!提示] **代理与程序执行格式**：调用CLI时
>代理工作流程，更倾向于使用“--格式json”或直接文件导出（'-o<file>'）
>用于确定性、结构化解析，而不是从中提取字段
>标准的折扣表。

### 1.查询变体（“查询”）

以基于1的“chr：pos：ref>alt”格式查询单一或多个变体以进行检查
评分及18个生物特征归因权重：

```bash
# Query single variant with basic feature importances (stdout JSON preview):
uv run scripts/alphagenome_atlas_avi.py query "chr9:128225994:G>A" --format json

# Query variant with exact underlying Atlas track indices, biosamples, and target genes:
uv run scripts/alphagenome_atlas_avi.py query "chr9:128225994:G>A" --include_track_info --format json

# Query multiple variants and export full track info to a file (prevents stdout overflow):
uv run scripts/alphagenome_atlas_avi.py query "chr9:128225994:G>A" "chr22:36201698:A>C" \
  --include_track_info --format json -o query_results.json
```

* **输出大小与重定向**：单一变体表/JSON查询紧凑
    （~1.0–1.5 KB）。查询$>3$变体或传递'--include_track_info
    --格式化json'（每个变体生成~3.9 KB），**始终导出
    直接访问文件**，使用“-o <file.json>”或“-o <file.tsv>”以避免
    超过上下文窗口限制。
* **典型运行时间**：每个变体约0.5–1.0秒（包括共计约12–15秒）
    环境启动）。单次叫>和$100$变体的比赛每分钟需$>1$。

### 2.注释与秩变体文件（“注释”）

用标准Ensembl VEP“CSQ”格式注释VCF（或CSV/TSV/Parquet）：

```bash
uv run scripts/alphagenome_atlas_avi.py annotate \
  --input test_data/example_variants.vcf \
  --output annotated_variants.vcf \
  --top_k 20 \
  --min_phred 15.0 \
  --top_output top_variants.json
```

* **输出大小与重定向**：“annotate”直接流传输完整呼号集
    通过“--输出”（'.vcf'、'.vcf.gz'、'.parquet'、'.tsv'、'.csv'）到磁盘。
    Stdout 显示有界总结（顶候选表 + 前三模态
    分解，~4.0–5.5 KB）。下游时使用“--top_output <file.json>”
    工具需要机器可读的顶选数据。
* **典型运行时和呼用集缩放**：吞吐量为~10个变体/秒
    （默认）和~5个变体（含赛道信息）。小呼号集（$\le 100$
    变体）取~15秒。调用集$\ge 500$变体静默执行，费用为$>1$
    分钟（例如，1000个变体耗时~2–3分钟;10,000个变体耗时~20分钟）。

### 3.饱和诱变窗口扫描（“区域”）

扫描一个基于1的封闭基因组窗口（“chr：start-end”）以获得所有可能的分数
单核苷酸取代（$3 \ 乘以 N$ 的变体，$N$-bP 窗口）：

```bash
uv run scripts/alphagenome_atlas_avi.py region \
  --region chr9:128225990-128226000 \
  --min_phred 15.0 \
  --top_k 20 \
  --output region_hotspots.tsv
```

* **输出大小与重定向**：扫描100 bp窗口产生300个SNV
    （~42 KB TSV / ~105 KB JSON），而1,000 bp窗口产生3,000 SNV
    （~421 KB TSV / ~1.06 MB JSON）。**始终注明'--输出
    用 <file.tsv|parquet>'** 保存完整数据集;stdout 只会显示一个
    前20名候选人预览。
* **典型运行时间**：查询在**1.5–3.0区间预计算gRPC密集得分
    S** 可兑换最多 1,000 个 bp（默认为“--max_window_size”）。

### 4.检查Atlas数据库元数据（“metadata”）

倾倒或搜索注册评分员、18个生物特征定义，或
实验曲目目录：

```bash
# List all registered scorers:
uv run scripts/alphagenome_atlas_avi.py metadata --scorers --format json

# List the 18 biological feature attribution modalities:
uv run scripts/alphagenome_atlas_avi.py metadata --features --format json

# Search experimental tracks by query keyword with a controlled preview (top 20):
uv run scripts/alphagenome_atlas_avi.py metadata --tracks --query "GATA1" --top_n 20

# Dump complete 9,440-track catalog to Parquet or TSV for offline search:
uv run scripts/alphagenome_atlas_avi.py metadata --tracks --output atlas_tracks.parquet
```

* **输出大小与重定向**：'--特征'（~1.3 KB）和'--计分员表
    （~1.7 KB）安全地低于4 KB。实验性曲目目录包含
    **9,440 轨道**（~972 KB 表 / ~2.55 MB JSON）。**绝不要未经过滤地倾倒
    向州立**的轨道;始终提供狭窄的“--查询”，指定“--top_n 20”，
    或导出为“--output atlas_tracks.parquet”。
* **典型时长**：~1.5–2.5秒。

### 5.检查基因结构与剪接连接（“gtf”）

查询GENCODE v46基因注释，提取基于1的外显子边界，满足
供体/受体坐标，并计算典范和外显子跳跃拼接
交汇坐标：

```bash
# Query MANE Select exon boundaries for a gene (stdout JSON preview):
uv run scripts/alphagenome_atlas_avi.py gtf --gene CAPN3 --exons --format json

# Query canonical and exon-skipping splice junctions for a variant locus:
uv run scripts/alphagenome_atlas_avi.py gtf --variant "chr15:42387805:C>G" --junctions --format json

# Extract CDS and UTR segments for an Ensembl transcript ID:
uv run scripts/alphagenome_atlas_avi.py gtf --transcript_id ENST00000397163.8 --cds --utr --format json
```

* **输出大小与重定向**：单基因MANE Select查询
    “--外显子”是紧致的
    （<2.5 KB）。** 始终导出为 '--output <file.tsv|parquet>' 或重定向 （'>
    当通过“--all_transcripts”（30–500）gtf_out.json
    KB），'--region'（$>50\text{ kb}$），'--格式json'，或用
    30美元>美元外显子（例如“TTN”、“DMD”）。
* **典型运行时间与内存**：导入318MB的GENCODE v46羽状数据集
    （~4.37 GB 内存）。缓存查询在**~4–6 s**内执行。冷启动运行
    从 GCS 下载文件时，在企业/云顶网络上获取 **~5–10 s**，
    但在外部网络上可能需要高达60–90秒的流量。不要扼杀这个过程
    在初次下载时过早。

--------------------------------------------------------------------------------

## 程序化 Python SDK 使用

在用 Python 程序化查询 AlphaGenome 时：

1. **客户端工厂**：始终实例化客户端
    'atlas.create（api_key）' — do **NOT** 实例化'atlas.AtlasClient（）'
    直接操作（这需要内部的 gRPC 存根）。
2. **坐标系**：“基因组。Interval' 在 **0 基半开时工作
    索引（'[开始，结束）'）。查询基于1的闭区间时
    'chr：start_1_based-end_1_based'，pass 'start = start_1_based - 1'，'end =
    end_1_based'。
3. **单一变异**：“基因组。Variant.from_str（“chr：pos：ref>alt”）' 期望
    **基于1的**位置坐标。

```python
import os
from alphagenome.atlas import atlas
from alphagenome.data import genome
import dotenv

dotenv.load_dotenv(os.path.expanduser('~/.env'))
client = atlas.create(os.environ['ALPHAGENOME_API_KEY'])

# Query 1-based closed interval chr11:5225727-5226575 using 0-based half-open [5225726, 5226575)
interval = genome.Interval(chromosome='chr11', start=5225726, end=5226575)
results = client.query_interval(
    interval,
    requested_scorers=['AVI_SCORE', 'AVI_SCORE_FEATURE_IMPORTANCE'],
)

# Query single variant with 1-based coordinate
variant = genome.Variant.from_str('chr11:5225488:A>T')
variant_scores = client.query_variant(
    variant,
    requested_scorers=['AVI_SCORE', 'AVI_SCORE_FEATURE_IMPORTANCE'],
)
```

--------------------------------------------------------------------------------

## 输出模式与响应结构

### 1.VCF CSQ 与信息标签结构（“注释”）

在编写带注释的VCF文件时，会注入以下注释：

* **Ensembl VEP 'CSQ' 格式字符串**：
    '等位基因|AVI_PHRED|AVI_RAW|AVI_QUANTILE|AVI_TOP_PERCENTILE|AVI_TOP_FEATURE'
* **子字段定义**：
    * “等位基因”（*字符串*）：替代等位基因碱基（例如 'A'）。
    * 'AVI_PHRED' （*float*）：校准的Phred影响分数（$\text{Phred} =
        -10 \cdot \log_{10}（1.0 - \text{quantile}）$）。范围：'[0.0， ~70.0]'。
        更高=功能影响更大。
    * 'AVI_RAW'（*float*）：原始连续模型预测。
    * 'AVI_QUANTILE'（*float*）：校准尾部分位数（$1 - \text{CDF}$）。
        范围：'（0.0， 1.0]'。
    * “AVI_TOP_PERCENTILE”（*浮动*）：全基因组SNV的顶尖百分位
        （$10^{-\text{Phred}/10} \乘以100\%$，例如“0.0380”代表Top 0.038%）。
    * 'AVI_TOP_FEATURE'（*字符串*）：主要贡献者的显示名称
        生物模态（例如“拼接”、“Alpha误解”、“ChIP-TF”，
        “DNASE-seq”、“Cactus”）。
* **独立信息标签**（除非是'--vep_csq_only'）： 'AVI_PHRED=浮动'，
    'AVI_RAW=浮点'，'AVI_QUANTILE=浮点'，'AVI_TOP_PERCENTILE=浮点'，
    “AVI_TOP_FEATURE=弦”。

### 2.表格和 JSON 记录模式（“query”、“region”、“--top_output”）

导出为 JSON、TSV、CSV 或 Parquet 的输出记录包含以下内容
场：

* 'Rank'（*整数*，出现在'--top_output'和'region'表格导出中）：
    基于1的候选人排名，按Phred递减排序。
* '变异'（*字符串*）：基因组变异字符串，位于'chr：pos_1_based：ref>alt'
    格式（例如'chr9：128225994：G>A'，其中坐标基于1）。
* '染色体'（*字符串*）：带有'chr'前缀的连体名称（例如'chr9'）。
*“位置”（*整数*）：基于1的基因组坐标。
* 'ref'（*字符串*）：参考等位基因碱基。
* 'alt'（*字符串*）：替代等位基因碱基。
* 'avi_phred'（*float*）：校准的Phred评分。
* 'avi_raw'（*float*）：原始连续模型评分。
* “avi_quantile”（*float*）：尾部分位数（$1 - \text{CDF}$）。
* 'top_percentile'（*float*）：精确的最高百分位值（例如，'0.3421'
    排名前0.34%）。
* 'top_modality'（*字符串*）：贡献最高的生物学者显示名称
    模态（例如“拼接”、“Alpha错义”、“ChIP-TF”）。
* 'top_feature_importance'（*float*）：归因权重（SHAP值）
    顶级模态。
* **可选归因权重（'-include_features'）**：18列
    'fi_<MODALITY>'（例如'fi_MERGED_SPLICING'，'fi_ALPHAMISSENSE'，
    “fi_MAX_ABS_RNA_SEQ”、“fi_CACTUS_241_WAY”）。
* **可选曲目来源（'--include_track_info'）**：
    “track_idx_<MODALITY>”，“track_name_<MODALITY>”，
    “track_biosample_<MODALITY>”、“<MODALITY>track_gene_”。

### 3.GTF 查询模式（“gtf”）

当用“gtf --format json”查询基因结构时，每个转录本对象
提供：

* **基因与文字记录元数据**：“gene_name”、“gene_id”、“transcript_id”，
    “transcript_type”、“染色体”、“开始”、“结束”、“链”、“is_mane_select”，
    “num_exons”（坐标为以1为基础的闭合）。
* **外显子阵列（'--exons'）**：
    * “exon_number”（*内译*）：基于1的外显子索引，转录本顺序为5'至3'。
    * '开始'， '结束'， '宽度'（*int*）：基于1的闭外显子坐标和
        长度以BP表示。
    * “受体”，“供体”（*内文*）：基于1基的5'接接接头和3'接头
        捐赠者坐标。
    * 'overlaps_variant'（*bool*）：如果查询变异重叠，则为真
        网站。
* **交汇数组（“--junctions”）**：
    * '类型'（*字符串*）：'典范内含子 {i}' 或 '外显子 {k} 跳跃'。
    * 'upstream_exon'， 'downstream_exon' （*内性*）：基于1的侧翼外显子
        数字按5'至3'的成绩单顺序排列。
    * 'junction_start'， 'junction_end'（*内文*）：基于1的基因组供体和
        接收器坐标。
    * 'intron_length'（*int*）：内含子长度以血压计。
    * 'score_id'（*字符串*）：构造图谱轨道比较标记。
    * 'atlas_url'（*字符串*）：可点击深度链接至Atlas赛道预测。
* **CDS 和 UTR 数组（'--cds'， '--utr'）**：基于1的闭合 'start'， 'end'，
    “宽度”（*int*）。

--------------------------------------------------------------------------------

## 评分指标与解读

* **AVI Phred**：校准分数（“Phred = -10 * log10（1.0 - 分位数）”）：
    * 'Phred >= 40'：** 预测影响前0.01%** 所有全基因组SNV的影响。
    * 'Phred >= 30'：**全基因组SNV预测影响前0.10%**。
    * 'Phred >= 20'：**预测前1.0%**所有全基因组SNV的影响预测。
    * 'Phred >= 15'：**预测影响前3.16%**所有全基因组SNV的影响。
    * 'Phred >= 10'：**全基因组SNV预测影响前10.0%**。
    * 'Phred < 10'：**所有全基因组SNV中排名最底90%**。
* **最高百分位**：全基因组SNV中，与 或
    更大影响力：“最高百分位 = 10^（-Phred/10） * 100%”（例如 Phred 29.7
    $\暗示$ 前0.11%。
* **顶级模态**：领先的生物特征归属（'元数据'）
    ——特征'）。

--------------------------------------------------------------------------------

## 可视化与图谱深度链接

> [!重要] **强制性图谱深度链接与变体分数**：每当
>报告、讨论或显示变异的AVI分数（无论是针对
>单一变异查询、排名候选表或基因组区域扫描），你
> **必须始终提供可点击的深度链接
> [α基因组图谱]（https://deepmind.google.com/science/alphagenome/atlas）**
每个变体都有>。

1. **用户上下文优先级**：始终优先考虑**用户上下文
    第一**（例如疾病、组织或相关细胞类型）。缺席时，使用
    “--include_track_info”与“query”一起发现驱动生物样本的细胞
    线路、本体库里和轨道索引。
2. **强制剪接与RNA-seq共绘规则**：每当绘制或
    可视化剪接变体，**始终绘制连续RNA-seq表达
    同时接入轨道（“SPLICE_JUNCTIONS”、“SPLICE_SITE_USAGE”，
    “SPLICE_SITES”）用于评估结构拼接断裂及其产生的影响
    转录丰度变化。
3. **图谱链接构建**：使用**'alphagenome-atlas-website-links'
    技能**（“脚本/alphagenome_atlas_links.py”）用于所有URL生成，
    布局配置（“lItems”）、生物样本过滤（“f”）以及
    “/atlas/track-predictions”比较图表链接。