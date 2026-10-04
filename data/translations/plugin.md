# 插件

插件**是一个带有命名空格的自定义捆绑包，用于发布、安装和
作为一个整体启动。它可以包含技能、代理、规则、MCP服务器和
钩子。当插件开启时，里面的所有东西都是激活的;禁用它需要
一整捆东西一下子倒下。

你的任务要么是更改插件的生命周期状态，要么是获取新的插件
功能性进入了合适的插件。步骤0和步骤1是两者共有的;步
1 会引导你进入 Step 2A 或 Step 2B。

对于底层的自定义系统——发现根、加载优先级，
每种自定义类型的用途——详见定制指南技能。就是这样
技能不代表内容。

## 步骤0：印前检查和盘点

每条路径都需要知道已经安装了什么。联系语言服务器
通过其本地Connect端点。地址和CSRF令牌通常已经
在你的壳体环境中;你不需要去找端口文件。

```bash
: "${ANTIGRAVITY_LS_ADDRESS:=localhost:5387}"
curl -sS "http://${ANTIGRAVITY_LS_ADDRESS}/healthz"
```

先把辅助工具写入一个文件，然后在下面每个调用中获取它的源代码。每人
你执行的命令是全新的 shell，所以一个调用中定义的函数会被删除
下一个;文件的来源是它可重复使用的关键。

```bash
cat > /tmp/lsrpc.sh <<'EOF'
: "${ANTIGRAVITY_LS_ADDRESS:=localhost:5387}"
lsrpc() {  # usage: lsrpc <MethodName> <json-body>
  curl -sS -X POST \
    "http://${ANTIGRAVITY_LS_ADDRESS}/exa.language_server_pb.LanguageServerService/$1" \
    -H "Content-Type: application/json" \
    -H "x-codeium-csrf-token: ${ANTIGRAVITY_CSRF_TOKEN}" \
    -d "$2"
}
EOF
```

现在列出已安装的插件。在该技能的每个“lsrpc”片段前加一个
'来源 /tmp/lsrpc.sh &'：

```bash
source /tmp/lsrpc.sh && lsrpc GetAllPlugins '{}' | jq '[.plugins[] | {
  name,
  dir: (.path | split("/") | last),
  disabled: (.disabled // false),
  isGlobal,
  skills: [.skills[]?.name],
  agents: [.agents[]?.name],
  rules: [.rules[]?.absolutePath],
  hooks: ((.hooksJson // "") | length > 0),
  mcp: [.mcpServers[]?.name]
}]'
```

> **绝不要未过滤地阅读“GetAllPlugins”。** 回复内嵌于 *full
>每个捆绑的“SKILL.md”的文本*。单个插件可能超过 16KB，且
>填充配置会淹没你的上下文。一定要通过“jq”管道。

**'dir' 是重要的标识符。** 它是安装目录名称——
最后一条路径——也是下面所有突变的关键所在。确实如此
经常**不**与“plugin.json”中的“name”同一个插件：安装的插件
来自市场的 会落在一个以签名 64 位哈希命名的目录中，因此
显示为“data-tools”的插件可能存在于名为
“-1870732469773246571。”在预期使用“dir”时使用“name”会无声失败，或者
修建一条垃圾通道。

## 第一步：决定类型

- 用户为现有插件命名，并使用生命周期动词——“关闭X”，
    “安装Y”、“去除Z”-> **步骤2A**。
- 用户希望新增功能，或希望整理现有的松散定制
    上——“我想要一个Strava功能”，“把这些技能打包在一起”——> **step
    2B**。

## 步骤2A：生命周期操作

先将目标从步骤0库存中解析到其“dir”。如果用户的
单词可以匹配多个插件，问是哪一个而不是猜。

**启用或禁用。** 这和写入插件页面执行的操作相同，而且
生效时即生效——不重启。

```bash
# Enable:
source /tmp/lsrpc.sh && lsrpc JetboxWriteState '{"userConfig":{"plugins":{"<dir>":{"enabled":true}}}}'

# Disable:
source /tmp/lsrpc.sh && lsrpc JetboxWriteState '{"userConfig":{"plugins":{"<dir>":{"enabled":false}}}}'
```

写入深度合并，所以只发送一个插件。绝不要手工编辑
'~/.gemini/config/config.json' 以实现这一点：写入绕过该语言
服务器错过了实时重载，只能通过慢速后备投票被选中。

**卸载。**

```bash
source /tmp/lsrpc.sh && lsrpc DeletePlugin '{"pluginId":"<dir>"}'
```

**运行前请检查这两个：**

- **内置插件无法卸载。** 路径包含
    “/builtin/plugins/” 是随产品预发的。拒绝，并提出关闭它
    反而。
- **卸载后会留下启用项。** 没有任何东西清除
    '插件。<dir>'来自'config.json'。如果插件被禁用了，之后又禁用了
    重新安装到同一个目录名后，它会显示 **disabled** 表示 NO
    显而易见的理由。在删除禁用插件之前，先把它设回启用状态，所以
    陈旧的条目无害，告诉用户你做了。

**安装。** 对于发布到代理市场的插件：

```bash
source /tmp/lsrpc.sh && lsrpc InstallCustomization '{"id":"<marketplace-id>"}'
```

你不能从插件名称中推导出这个ID。听听市场的说法
插件页面的标签页，或者向用户索要。如果你只有一个名字，那就说
所以，与其猜测身份认同，

“找不到来源”错误意味着两种情况之一：ID错误，或者
市场目录没有为该用户启动。目录柜里有一个明显的迹象——
ID返回为空，所以消息写着“用于定制，而非
“发现”，词语之间没有任何东西。先重新核对身份证。

只安装带有市场条目的插件。如果插件没有，或者
目录不会为该用户启动，不要尝试用其他方式安装;
告诉用户无法安装。

新安装的插件**目录**只在启动时被发现。告诉
用户在期待技能出现前重新开始。

生命周期操作到此结束。跳过只讲写作的第三步，直接去做
进入第四步。

## 步骤2B：确定该功能的归属

插件是一个捆绑包，所以第一个问题从来不是“我该做什么”，而是
“它去哪儿了？”从第0步开始做清单，看看请求是否成立
可以兼容现有插件。插件通常围绕以下三种形状之一凝聚：

- **数据提供商或外部服务。** 所有与同一系统通信的设备
    —— Strava，GitHub，一个特定的API。它是MCP服务器，是驱动力的技能
    它和关于它的个性规则是一体的。
- **一个工件或文件类型。** 电子表格处理、原型编辑、日志
    分析。按用户操作的设备分组。
- **一个角色或重复工作。** 数据分析，经营小型企业，
    审阅文档，编写代码。更广泛，且当
    能力跨越多个提供者，服务于同一重复任务。

**推荐并继续。** 一行说明你选择了哪个插件及其原因，
然后继续。只有当两个现有插件ask_question
是真正亲近的，或者是当一切都不合适，新的界限不清晰时。
不要在用户可以轻松撤销的决定上拖延。

如果都不合适，可以在'~/.gemini/config/plugins//'创建一个新插件<name>。
在确定名字之前，先对照Step 0库存：名字共享
一个全局命名空间，当两个插件声称同一个名称时，第一个
发现获胜，另一项则被无声地丢弃。

如果插件是要分享或发布的，请在源代码中创建
它将从仓库发布，而不是用户的配置文件目录。

### 整合松散的自定义

当用户要求整理独立自定义时，将目录移动：a
技能在“~/.gemini/config/skills/foo/”变成
'~/.gemini/config/plugins/<name>/skills/foo/'，规则变为
插件内的“rules/AGENTS.md”。

MCP服务器需要先收到警告。将条目移出用户的
“mcp_config.json”并与插件自身的“mcp_config.json”绑定了其生命周期
对插件来说：只有在插件启用时才组装，因此禁用了
插件会停止提供其工具，同时也停止在
捆绑。控制权也随之移动，因为服务器不再是
用户自行配置，并且通过插件管理，而不是单独管理。说
用户在你移动条目之前先了解这个。

## 步骤3：作者化捆绑包

只创建插件实际使用的子目录：

```text
~/.gemini/config/plugins/<name>/
├── plugin.json       # required
├── README.md         # user-facing docs; never read by the agent
├── mcp_config.json   # optional, same format as the user's own
├── hooks.json        # optional
├── assets/logo.svg   # optional
├── skills/<skill>/SKILL.md
├── agents/<agent>.md
└── rules/AGENTS.md
```

自己写内部定制——“SKILL.md”，代理折扣，
规则、MCP配置。不要把这些信息作为后续回复给用户。
插件的“rules/AGENTS.md”中的规则是纯的 markdown，没有 frontmatter 和
在插件启用时，这些都一直开启。

“plugin.json”被解析为JSONC，因此允许注释和逗号：

```json
{
  "name": "strava",
  "description": "Strava integration: pull activity data, summarize training load, and draft workout notes.",
  "logo": "assets/logo.svg",
  "suggestedPrompts": [
    "Summarize this week's workout mileage and heart rate zones",
    "Compare pacing and cadence across my last 4 long runs",
    "Draft an annotated Strava description for my latest activity"
  ]
}
```

|场 |类型 |注释 |
|------------------ |-------- |-------------------------------------------- |
|'名字' |字符串 |标签用户看到的，以及全局唯一 |
： ： ： 关键点 — 两个插件共享一个“名称”碰撞 ：
：：：：其中一个被掉落。**不是安装：
：：：标识符;那就是目录。小写：
：：：烤肉箱。默认目录名称：
： ： ： 如果省略。                                 :
|'描述' |字符串 |一两句话说明插件 |
：：：是谁，是为谁而做的。内容如下：
市场搜索匹配。                 :
|“标志” |字符串 |可选。相对于插件 | 的路径
： ： ： 目录，如“assets/logo.svg”，结尾：
： ： ： ： 在“.png”、“.svg”、“.jpg”、“.jpeg”或：
： ： ： '.webp'。URL和绝对路径分别是：
：：：默默拒绝——值不好则表示不 ：
：：：标志而不是错误。                  :
|'建议提示' |string[] |可选。最多3个卡片 |
：：：以及细节视图。三个提示如下：
推荐用于UI卡牌布局。空：
跳过字符串，新增提示：
：：：超过3的则被忽略。                       :
|'displayName' |字符串 |可选。人类可读的呈现标题 |
： ： ： 以UI头、卡片和斜杠显示：
： ： ： 命令菜单。                              :
|'版本' |字符串 |可选。语义版本字符串。          |
|“残疾” |布尔值 |可选。发货时插件是关闭的。A |
：：：用户已经在：
：：：这片田野。                                 :

> **不要添加任何其他顶层字段。** “作者”和“主页”是静默的
>被加载者丢弃——它们既不生效，也不会出错。

提出用“generate_image”工具生成标志。要求一个方形资产
至少128x128，背景透明，高对比度以便读取
两个主题，以及大约10%的空白边距——画面没有添加任何填充
它自己，中心裁剪任何非方形的部分。

## 步骤4：验证并交还

重新运行 Step 0 库存，确认插件是否与组件一起出现
你期待。然后告诉用户：

- 发生了什么变化，以及现在哪个插件拥有它。
- 是否需要**重启**。创建或安装新插件
    目录需要一个;启用、禁用和卸载都不行。
- 管理地点，作为链接：'[<name>]（<dir>customization://）' 打开
    插件自有页面，列出它提供的功能，并可以开关它。

“' <dir>是步骤0的安装目录，绝不是清单上的”名称“。A
该会话创建的插件目录直到重启才会被发现，且
在那之前，页面报告该ID下没有安装任何东西，所以请给出链接
还有一起重启。

不要发出“plugin://”或“plugins://”链接;它们不会被处理和渲染
作为死文本。

## 限制与技巧

- **在安装目录名称中标记所有变异，绝不标记“plugin.json”的
    'name'。** 这是破坏插件操作最常见的方法。
- **更倾向于语言服务器RPC而非编辑文件。** 'config.json' 是
    以 Mode 0600 原子形式写入，并保持兄弟状态 — 'userSettings'，
    许可授予。粗心的重写会让他们重创。
- **每个插件一个连贯的目的。** 捆绑无关能力的强制性
    用户进入全有或全无的切换模式。如果请求不符合
    插件描述，就是创建新插件的信号。
- **MCP 服务器名称也是全局的。** 它们会在用户配置中相互碰撞
    并且每个已安装的插件，所以插件的服务器都用该插件作为前缀
    用名称代替泛泛的“搜索”或“数据库”。
- **保持“描述”诚实且及时。** 它是用户在阅读前所读的内容
    安装以及匹配的搜索内容。当捆绑包内容时更新
    改变。