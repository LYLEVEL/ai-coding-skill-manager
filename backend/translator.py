# -*- coding: utf-8 -*-
"""
中文概要与本地映射字典
针对 Antigravity 官方技能、常用工作流及生信/科研插件，提供 100% 纯正详尽的中文功能概要、分类与标签
"""

BUILTIN_CHINESE_DICT = {
    # ==================== 1. 软件工程与敏捷工作流 (Superpowers Suite) ====================
    "brainstorming": {
        "summary": "头脑风暴与需求探索：在开发新功能或组件前，深入挖掘用户意图、澄清需求并形成设计共识。",
        "category": "需求与规划",
        "tags": ["头脑风暴", "需求分析", "系统设计"]
    },
    "writing-plans": {
        "summary": "编写分步实施计划：将需求规格转化为颗粒度明确、支持测试驱动与逐步落地的工程实施计划。",
        "category": "需求与规划",
        "tags": ["实施计划", "架构规划", "步骤拆解"]
    },
    "executing-plans": {
        "summary": "执行实施计划：按步骤加载并严格执行计划文件中的任务，并在关键节点进行自检与审查。",
        "category": "代码开发",
        "tags": ["计划执行", "自动化落地", "检查点"]
    },
    "subagent-driven-development": {
        "summary": "子智能体协同开发：分派独立的轻量子智能体并行或逐步完成计划任务，高效迭代与阶段性审查。",
        "category": "代码开发",
        "tags": ["子智能体", "并行开发", "自动化审查"]
    },
    "dispatching-parallel-agents": {
        "summary": "并行智能体分发：当面对两个以上互不依赖的独立任务时，调度多个子智能体并发执行加速产出。",
        "category": "代码开发",
        "tags": ["并发任务", "多智能体", "任务分发"]
    },
    "test-driven-development": {
        "summary": "测试驱动开发（TDD）：在编写业务实现代码之前，先编写失败测试用例，确保红绿重构流程严谨。",
        "category": "质量保证",
        "tags": ["TDD", "单元测试", "测试驱动"]
    },
    "systematic-debugging": {
        "summary": "系统化缺陷调试：遇到任何 Bug 或测试报错时，遵循科学归因流程系统排查根因，杜绝盲目修改。",
        "category": "调试与维护",
        "tags": ["系统排错", "根因分析", "缺陷定位"]
    },
    "verification-before-completion": {
        "summary": "完成前全项验证：在声明任务完成或提交代码前，执行严格的构建测试验证，以证据说话。",
        "category": "质量保证",
        "tags": ["质量验收", "构建验证", "提测把关"]
    },
    "requesting-code-review": {
        "summary": "发起代码审查：在阶段性交付或合并前自动组织评审清单，严格自检关键逻辑与代码坏味道。",
        "category": "代码开发",
        "tags": ["Code Review", "代码规范", "安全审查"]
    },
    "receiving-code-review": {
        "summary": "接收代码评审反馈：审慎评估审查意见与修改建议，确保技术合理性而非盲目采纳。",
        "category": "代码开发",
        "tags": ["审查处理", "技术复核", "代码改进"]
    },
    "using-git-worktrees": {
        "summary": "Git Worktree 隔离工作区：创建独立的工作树隔离特性开发环境，避免分支污染与工作区冲突。",
        "category": "版本控制",
        "tags": ["Git", "Worktree", "多分支隔离"]
    },
    "finishing-a-development-branch": {
        "summary": "分支收尾与集成：特性分支完工后，引导规范的分支合并、PR 创建或干净的工作树清理。",
        "category": "版本控制",
        "tags": ["分支合并", "PR提交", "工作流收尾"]
    },
    "to-prd": {
        "summary": "对话沉淀为 PRD：将当前的讨论记录与业务逻辑沉淀整理为标准产品需求文档（PRD）并归档。",
        "category": "需求与规划",
        "tags": ["PRD输出", "需求沉淀", "产品文档"]
    },
    "healing-prd-agent": {
        "summary": "PRD 需求孵化器：将用户模糊的初步想法转化为完备的交互规格说明书、原型与开发指令。",
        "category": "需求与规划",
        "tags": ["PRD撰写", "产品原型", "需求提炼"]
    },
    "workflow-skill-creator": {
        "summary": "工作流技能提炼器：将刚刚完成的会话操作流程自动萃取、总结并封装为可复用的新 Skill 规范。",
        "category": "核心基础",
        "tags": ["技能提炼", "流程沉淀", "复用封装"]
    },

    # ==================== 2. Antigravity 平台核心与生态配置 ====================
    "using-superpowers": {
        "summary": "技能调度总线：会话启动时的基石技能，规范智能体如何检索、激活与调用技能库。",
        "category": "核心基础",
        "tags": ["技能调度", "基石核心", "调度规范"]
    },
    "agy-customizations": {
        "summary": "Antigravity 自定义规范指引：全方位解释技能、规则、插件、Hooks 与 MCP 的加载机制与开发标准。",
        "category": "核心基础",
        "tags": ["官方指南", "扩展机制", "规则配置"]
    },
    "antigravity-guide": {
        "summary": "Antigravity 综合使用手册：包含 CLI 工具、IDE 快捷键、斜杠命令与 Python SDK 快速参考。",
        "category": "核心基础",
        "tags": ["使用指南", "快捷指令", "IDE扩展"]
    },
    "antigravity_guide": {
        "summary": "Antigravity 综合使用手册：包含 CLI 工具、IDE 快捷键、斜杠命令与 Python SDK 快速参考。",
        "category": "核心基础",
        "tags": ["使用指南", "快捷指令", "IDE扩展"]
    },
    "writing-skills": {
        "summary": "技能规范编写器：指导开发符合 Antigravity 规范的新 Skill，包含元数据结构、提示词设计与测试验证。",
        "category": "核心基础",
        "tags": ["Skill创建", "提示词工程", "扩展开发"]
    },
    "migrate-workflows": {
        "summary": "工作流迁移转换器：将旧版遗留的自动化 workflows 自动无损升级为新版 Antigravity Skill 标准。",
        "category": "核心基础",
        "tags": ["平滑迁移", "版本升级", "工作流重构"]
    },
    "automation": {
        "summary": "后台定时自动化向导：指导设计、创建和调度 Antigravity 后台定时任务（Cron）与周期作业。",
        "category": "核心基础",
        "tags": ["定时任务", "后台守护", "自动化调度"]
    },
    "permissioned-github": {
        "summary": "GitHub 权限合规交互：在与 GitHub 进行写入、创建 PR 或敏感仓库操作时提供安全审批指引。",
        "category": "版本控制",
        "tags": ["GitHub", "权限合规", "代码推送"]
    },
    "plugin": {
        "summary": "插件包开发与管理：指导创建、打包与发布包含规则、技能和 MCP 配置的命名空间插件包。",
        "category": "核心基础",
        "tags": ["插件机制", "扩展包", "命名空间"]
    },
    "credentials": {
        "summary": "API 凭证安全配置向导：规范处理与验证各平台 API 密钥与凭据，保障私密信息不外泄。",
        "category": "安全配置",
        "tags": ["API密钥", "凭证管理", "安全合规"]
    },
    "uv": {
        "summary": "uv 高性能包管理器检测器：检测并自动安装配置 Python 极速包管理器 uv，确保依赖链路可用。",
        "category": "开发环境",
        "tags": ["Python", "uv", "环境配置"]
    },
    "android-cli": {
        "summary": "Android CLI 工具链：辅助进行安卓应用工程创建、模拟器管理、设备截图与官方 SDK 交互。",
        "category": "移动开发",
        "tags": ["Android", "移动端", "模拟器交互"]
    },

    # ==================== 3. 前端与界面设计 (UI Design) ====================
    "frontend-design": {
        "summary": "高质感前端界面设计：生成精致、生产级的前端 Web 组件与页面，告别千篇一律的粗糙 AI 审美。",
        "category": "前端与可视化",
        "tags": ["前端工程", "TailwindCSS", "高级设计"]
    },
    "generative_ui": {
        "summary": "交互式生成式 UI：在聊天或独立视窗中渲染丰富的 HTML/图表/可交互组件与数据可视化视窗。",
        "category": "前端与可视化",
        "tags": ["组件生成", "图表可视化", "动态UI"]
    },
    "canvas-ui": {
        "summary": "Canvas/WebGL 创意动效：提供流体、玻璃拟态、粒子、故障风等 24 种 WebGL 创意视觉特效。",
        "category": "前端与可视化",
        "tags": ["WebGL", "动效粒子", "视觉特效"]
    },
    "cozy-pastel-ui-design": {
        "summary": "温馨治愈系 UI 风格：以柔和圆润、治愈自然、立体微触感为特色的 React 界面与组件设计套件。",
        "category": "前端与可视化",
        "tags": ["治愈风格", "柔和圆润", "React组件"]
    },
    "cozy_ui_design": {
        "summary": "温馨治愈系 UI 风格：以柔和圆润、治愈自然、立体微触感为特色的 React 界面与组件设计套件。",
        "category": "前端与可视化",
        "tags": ["治愈风格", "柔和圆润", "React组件"]
    },

    # ==================== 4. 学术文献与知识探索 (Literature) ====================
    "literature-search-arxiv": {
        "summary": "arXiv 预印本学术文献检索：搜索计算机、物理、数学等最新科研论文元数据、摘要并下载全文 PDF。",
        "category": "学术检索",
        "tags": ["arXiv", "预印本", "论文检索"]
    },
    "literature-search-biorxiv": {
        "summary": "bioRxiv / medRxiv 生物医学预印本搜索：按学科分类与时间段精准筛选生命科学与医学前沿预印本论文。",
        "category": "学术检索",
        "tags": ["bioRxiv", "医学预印本", "文献下载"]
    },
    "literature-search-europepmc": {
        "summary": "Europe PMC 欧洲医学文献库检索：检索生命科学文献、获取开放获取（OA）全文 XML/文本并分析引用链。",
        "category": "学术检索",
        "tags": ["EuropePMC", "医学文献", "开放获取"]
    },
    "literature-search-openalex": {
        "summary": "OpenAlex 全球学术知识图谱：跨学科检索学术论文、学者影响力（H指数）、科研机构与全球引用网络。",
        "category": "学术检索",
        "tags": ["OpenAlex", "学术图谱", "引用统计"]
    },
    "pubmed-database": {
        "summary": "PubMed 生物医学文献库：检索生物医学研究与临床试验论文，抓取摘要全文，并与基因/化合物数据库交叉互联。",
        "category": "学术检索",
        "tags": ["PubMed", "生物医学", "临床文献"]
    },
    "predictingthepast": {
        "summary": "古代文献与碑文智能修复与断代：调用 Aeneas 与 Ithaca 深度学习模型对古希腊语/拉丁语残篇进行语义修复与断代。",
        "category": "数字人文",
        "tags": ["碑文修复", "古代文献", "深度学习"]
    },

    # ==================== 5. 生物计算与生命科学 (Science & Bioinformatics) ====================
    "alphafold-database-fetch-and-analyze": {
        "summary": "AlphaFold 蛋白质结构预测与分析：根据 UniProt 编号提取 3D 预测结构、pLDDT 置信度及结构域边界分析。",
        "category": "生物与生命科学",
        "tags": ["AlphaFold", "蛋白质结构", "置信度分析"]
    },
    "alphagenome-atlas-website-links": {
        "summary": "AlphaGenome 基因组图谱直链生成：构建单突变位点分析直链、Locus 基因座视图与参考序列比对图谱。",
        "category": "生物与生命科学",
        "tags": ["基因组图谱", "变异位点", "深度链接"]
    },
    "alphagenome-single-variant-analysis": {
        "summary": "AlphaGenome 单变异调控效应分析：评估非编码区突变对基因表达（RNA-seq）、染色质可及性与转录因子的影响。",
        "category": "生物与生命科学",
        "tags": ["非编码变异", "表达调控", "功能预测"]
    },
    "alphagenome-variant-impact-score": {
        "summary": "AlphaGenome 变异影响评分 (AVI)：通过 AVI 评分与饱和突变扫描窗口，量化基因突变的致病性和功能损伤度。",
        "category": "生物与生命科学",
        "tags": ["AVI评分", "饱和突变", "致病性评分"]
    },
    "chembl-database": {
        "summary": "ChEMBL 生物活性与小分子药物库：检索活性小分子化合物、药物靶点结合亲和力（IC50/Ki）及分子化学结构。",
        "category": "生物与生命科学",
        "tags": ["ChEMBL", "药物活性", "靶点IC50"]
    },
    "clinical-trials-database": {
        "summary": "ClinicalTrials 全球临床试验数据库：按病种、药物、分期和招募状态检索全球临床试验方案与入组标准。",
        "category": "生物与生命科学",
        "tags": ["临床试验", "招募标准", "新药研发"]
    },
    "clinvar-database": {
        "summary": "ClinVar 人类变异临床致病性库：查询突变位点的临床致病性分类（致病/良性/意义未明）与循证医学证据。",
        "category": "生物与生命科学",
        "tags": ["ClinVar", "致病突变", "临床遗传"]
    },
    "dbsnp-database": {
        "summary": "NCBI dbSNP 短突变位点数据库：根据 rsID 查询单核苷酸多态性（SNP）、等位基因频率与 GRCh38 基因组坐标。",
        "category": "生物与生命科学",
        "tags": ["dbSNP", "SNP变异", "等位基因频率"]
    },
    "embl-ebi-ols": {
        "summary": "EMBL-EBI 本体查找服务 (OLS)：跨 250+ 生物医学本体库（GO、DOID、HP）检索标准受控词汇与层级拓扑。",
        "category": "生物与生命科学",
        "tags": ["生物本体", "受控词汇", "知识拓扑"]
    },
    "encode-ccres-database": {
        "summary": "ENCODE 顺式调控元件库 (cCREs)：查询人类各细胞类型的候选启动子、增强子及 ChIP-seq 组蛋白修饰峰图。",
        "category": "生物与生命科学",
        "tags": ["ENCODE", "增强子", "顺式调控"]
    },
    "ensembl-database": {
        "summary": "Ensembl 基因组与序列数据库：转换基因/转录本/蛋白编号，抓取序列外显子结构并预测突变后果（VEP）。",
        "category": "生物与生命科学",
        "tags": ["Ensembl", "基因结构", "VEP注释"]
    },
    "foldseek-structural-search": {
        "summary": "Foldseek 蛋白质三维结构极速比对：传入 PDB/CIF 结构坐标文件，在结构数据库中快速检索相似构象。",
        "category": "生物与生命科学",
        "tags": ["Foldseek", "结构比对", "同源构象"]
    },
    "gnomad-database": {
        "summary": "gnomAD 人群突变频率与基因耐受性库：查询人类群体等位基因频率及功能缺失不耐受指标（pLI / LOEUF）。",
        "category": "生物与生命科学",
        "tags": ["gnomAD", "人群频率", "基因耐受性"]
    },
    "gtex-database": {
        "summary": "GTEx 人体组织表达与 eQTL 数据库：检索人体 54 个健康组织中的定量 RNA 表达水平与变异表达性状关联。",
        "category": "生物与生命科学",
        "tags": ["GTEx", "组织特异表达", "eQTL分析"]
    },
    "human-protein-atlas-database": {
        "summary": "人类蛋白质图谱 (HPA)：查询人体正常组织与肿瘤中蛋白质的半定量表达及细胞内亚显微定位（免疫荧光）。",
        "category": "生物与生命科学",
        "tags": ["HPA", "组织表达", "亚细胞定位"]
    },
    "interpro-database": {
        "summary": "InterPro 蛋白质家族与功能结构域：整合 Pfam/CDD 等 14 个数据库，识别蛋白质结构域、保守位点与 GO 功能。",
        "category": "生物与生命科学",
        "tags": ["InterPro", "结构域", "蛋白质家族"]
    },
    "jaspar-database": {
        "summary": "JASPAR 转录因子结合基序库：获取转录因子的位置频率矩阵（PFM）与权重矩阵（PWM），用于结合位点预测。",
        "category": "生物与生命科学",
        "tags": ["JASPAR", "转录因子", "Motif基序"]
    },
    "ncbi-sequence-fetch": {
        "summary": "NCBI 序列自动抓取：通过 E-utilities 工具根据 Accession 序列号拉取核酸与蛋白质 FASTA 完整序列。",
        "category": "生物与生命科学",
        "tags": ["NCBI", "FASTA下载", "序列检索"]
    },
    "openfda-database": {
        "summary": "openFDA 药品与食品安全监管库：查询 FDA 药品不良反应报告、处方说明书、召回事件及医疗器械审批。",
        "category": "生物与生命科学",
        "tags": ["openFDA", "药物安全", "不良反应"]
    },
    "opentargets-database": {
        "summary": "Open Targets 药物靶点识别平台：分析疾病与靶点的遗传学证据、多组学关联度、成药性及临床在研药物。",
        "category": "生物与生命科学",
        "tags": ["OpenTargets", "新药靶点", "成药性"]
    },
    "pdb-database": {
        "summary": "RCSB PDB 实验生物大分子结构库：检索冷冻电镜/X射线测定的高分辨率蛋白质、核酸与配体 3D 实验结构。",
        "category": "生物与生命科学",
        "tags": ["PDB", "晶体结构", "大分子结构"]
    },
    "protein-sequence-msa": {
        "summary": "Clustal Omega 蛋白质多序列比对：执行多条蛋白质序列的同源比对，分析序列保守区域与核心催化残基。",
        "category": "生物与生命科学",
        "tags": ["多序列比对", "ClustalOmega", "保守性分析"]
    },
    "protein-sequence-similarity-search": {
        "summary": "MMseqs2 / BLAST 蛋白同源序列检索：基于氨基酸序列快速搜索同源匹配物并推断蛋白质生化功能。",
        "category": "生物与生命科学",
        "tags": ["MMseqs2", "BLAST", "同源搜索"]
    },
    "pubchem-database": {
        "summary": "PubChem 化学分子与生物活性库：根据 CID/SMILES/化学名检索化合物物化性质、化学结构与生物测试数据。",
        "category": "生物与生命科学",
        "tags": ["PubChem", "化合物", "小分子结构"]
    },
    "pymol": {
        "summary": "PyMOL 分子结构渲染与空间分析：生成高质量蛋白质 3D 构象渲染图、空间结构对齐与结合位点残基标注。",
        "category": "生物与生命科学",
        "tags": ["PyMOL", "分子渲染", "空间对齐"]
    },
    "quickgo-database": {
        "summary": "QuickGO 基因本体论注释平台：将基因映射至生物学过程、分子功能与细胞组分，探索 GO 词条上下级图谱。",
        "category": "生物与生命科学",
        "tags": ["QuickGO", "GO分类", "生物通路"]
    },
    "reactome-database": {
        "summary": "Reactome 生物学信号通路数据库：执行基因列表通路富集分析、信号转导级联网络检索并导出通路拓扑图。",
        "category": "生物与生命科学",
        "tags": ["Reactome", "通路富集", "信号转导"]
    },
    "science-skills-common": {
        "summary": "科学计算通用底层套件：提供内置速率限制、指数退避重试与容错机制的统一科学计算 HTTP 通信客户端。",
        "category": "生物与生命科学",
        "tags": ["基础套件", "HTTP客户端", "科学计算"]
    },
    "scienceskillscommon": {
        "summary": "科学计算通用底层套件：提供内置速率限制、指数退避重试与容错机制的统一科学计算 HTTP 通信客户端。",
        "category": "生物与生命科学",
        "tags": ["基础套件", "HTTP客户端", "科学计算"]
    },
    "string-database": {
        "summary": "STRING 蛋白质相互作用网络库 (PPI)：检索已知与预测的蛋白质互作关联、网络置信度评分与功能富集。",
        "category": "生物与生命科学",
        "tags": ["STRING", "PPI互作", "互作网络"]
    },
    "ucsc-conservation-and-tfbs": {
        "summary": "UCSC 进化保守度与转录因子结合位点：抓取多物种进化保守评分（phyloP/phastCons）及 ENCODE 转录调控位点。",
        "category": "生物与生命科学",
        "tags": ["UCSC", "进化保守度", "TFBS调控"]
    },
    "unibind-database": {
        "summary": "UniBind 实验转录因子结合位点库：提供经过直接实验验证的直接 TF-DNA 结合位点坐标与 BED/FASTA 数据下载。",
        "category": "生物与生命科学",
        "tags": ["UniBind", "结合位点", "ChIP验证"]
    },
    "uniprot-database": {
        "summary": "UniProt 蛋白质序列与功能知识库：检索蛋白质功能描述、分类学、结构域标注、催化活性与翻译后修饰。",
        "category": "生物与生命科学",
        "tags": ["UniProt", "蛋白质序列", "功能注释"]
    }
}

def normalize_key(name: str) -> str:
    """归一化技能键名，忽略中划线、下划线及大小写"""
    return name.strip().lower().replace("_", "-")

def get_chinese_summary(skill_name: str, original_description: str = "") -> dict:
    """
    根据技能名称和原始描述，返回结构化的中文概要、分类和标签
    """
    norm_name = normalize_key(skill_name)
    
    # 优先在标准映射字典中精确查找
    for k, v in BUILTIN_CHINESE_DICT.items():
        if normalize_key(k) == norm_name:
            return v.copy()
    
    # 模糊匹配或前缀分类
    if any(w in norm_name for w in ["bio", "gene", "protein", "alpha", "chem", "rna", "dna", "seq", "pdb"]):
        category = "生物与生命科学"
        tags = ["生信计算", "分子生物"]
        summary = f"生物信息与生命科学专业分析工具：提供针对 {skill_name} 的数据检索与计算支持。"
    elif any(w in norm_name for w in ["git", "branch", "repo"]):
        category = "版本控制"
        tags = ["Git", "版本管理"]
        summary = f"版本控制与分支管理工具：规范化 {skill_name} 操作流程与协同指引。"
    elif any(w in norm_name for w in ["test", "debug", "verify"]):
        category = "质量保证"
        tags = ["测试验证", "质量控制"]
        summary = f"软件测试与质量保证规范：辅助针对 {skill_name} 进行缺陷排查与自动化验收。"
    elif any(w in norm_name for w in ["ui", "frontend", "web", "css", "html"]):
        category = "前端与可视化"
        tags = ["前端设计", "交互界面"]
        summary = f"现代化前端与交互设计组件：提供基于 {skill_name} 的设计规范与实现能力。"
    elif any(w in norm_name for w in ["search", "paper", "literature", "arxiv"]):
        category = "学术检索"
        tags = ["文献检索", "科研助手"]
        summary = f"学术研究与文献检索助手：快速查询并分析与 {skill_name} 相关的学术成果。"
    else:
        category = "实用工具"
        tags = ["扩展技能", "效率工具"]
        summary = f"Antigravity 扩展技能：在特定场景下为模型提供 {skill_name} 的上下文规则与执行指引。"

    return {
        "summary": summary,
        "category": category,
        "tags": tags
    }
