# 构建用户界面扩展

**UI 扩展**是一个小型本地网页应用，Antigravity 在侧面显示
玻璃窗旁边是一段对话。它被打包为一个包含
**sidecar**（应用启动并监督的后台进程），其
“sidecar.json”显示出一个网页界面。侧车运行本地 HTTP 服务器;
《反重力》将其页面嵌入沙盒iframe中，传递主题和
对话背景。

**始终将UI扩展作为插件创建**：
“插件/<plugin>/侧车/<sidecar>/”。插件是用户安装的，
在应用中启用和发现，之后还可以捆绑技能、规则和MCP
服务器与面板并列。不要在插件外创建裸侧车。

侧车用**Node.js**编写，内置了侧车SDK。反重力
安装SDK本身，因此扩展不需要“npm安装”，也不需要
“node_modules。”

## 参考实现

一个完整的、可工作的扩展位于该技能旁边
['参考文献/模板/']（参考文献/模板/）读一读，了解插件
布局和下面的图案，然后只构建用户扩展所需的内容。
你不必复制整个模板：重复使用适合的部分（
manifests、静态文件路由、“styles.css”），并省略了演示版本
特征。

```text
references/template/
├── plugin.json                  # Plugin manifest
├── assets/
│   └── logo.svg                 # Plugin logo shown in the app
└── sidecars/
    └── panel/                   # One sidecar = one UI extension
        ├── sidecar.json         # Process + UI manifest
        ├── package.json         # Marks the folder as an ES module package
        ├── main.mjs             # Backend: routes, APIs, persistence
        ├── index.html           # Frontend markup
        ├── app.js               # Frontend logic (window.sidecar)
        └── styles.css           # Theme-aware styles
```

它显示了所有动态环节：提供页面和静态文件，JSON API，
将状态持久化到侧车的数据目录，并向
特工。UI扩展的最低要求是
“plugin.json”、“sidecar.json”，一个后端入口点和一个页面
那就是加载“/preload.js”。

## 安装地点

Antigravity 在全局配置目录中发现插件：

|OS |插件位置 |
|------------- |----------------------------------------------- |
|macOS / Linux |'~/.gemini/config/plugins/<plugin>/' |
|Windows |'%USERPROFILE%\.gemini\config\plugins\<plugin>\' |

> [!重要]
> **不要假设操作系统。** 用户可能使用macOS、Linux或Windows。决心
在写入任何内容之前，>当前机器的主目录，
>更喜欢用文件编写工具而不是shell命令来创建目录，
>复制文件。如果必须使用弹壳，则与平台匹配：'mkdir -p'，
> 'cp -r' 在 Windows PowerShell 或 'cmd.exe' 中不存在。

## 显现

### 'plugin.json'

```json
{
  "name": "my-extension",
  "description": "One sentence on what the panel does and who it is for.",
  "logo": "assets/logo.svg"
}
```

- **'name'**：插件标识符，小写kebab大小写。默认使用
    如果省略目录名称。保持它和目录名相等以避免
    困惑。
- **'描述'**：显示在自定义界面中。
- **'logo'**：插件内方形图像的相对路径，下文显示
    应用里的插件。写一小段
    方形SVG（例如'viewBox=“0 0 64 64”'）logo.svg转换为反映
    扩展的作用：一个简单、易于识别的字形，出现在实体上
    圆角方形背景，小尺寸和光线下均清晰可辨
    黑暗主题。不要重复使用模板的标志。支持的格式为“.svg”，
    “.png”、“.jpg”、“.jpeg”和“.webp”;绝对路径，路径之外
    插件和远程URL被忽略。

### '侧车/<sidecar>/sidecar.json'

```json
{
  "command": "node",
  "args": ["main.mjs"],
  "restart_policy": "always",
  "display_name": "My Extension",
  "description": "What this panel shows.",
  "has_web_ui": true,
  "ui_config": {
    "display_name": "My Extension",
    "views": [
      {
        "path": "/",
        "entrypoint": "SIDECAR_UI_ENTRYPOINT_AUX_PANE",
        "title": "My Extension"
      }
    ]
  }
}
```

- **'command' / 'args'**：保持“command”： “node”''。反重力取代
    当有节点可用时，Node.js节点，节点捆绑，且运行时
    否则就回到“PATH”上的“node”，所以每个操作系统都一样。
    工作目录是侧车文件夹。
- **'restart_policy'**：“总是”（默认），“失败时”或“从不”。
    面板用“always”。
- **'has_web_ui'**：对于 UI 扩展必须为 'true'。
- **'ui_config.views[]'**：面板展示的每个视图。“path” 是 URL
    路径由你的后端服务;“入口点”必须是
    在侧面板中渲染“SIDECAR_UI_ENTRYPOINT_AUX_PANE”;“标题”标签
    风景。
- **'env'** *（可选）*：额外的环境变量，作为字符串映射。

插件的侧车被标识为**'<plugin-name>/<sidecar-folder>'**，当
例如“我的扩展/面板”。

## 运行环境

反重力为边车过程设定了以下变量：

|变量 |含义 |
|--------------------------------- |---------------------------------------------------------------------------------------- |
|“ANTIGRAVITY_SIDECAR_WEB_PORT” |你的服务器必须监听端口。“SidecarApp”会自动使用它。千万别硬编码。|
|“ANTIGRAVITY_EXECUTABLE_DATA_DIR” |该侧车的私有、持久数据目录的绝对路径：'<app data dir>/sidecar_data/<plugin>/<sidecar>/data/'。|
|“ANTIGRAVITY_SIDECAR_UI_TOKEN” |用于认证非GET请求的令牌。由SDK和“preload.js”处理。         |

进程输出（“stdout” / “stderr”）写入为
'<app data dir>/sidecar_data/<sidecar-id>/logs/sidecar.log'，应用数据
目录是 '~/.gemini/antigravity' （'%USERPROFILE%\.gemini\antigravity' on
Windows）。当面板是空白或不断重启时，先阅读这个文件。

> [!警告]
> 数据目录属于侧车进程，而不是它启动的代理。
> 代理人默认不能写入。如果小组和代理人需要
>交换文件，建议使用用户工作区内的位置。

## 后端：“SidecarApp”

```javascript
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SidecarApp, Response } from 'sidecar_sdk';

const here = dirname(fileURLToPath(import.meta.url));
const app = new SidecarApp();

// HTML (and .js) pages, served on GET.
app.page('/', () => readFileSync(join(here, 'index.html'), 'utf8'));
app.page('/app.js', () => readFileSync(join(here, 'app.js'), 'utf8'));

// Any other content type: return a Response from a GET API route.
app.api('/styles.css', () =>
  new Response(readFileSync(join(here, 'styles.css'), 'utf8'), { contentType: 'text/css' }),
  'GET');

// JSON API. POST is the default method; plain objects are sent as JSON.
app.api('/api/greet', (data) => ({ message: `Hello, ${data.name ?? 'world'}!` }));

app.run();
```

- **'app.page（路径，处理器）'**：返回字符串的 GET 路由。路径以
    “.js”作为JavaScript，其他内容为HTML。
- **'app.api（path， handler， method = 'POST'）'**： 'handler（data）' 接收一个
    将查询字符串参数和解析后的 JSON 正体合并的对象。
    JSON可以返回一个纯对象，其他内容则返回“Response”。
- **'new Response（body， { contentType， status }）'**：自定义内容类型或
    状态代码。
- **'app.run（）'**：启动服务器。注册路线后，打一次电话。
- “/preload.js”和“/_sidecar/*”桥接路线已为你注册。

**认证**：GET请求是开放的，因此页面、脚本、样式和
图像加载到iframe中。其他方法都需要边车令牌;用途
前端的“window.sidecar.fetch”，并且会自动附加。

### 编写可移植后端代码

- 构建带有“节点：路径”（“join”、“dirname”）的路径并推导出脚本
    目录来自 'fileURLToPath（import.meta.url）'.切勿将“/”或
    “\”手工写的。
- 使用 'os.homedir（）' 和 'os.tmpdir（）' 代替 '~'， '$HOME'， '/tmp' 或
    “%TEMP%”。
- 存储状态在“ANTIGRAVITY_EXECUTABLE_DATA_DIR”中，而非代码旁边;该
    插件文件夹在用户更新时可以被替换。
- 更喜欢内置Node.js。捆绑的运行时没有“npm”，所以
    第三方依赖必须被卖给 sidecar 文件夹。
- 如果必须生成进程，使用带参数的“execFileSync” / “spawn”
    阵列，没有壳。不要假设“bash”、shell脚本、shebangs或
    可执行位;在Windows上，“npm”和“npx”等“.cmd”垫片不能被使用
    生成时没有外壳。
- 保持文件名唯一，忽略大小写;macOS 和 Windows 文件系统是
    通常不区分大小写。

## 前端：“preload.js”和“窗。侧车”

在你自己的脚本之前加载桥接：

```html
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="/styles.css">
  <script src="/preload.js"></script>
</head>
```

它应用了主机主题，并暴露了“window.sidecar”：

|成员 |描述 |
|----------------------------------------------- |---------------------------------------------------------------------------------------------------- |
|'conversationId' |活跃对话ID，或当面板未绑定对话时为“空”。                     |
|'fetch（URL， options）' |“fetch”封装器，添加边车令牌和JSON “Content-Type”。用它来做你自己的 API 路由。|
|'getWorkspaceUris（）' |承诺对话中工作区文件夹的URI（“file://...”）;如果没有，则表示“[]'。                   |
|'onWorkspaceChange（listener）' |工作区发生变化时调用“listener（uris）”。返回一个取消订阅功能。                 |
|'agent.sendMessage（message， [conversationId]）' |向正在进行的（或已给出的）对话发送消息。                                              |
|'agent.startConversation（message）' |以“message”作为第一个提示开始新对话。                                       |
|'agent.getConversationMetadata（conversationId）' |返回对话的元数据。                                                                |
|'ui.toggleAuxPane（{ open }）' |打开（“true”）、关闭（“false”）或切换（省略）侧面板。                               |
|'ui.toggleConversation（conversationId）' |切换主持人到该对话。                                                        |

Workspace URI 是“file://”URI，包括在 Windows 上
（“file:///C:/Users/......”）把这些数据按现状传给后台，然后用
'fileURLToPath'，来自'node：url'。不要手动解析它们。

警卫特工呼叫“window.sidecar.conversationId”;他们需要一个主动的
对话。

## 主题

'preload.js' 将主机的主题标记复制到 '：root' 上并实时更新
当用户切换主题时。只用这些标记来做样式，并且每个标记都有一个
后退，确保页面在主机外仍可阅读：

- **表面**：'--背景'，'--内容'，'--卡片'，'--次级'，
    “--静音”，“--侧边栏”，“--侧边栏-次要”，“--侧边栏静音”
- **文本**：“--前景”、“--次要前景”、“--前景静音”
    “--主前景”， “--占位符”
- **重音**：“--主音”，“--口音”
- **边框**：“--边框”，“---卡片边框”

```css
.card {
  background: var(--card, #ffffff);
  border: 1px solid var(--card-border, var(--border, #e0e0e0));
  color: var(--foreground, #1f1f1f);
}
button:hover {
  /* Moves toward the text color: lighter in dark themes, darker in light ones. */
  background: color-mix(in srgb, var(--primary, #1a73e8) 88%, var(--foreground, #000));
}
```

不要使用 '--vscode-*' 变量。使用系统字体栈而非网页字体
所以面板在每个操作系统上都匹配主机。模板的“styles.css”是
完整的起点。

## 工作流程

1. **在用户插件目录中创建插件**（参见
    [安装地点]（#where 安装）以一个烤肉盒的名字命名，如下
    “参考文献/模板/”的结构。写作“plugin.json”，然后
    “sidecar.json”，并附有扩展名本身的名称、描述和头衔，
    并为扩展创建一个标志，地址为“assets/logo.svg”，参考来源
    “plugin.json”（参见['plugin.json']（#pluginjson））。
2. **构建功能。** 在 'main.mjs' 和页面中写入后端路由
    在“index.html”中（如有需要还加“app.js”这样的文字），重复使用。
    参考实现中的模式，以及它们所适用的位置。继续造型
    主题代币。
3. **告诉用户如何启用和打开它。** 以这些内容结束你的回复
    步骤，使用插件的真实名称：
    1. 进入左侧边栏的**自定义**页面，选择
        **已安装**标签页。
    2. 找到插件，如果未启用，就启用它。侧车
        一旦启用插件，会自动启动。
    3. 进入任何对话，打开顶部的**⋮**（三点）菜单
        右，然后从**扩展*菜单中选择扩展以打开它
        在右侧窗格。
4. **用“sidecar.log”调试**（参见[运行时环境]（#runtime-environment））。
    空白面板或崩溃的常见原因：main.mjs 中的语法错误，a
    缺少页面请求的文件路径，或者硬编码的端口。

编辑后端代码后，侧车必须重启才能接入：询问
用户可以禁用并重新启用该插件。如果后端重新读取前端文件
（'index.html'， 'app.js'， 'styles.css'）
实现时，关闭和重新打开面板就足够了
仅前端的变更。