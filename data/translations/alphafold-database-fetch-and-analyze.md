# AlphaFold数据库：取用与分析

## 先修条件

1. **'uv'**：阅读“uv”技能并按照其设置说明操作以确保
    'uv'已安装并运行在PATH上。
2. **用户通知**：如果
    .licenses/alphafold_database_fetch_and_analyze_LICENSE.txt 目前还没有
    存在于工作区根目录中，然后（1）显著地通知用户
    要检查 https://alphafold.ebi.ac.uk/ 的条款，然后（2）创建文件
    记录通知文本和时间戳。

## 概述

下载 AlphaFold 预测结构（mmCIF）和预测比对误差
（PAE）矩阵来自AlphaFold数据库中给定UniProt ID的矩阵，然后执行
结构置信度（pLDDT）的自动启发式分析，内在
无序区域、刚性领域边界以及域间灵活性。

** 不要在 / /

- 用户仅拥有蛋白质名称、基因名或氨基酸序列（无）
    UniProt ID）——让他们在 ID 上查找
    [单一塑料]（https://www.uniprot.org 年）。
- 用户想搜索结构同源物（使用**Foldseek**）。
- 用户希望对自定义序列运行AlphaFold预测。
- 用户需要实验性的PDB结构（使用**RCSB PDB**）。

## 核心规则

- **使用包装器**：始终执行提供的辅助脚本以查询
    数据库，而不是直接访问数据库。剧本
    自动优雅地执行所需的费率限制。
- 不尝试计算领域边界或评估结构无序
    你自己;始终依赖脚本提供的输出。
- 如果使用该技能，确保在输出中提及。

## 实用脚本

**1.获取结构文件**

下载“.cif”结构文件、“_predicted_aligned_error.json”和API
用于UniProt ID的元数据JSON（“-metadata.json”）。处理分段回退
非常大的蛋白质。

示例：

```bash
uv run scripts/fetch_structure.py P00520 -o /path/to/output/
uv run scripts/fetch_structure.py P04637 -o /path/to/custom_results/
```

始终指定“-o”，并表示绝对路径或相对于用户的路径
项目根，绝不会是相对于技能目录的路径。

**2.分析pLDDT信心**

从保存的AFDB元数据JSON文件（由
“fetch_structure.py”）并打印启发式置信度评估（结构化，
混乱，混合）。

示例：

```bash
uv run scripts/analyze_plddt.py ./data/AF-P00520-F1-metadata.json
```

**3.分析PAE / 领域边界**

读取下载的PAE JSON文件，并使用一个
滑动窗口PAE启发式。

示例：

```bash
uv run scripts/analyze_pae.py ./data/AF-P00520-F1-predicted_aligned_error_v6.json
```

## 解读输出

剧本会打印分析到标准。仔细阅读并综合
用户结果：

1. **异构体 / 大蛋白警告（强制）:** 检查脚本输出
    任何“[！]警告行。如果脚本报告没有正史条目
    如果发现并使用了异构体，或者如果蛋白质非常大（>2700 AAs），
    你**必须**显著地向用户传达此警告。不要遗漏这一点
    警告。
2. **综合结构分析**：结合“pLDDT结论”和
    将“PAE结构结论”整理成一个统一的整体摘要。
    描述蛋白质的整体折叠信度，即
    无序区域及其刚性结构域布局。
3. 突出支持指标：
    - 整体pLDDT及分数置信度的崩溃
        （尤其是非常低和非常高的区别）。
    - 领域边界分析（不同全局域及其数量
        特定残基范围）。
4. **显性障碍警告：** 如果分析得出蛋白质为
    高度内在紊乱（例如，高比例<50 pLDDT，或缺乏
    刚性域），发出单独且显著的警告。建议用户不要这样做
    继续进行全蛋白下游结构分析（如Foldseek）
    或对接）。如果在无序中存在小有序结构域，请告知
    用户可严格限制未来分析仅限于这些特定残基
    界限。
5. 提醒用户，每个残基pLDDT嵌入在的B因子列中
    下载的 mmCIF 文件。