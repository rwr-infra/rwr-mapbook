# R2 归档管理（上传 / 删除 / 查看）

本站那十个历史版本整包（318 MB）**不在仓库里**——它们放在 Cloudflare R2 上，
页面上挂的是直链。这个目录就是管那批文件的命令行工具。

> **为什么不放仓库**：这个仓库里会变的是正文；带着几百 MB 归档走的话，
> 每个想改一个字的人 `git clone` 都要先拉几百 MB。

## 这个工具是给谁用的

维护者（能给 R2 上传/删除的人）。**只读仓库的人用不到它**——页面上的那些直链
点开就能下，不需要任何密钥。

> 🔑 **凭据不随仓库发。** 工具在 `tools/r2/`，密钥永远不在仓库里。
> 需要能上传 / 删除归档的凭据（或想让自己的账号能改这批归档），
> 去这里找人开：**<https://github.com/bananaxiao2333>**。
> 拿到之后自己存成 `creds.env`（见下），**它只属于你这台机器，不要提交、不要外传**。

## 三步上手

### 1. 装 boto3

```bash
python -m pip install boto3
```

（这台机器上用的是工作区里的便携 Python：
`D:/RWRWorkSpace/_py/py314/python.exe -m pip install boto3`。
`r2.bat` 会按 `RWR_PYTHON` 环境变量 → 那个便携 Python → PATH 上的 `python`
的顺序找解释器。）

### 2. 拿 R2 的 S3 凭据

凭据**不公开发放**——先按上面那段联系维护者要一对，或者自己按下面几步在
Cloudflare 面板上建一个（有权限的人才能建）：

1. **R2 → 概览**，右上角复制 **账户 ID**（endpoint 要用）；
2. **R2 → 管理 API 令牌**（Manage R2 API tokens）→ 创建**账户 API 令牌**；
3. 权限选 **Object Read & Write**（只上传也要 Write；要删文件同样靠它），
   桶范围选 `assets`（或你自己的桶）；
4. 创建完会显示 **Access Key ID** 和 **Secret Access Key**——**只出现这一次**，
   先存好再关页面。

### 3. 填自己的 creds.env

```bash
copy creds.example.env creds.env     # Windows
cp   creds.example.env creds.env     # macOS / Linux
```

然后编辑 `creds.env`：把 endpoint 里的 `<account-id>` 换成你的账户 ID，
两把钥匙换成上一步拿到的值。

⚠️ **`creds.env` 里是真密钥**：不要提交进仓库、不要发给别人、不要贴工单或聊天里。
它**不在仓库里**——`.gitignore` 挡着，推送工具也另有一道（见下）。

想换一种给法也行——**环境变量优先于文件**：

```
R2_CREDS=D:\某处\r2-creds.env          # 换一个文件位置（放在仓库外面最省心）
R2_ENDPOINT / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY
R2_BUCKET / R2_PREFIX / R2_PUBLIC_BASE
```

## 密钥放哪儿、怎么防漏

按顺序找：`R2_CREDS` 指的文件 → 本目录的 `creds.env` → `~/.r2/creds.env`；
文件里的每一项都能被同名环境变量盖掉。

**工具在仓库里，密钥永远不在。** 仓库那一份 `tools/r2/` 里只有代码与
`creds.example.env` 这个占位版；你自己的 `creds.env` 放哪儿都行，但别放进仓库：

- **`.gitignore`** 里已经写了 `creds.env` / `*.env`；
- 维护者用的推送工具另有一道**独立守门**（它走 GitHub API、根本不读 `.gitignore`）：
  文件名像密钥的（`creds.env`、`.env*`、`*.pem`、`id_rsa*` …）一律跳过并打印出来，
  连已经躺在远端的历史误推文件也会顺手删掉。

放在仓库外面最省心：`R2_CREDS=%USERPROFILE%\.r2\creds.env`，或者只设环境变量。

**文件权限**默认是宽的——工作区里那份实测 `BUILTIN\Users`（同机任何账户）可读、
`NT AUTHORITY\Authenticated Users` 甚至可写。「同机任何账户都能读到一把能改写归档
的钥匙」不该是常态，收紧一下：

```
r2.bat lock        # 去掉继承来的权限，只留你自己
r2.bat creds       # 看凭据是从哪儿读的、权限紧不紧（值一律打码）
```

`lock` 之后想恢复原样：`icacls creds.env /reset`。

几条习惯：

- **脚本任何输出都不打印密钥**：`creds` 打的是打码版，出错信息里也会把密钥抹掉
  （`redact()`），所以贴终端输出、贴报错都不会带出密钥；
- 想让密钥彻底离开你的工作目录（目录会被打包、会被别的东西读）：把文件挪出去，
  再用 `R2_CREDS` 指过去，或者干脆只设环境变量；
- **真要觉得漏了**：去 Cloudflare 面板把那个 API 令牌**吊销重建**（R2 → 管理 API
  令牌），再把新的一对值填回 `creds.env`——比追查「到底谁看过」省事得多。

### 4. 验证连上了

```bash
r2.bat list
```

列出来十个包（约 303 MB）就成了。

## 命令

```
r2.bat list                        线上都有什么
r2.bat head 060.zip                看一个文件的大小、类型、缓存头、公开地址
r2.bat upload D:\pkg\070.rar       上传一个（对象名默认就是文件名）
r2.bat upload-dir D:\pkg           上传一个文件夹里的文件
r2.bat delete 070.rar              删除（要你手打一遍名字才肯删）
r2.bat verify                      页面上的直链/哈希/大小，和线上对一遍
r2.bat verify --hash               连哈希一起核（把这些文件流式读一遍再算，慢）
r2.bat creds                       凭据从哪儿读的、权限紧不紧（值打码）
r2.bat lock                        把凭据文件的权限收紧到只有你自己
```

Windows 上 `r2.bat` 只是包一层；其它系统直接 `python r2.py <命令>`。

`upload` 不加对象名时，对象名就取文件名（`070.rar`）。想换名字：
`r2.bat upload D:\pkg\新版.rar 070.rar`。

## 发布前对一遍（`r2.bat verify`）

站外那十几条直链**不在 CI 的体检范围里**（`linkcheck` 够不着别的域），页面上的哈希
也没人复核；十几条链接靠手点不现实。`verify` 一次把这几件事说清：

- 页面链了、线上没有 → **点开就是 404**（会算作失败，退出码非 0）；
- 线上有、页面里没人链 → 漏挂还是历史遗留，你自己判断；
- 页面链了但哈希表里没有这一条（或反过来）→ 两处记录对不上了；
- 大小标签和线上对不上（页面写的是**十进制**：26.2 MB 就是 26 212 902 字节）；
- 各语言的页面链接/哈希不一致 → 英文页改漏了；
- 加 `--hash` 再把线上文件流式读一遍、真算一遍 sha256 对一遍
  （十几条链接 300 MB 左右，慢；想抽样就用 `--only vdao.svg` 挑几个）。

`list`/`head`/`upload` 打的大小也是**十进制**，和页面上的数字同一套——
可以直接把 `r2.bat list` 的数字抄进页面。


## 整批上传一个文件夹

新加一批文件时（比如新版本的模板与预制件都在同一个目录里），一个一个传太麻烦：

```bash
r2.bat upload-dir D:\RWRMap\0100\1007_Data\assaumbles
r2.bat upload-dir D:\RWRMap\0100\1007_Data\assaumbles --ext .asmb      # 只传这类
r2.bat upload-dir D:\pkg --dry-run                                     # 先看看会传什么
```

它做的事：

1. 先把**清单列出来**（文件名 + 大小 + 合计），整个确认一次再动手，
   不至于每个文件问一遍（三个文件问三次很烦）；
2. 每个文件照旧走那一套：算 sha256、按扩展名给类型、带长缓存、传完 HEAD 校验；
3. **同名还是一个个查**：线上已有同名的那几个会被跳过并说明（不覆盖），
   要覆盖就加 `--overwrite`；
4. 最后把这一批的 sha256 一次列出来，直接粘进页面那份哈希表。

几个开关：`--ext` 挑后缀、`--dry-run` 只列不传、`--recursive` 连子文件夹一起
（⚠️ 对象名只取文件名，子文件夹里的同名文件会互相覆盖，慎用）、
`--content-type` 整批指定一个类型、`--yes` 不问直接传。

⚠️ **默认不往子文件夹里钻**：本站的约定是「对象名就是文件名、不带目录」，
   所以整批上传只取顶层文件；下面还有子文件夹时会告诉你一声，让你自己决定。

## 上传时会做什么

1. 先把本地文件的 **sha256 算出来给你看**，问一句「上传？」——
   传错文件是这里唯一会静默出错的地方，所以对一眼再回车（`--yes` 可跳过）；
2. **同名会挡下来**：线上已有同名对象就直接拒绝，并告诉你线上那个多大、
   什么时候改的。归档是冻结的，覆盖找不回来；要覆盖得显式加 `--overwrite`；
3. 按扩展名给 `Content-Type`（`.zip` → `application/zip`、
   `.rar` → `application/vnd.rar`、`.svg` → `image/svg+xml`，其余自动猜；
   认不出的（比如 `.asmb`）按 `application/octet-stream` 传并提示，
   可用 `--content-type` 指定）；
4. 一律带长缓存 `Cache-Control: public, max-age=31536000, immutable`；
5. 几十 MB 的包走分段上传；传完 HEAD 一下，线上大小和本地对不对会明说；
   大文件（≥ 8 MB）在终端里画一行百分比进度，免得看着像卡死；
6. 打印公开地址和 sha256，拿去更新页面里那份清单。

## 删除时会做什么

先显示这个对象的大小、公开地址，然后**要你手打一遍对象名**才肯删
（防手滑；`--yes` 可跳过，慎用）。删完再查一次有没有残留。

## 新增一个归档的完整步骤

1. `r2.bat upload D:\xxx\文件名.asmb`（对象名默认取文件名，别带目录）；
2. 记下脚本最后打印的 **sha256** 和公开地址；
3. 页面侧同步：在 `content/download/index.zh-hans.md` 加一行（文件名、大小、直链），
   并把 sha256 添进表下那份清单；英文页 `content/download/index.en.md` 同样改，
   并让译文的 `source_sha256` 跟着更新，否则 `i18n_check` 会判「已过期」；
4. **`r2.bat verify`** 对一遍：链接在不在、哈希表跟没跟上、英文页改漏没有；
5. 本地预览会自动重建，开 <http://127.0.0.1:8000/download/> 点一遍新链接。

## 几条约定（与仓库 README 的「历史版本归档放在站外」一致）

- **对象名就是原文件名**，不带版本目录——名字本身已经唯一，多套一层只会在换存储时
  多一处要改的地方；所以这里也只认一层文件名，传 `a/b.zip` 会被拒绝；
- **归档是冻结的**：同名文件永远同一个内容，所以敢上 immutable 长缓存。
  已经发出去的包不要改内容，要变就换一个新文件名；
- **哈希只写一处**：只在页面 `content/download/index.<lang>.md` 的清单里写，
  存储那边不另存清单文件（两份记录会分叉，一份不会）；
- **站外那些直链不在 CI 体检范围内**（它们指到别的域上，构建期够不着）——
  改过下载页就用 `r2.bat verify` 对一遍，别靠手点。

## 出问题怎么查

| 现象 | 多半是 |
| --- | --- |
| `× 缺 R2_ENDPOINT / R2_ACCESS_KEY_ID …` | `creds.env` 没建或没填全；从 `creds.example.env` 复制一份（或用 `R2_CREDS` 指到别的路径） |
| `AccessDenied` | 令牌权限不够（要 Object Read & Write），或桶范围不对 |
| `NoSuchBucket` / 403 | `R2_BUCKET` 填错；本站是 `assets`，`rwrme-web-assets` 是**前缀**不是桶名 |
| `list_buckets` 报 AccessDenied | 正常——R2 不允许列桶，按桶操作不受影响 |
| 上传卡住不动 | 走的是外网；几十 MB 分段上传，看终端提示（有进度条那行） |
| 页面上的链接 404 | 对象名和页面写的文件名不一致（大小写、后缀）——`r2.bat verify` 会直接点名 |
| `verify` 说「大小标签对不上」 | 页面写的是十进制 MB，别把 MiB 的数字抄进去（`list` 打的就是十进制） |
| `lock` 报 `Access is denied` | 权限改动被当前环境挡住了；在一个正常的 cmd 窗口里跑同一条 `icacls` |

