# uniprot-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：UniProt 蛋白质序列与功能知识库：检索蛋白质功能描述、分类学、结构域标注、催化活性与翻译后修饰。
- **所属领域**：`生物与生命科学`
- **关联标签**：`UniProt、蛋白质序列、功能注释`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **UniProt** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **UniProt Database Access**
- **Prerequisites**
- **Overview**
- **Core Rules**
- **Use Cases**
- **Available Tools**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```text
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?protein ?name WHERE {
  ?protein a up:Protein ;
           up:sequence/rdf:value "SEQUENCE_HERE" .
  OPTIONAL {
    ?protein up:recommendedName/up:fullName ?name .
  }
}
```

```text
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?uniparc ?val WHERE {
  GRAPH <http://sparql.uniprot.org/uniparc> {
    ?uniparc a up:Sequence ;
             rdf:value ?val .
    FILTER (?val = "SEQUENCE_HERE")
  }
}
```

```text
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX taxon: <http://purl.uniprot.org/taxonomy/>
SELECT (COUNT(?protein) AS ?count) WHERE {
  ?protein a up:Protein ;
           up:reviewed true ;
           up:organism taxon:9606 .
}
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: Always use the provided Python scripts (e.g.,
- **No Hallucinations**: Do NOT invent protein functions, metadata, or
- **Notification**: If this skill is used, ensure this is mentioned in the
- **Searching for Protein Function**: Querying functional annotations, GO
- **Searching for Protein Sequence**: Searching for protein sequences by their
- **Understanding Protein/Organism Relationships**: Leveraging the Taxonomy
- **Large-Scale Metadata Retrieval**: Fetching annotations for thousands of
- **Sequence Discovery**: Finding orthologs or non-model proteins via UniParc.

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。