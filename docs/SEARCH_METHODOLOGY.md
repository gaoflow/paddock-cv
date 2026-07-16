# 围场岗位搜索方法论（How to Search）

> 本文档沉淀本项目从 0 到 480+ 人档案、389 张已验证头像的全部搜索方法。
> 目标读者：想复刻"选定一个围场岗位 → 摸清全部在职者 → 反推入行路线"研究的人。
> 配套文档：`SEARCH_LOGIC.md`（逐条操作日志）、`DATA_METHOD.md`（数据规范）、`RESEARCH_METHOD_2026-06-29.md`（单日深挖实录）。
> 更新：2026-07-16。

## 0. 核心原则（先读这个）

1. **宁缺毋假**。找不到就留空，绝不编造履历、绝不张冠李戴头像。错误的脸比首字母占位符伤害大得多。
2. **每条结论都要有可点开的来源**。每次采纳/拒绝都写入审计文件（本项目为 `data/lookup_runs.json`，已 180+ 条）。
3. **身份绑定强度决定一切**（见 §4）。同名人极多（例：Aston Martin 工程师 Stephen Glass vs 同名足球运动员 David Wheater vs 同名球员），绑定不牢就拒绝。
4. **搜索是漏斗不是清单**：宽 → 窄 → 验证 → 审计，每层都有明确的停止条件（§7）。

## 1. 研究一个岗位的四层问题

| 层 | 问题 | 主要信源 |
|---|---|---|
| L1 岗位定义 | 这个岗位做什么、在组织里的位置 | 车队官方 careers 博客、编辑访谈（motorsport.com 对 Haas RE Dominic Haines 的访谈是范本） |
| L2 在职名单 | 2026 赛季每支车队这个岗位是谁 | 赛季前瞻综述（RacingNews365 "F1 race engineers 一览"）、车队官宣、TV 转播口播交叉验证 |
| L3 个人履历 | 每个人怎么走到这个位置（学历→轨迹→年限） | LinkedIn 公开摘要、大学校友专题、编辑访谈、FIA/系列赛官方 People 栏目 |
| L4 可视化资产 | 头像、车队 logo | 见 §4 头像专章 |

**关键认知：L2 是全研究的地基。** 名单错了后面全错。名单必须用 ≥2 个独立信源交叉（综述文章 × 官宣 × 转播/社媒口播），并记录置信度（high/medium/low）。

## 2. 信源金字塔（可信度从高到低）

1. **第一方**：车队官网/careers 页、车队官方 media 发布（media.alpinecars.com 这类官方 CDN 带命名图说的最硬）、系列赛官方（FIA F2 "People of the Paddock"、ELMS/GTWC 车手档案、Formula E 车队页）。
2. **权威编辑**：motorsport.com、The Race、F1.com features、Autosport、地区大报的单人专访（Il Mattino 对 Nenci 的专访）。**单主体专访的头图 > 顺带提到的配图**。
3. **教育/机构**：大学校友专题（剑桥 Girton 学院之于 Adam Kenyon、巴斯大学 case study 之于 Oli Cartlidge）、Cranfield/Oxford Brookes 等赛车工程硕士项目页。**这是被普遍低估的富矿**——校友当上 F1 工程师，母校一定发专题。
4. **本人自证**：本人 LinkedIn/XING 公开档案（自己选的照片=身份可靠；文字履历可用但需交叉验证在职时段）。
5. **聚合器（只当线索，永不当证据）**：theorg.com、RocketReach、autoracing1 mugshots——第三方抓来的照片无法验证归属，**一律拒绝作为头像来源**；文字信息只用于生成新的搜索词。

### 2b. 岗位入行信息的专属信源（2026-07 新增验证）

- **车队 careers 博客直接回答"怎么进来"**：Williams careers 博客有 "How to become an F1 engineer" 专文；Mercedes 官网列出 2 个 24 个月工程 graduate programme（每年 9 月入职）；Aston Martin careers 有 early-careers 分层页。
- **F1 官方自己也招**：Biggin Hill 工程部有 12 个月 industrial placement（Raceteq 2026-05 报道）。
- **聚合器**：formulacareers.com（按岗位类型分类的 live vacancies，周更）、motorsportjobs.com、fluidjobs.com（例：Cadillac Graduate Model Design Engineer，2026-07-10 截止）。
- **从业者共识与我们的 26 人 CV 数据互证**：r/F1FeederSeries "最优路径是以 placement student 或 graduate 身份直接进 F1"——对应我们数据里 uni→junior formula→F1 15/26、数据工程→RE 8/26 的分布。

## 3. 查询模式手册（Query Patterns）

按产出率排序：

```text
# 名单层
"<系列赛> <年份> race engineers" 综述        → RacingNews365/GPFans 年度盘点
"<车队> announces|appoints <岗位>"            → 官宣
site:linkedin.com/in "<姓名>" "<车队>"        → 本人档案（拿摘要即可,别指望进得去）

# 履历层
"<姓名>" "<大学>" OR "MSc" OR "graduated"     → 校友专题/学位信息
"<姓名>" interview|访谈|Q&A                    → 单人专访(履历+头图双收)
"In Profile <姓名>"                            → GTWC/系列赛官方人物专栏固定栏目名

# 头像层
"<姓名>" site:<车队官网域名>                   → 官方肖像
"<姓名>" wikimedia OR wikipedia               → 自由授权图
"<姓名>" + 母语媒体名                          → 意大利人搜 Il Mattino/motorionline,
                                                 法国人搜 Endurance-Info/AutoHebdo
```

**语言本地化是隐藏杠杆**：意大利工程师用意大利语搜、法国人用法语搜，编辑专访几乎都在母语媒体。

## 4. 头像的身份绑定强度谱（本项目最重要的方法输出）

从强到弱，取最强可得项：

1. **官方 CDN + 命名图说**：车队 media 发布会图集里 `<p class="img-text">Joe Burnell</p>` 这种逐图命名 → 直接采纳。
2. **单主体专访头图**：文章标题就是这个人（"quattro chiacchiere con Marco Adurno"）→ 采纳。
3. **文件名/alt 命名 + 第二独立佐证**：图片文件名含 `audi_francesco_nenci` + 另一家图库的 DTM 图说提到同一人 → 采纳。
4. **上下文排除法（medium 置信）**：双人照中另一人是已知车手（可脸部比对），目标按位置/制服排除确定 → 采纳但标 medium。
5. **本人自选照片**（XING/LinkedIn 自己的头像）：身份可靠，无更强来源时采纳。
6. **以下一律拒绝**：视频帧/YouTube 缩略图（含 maxresdefault）、licdn.com 直链（999/过期）、theorg/RocketReach/autoracing1 第三方 mugshot、带水印的 Getty/Alamy 预览图、车比人大的"工作照"、无法定位人物的合影。

**采纳后的固定流水线**：下载（校验 HTTP 200 + `image/*` + JPEG 结尾 `ffd9`）→ 用眼睛看一遍（是不是这个人、单主体、脸清晰）→ 裁剪成头像 → 本地化存 `web/img/<name>-<source>.jpg` → 数据文件写 local 路径 + 完整 provenance → 审计文件记一条。**永远不要引用远程 URL 上线**（ORB 封锁、链接腐烂、防盗链都会让它悄悄挂掉）。

## 5. 履历数据的核验规则

- 每条 career entry 必须带 `source_url + source_title`；教育条目同理。
- LinkedIn 公开摘要可以作为骨架，但**在职时段和职位名要有第二信源**（官宣/专访/系列赛人物栏）抽查印证。本项目按 ~15% 比例抽查，全部通过才整批合入。
- 中文字段（org_zh/role_zh）是翻译层，不是事实层——事实以英文原文为准。
- 合并脚本只填空、不覆盖（见 `/tmp/f1careers/merge.py` 模式：`if new and not existing`）。

## 6. 工具链

- **搜索**：mysearch MCP（Tavily+Firecrawl 交叉验证模式），比单引擎少 30%+ 幻觉命中；LinkedIn/Wikipedia 公开摘要可读。
- **批量**：把 8-16 人一组发给子代理并行搜，**给代理的提示词里写死拒绝规则**（"licdn/theorg/视频帧一律返回 NONE"），否则代理会把垃圾源当成果。
- **下载**：curl 带浏览器 UA + Referer；部分域名 ORB 封锁直接放弃（motorsport.hyundai.com、autohebdo.fr 等）。
- **验图**：宁可人眼看一遍（Read 图片），不要信文件名。
- **审计**：`data/lookup_runs.json` 每条含 `run_type/target/tool/provider/status/notes_zh`。

## 7. 停止条件（什么时候承认"没有"）

一个人可以标记为"无公开静态头像"，当且仅当：

1. ≥2 个独立代理/轮次、≥4 种查询模式（官方站、编辑、Wikimedia、母语媒体）全部落空；
2. 找到的全部候选都命中 §4 的拒绝清单；
3. 审计文件里记录了"确认无"及其证据。

本项目的实测天花板：F1 工程师 59/68、系列赛人员 316/407——剩余缺口全部是 blocked-LinkedIn-only 或 video-only 的后台工程师/技师。**F2 后台长尾已被证明是贫矿**（3 个代理 × 20 个目标 = 0 产出），不要再烧 token。

## 8. 常见坑（都踩过）

- **同名人**：David Wheater（Alpine 空动总监）≠ David Wheater（足球运动员）。绑定必须含车队/岗位上下文。
- **"文章提到他"≠"图是他"**：F1.com 讲 Stephen Glass 重组的文章头图是 Lance Stroll。
- **聚合器的自信是假的**：theorg 上的哈斯"组织架构图"配的照片来源不明，4 张全拒。
- **数据过期**：围场人事一个转会窗就变（Wheatley 2026-03 闪离 Audi）。任何"某人在某队"的断言都要带时间戳，改名单前先搜最新动态。
- **视频帧的诱惑**：Montecchi 只有 F1-75 发布会视频帧（带字幕烧录），再清晰也不用——规则就是规则。

## 9. F1 职位与人员深挖策略（2026-07-16）

### 9.1 为什么旧策略会漏人

旧流程以 `Technical Director`、`Head of Race Engineering`、`Race Engineer`、`Strategy Engineer` 等少数标准 title 为中心。实际车队没有统一组织图和统一职称：同一责任域可能使用 `Director, Race Engineering`、`Associate Director, Race Engineering`、`Chief Strategist`、`Strategy Analytics & Data Engineer`、`Head of Aero Performance & Correlation` 等名称。只搜标准 title 会出现两类错误：

1. 已公开的人没有命中，被页面误显示成“未找到姓名”。
2. 不同职业路径被压成一栏，例如轮胎与气动、系统与控制、仿真与测试、CTO 与 Chief Designer。

完整岗位族、职责边界和一级来源见 [`docs/research/f1-role-taxonomy-strategy-2026-07-16.md`](research/f1-role-taxonomy-strategy-2026-07-16.md)。公开样例使用的机器可读版本是 `data/sample/f1_role_taxonomy.json`。

### 9.2 搜索单位改为“车队 × 岗位族 × 职级”

每支车队建立覆盖矩阵，不再问笼统的“这队工程师是谁”，而是逐格搜索：

```text
车队（含现名、法律实体名、历史名）
× 岗位族（含职责同义词）
× 职级（director/head/principal/lead/senior/engineer/graduate）
× 工作范围（factory/trackside/car/remote support）
```

岗位族至少覆盖：技术管理、工程与机械设计、气动研发、赛道气动、车辆动力学、单车性能、赛道/比赛工程、策略、仿真建模、DiL 模拟器、系统电子、控制、性能软件与数据、动力单元与集成、轮胎性能与建模、可靠性测试验证。

### 9.3 每格执行五轮查询

1. **官方组织轮**：车队官网的任命、组织调整、人物专题，先确定部门和职责边界。
2. **精确 title 轮**：`site:linkedin.com/in "<车队别名>" ("Head of X" OR "X Engineer")`。
3. **部门反向轮**：不限定 senior title，搜索 `lead/senior/engineer/graduate`，避免只找到负责人。
4. **人员反向轮**：从明确的个人档案读取车队实际 title，再用该 title 和历史队名扩展同部门搜索。
5. **时效复核轮**：确认 `Current/Present`、开始时间、是否已离队或仅为未来任命。

车队别名必须包含历史与商业名称。例如 Racing Bulls 同时搜索 `Racing Bulls`、`Visa Cash App RB`、`RB F1 Team`、`VCARB`、`Faenza`；Audi 同时搜索 `Audi Revolut F1 Team`、`Sauber`、`Hinwil`；Cadillac 同时搜索 `Cadillac Formula 1 Team`、`Andretti Cadillac`、`Silverstone`。

### 9.4 MySearch 的实际使用记录

本轮确实使用了 MySearch，不是只写在方法论里。调用端从 `MYSEARCH_BASE_URL` 读取服务地址；同机部署建议使用 loopback，避免 DHCP 地址变化导致中断。MySearch 用于：

- 批量返回公开 LinkedIn 档案摘要，读取当前职位、起止时间和车队实体；
- 同时搜索多个 title alias，发现车队自己的真实命名；
- 对欠覆盖岗位族做跨车队反向扫描，例如 simulation、controls、tyres、reliability、trackside aero。

MySearch 是发现工具，不自动等于证据。合入规则仍是：官方页面可标 `high`；能精确绑定本人、当前车队、当前职位的本人公开职业档案可按用户要求标 `medium` 合入；聚合站摘要、招聘广告和搜索结果推断不得生成人名。

### 9.5 覆盖与停止条件

- **覆盖状态属于研究审计，不属于首页人物卡。** 某格未找到公开姓名，只表示本轮研究未解决，不表示车队没有该岗位。
- 同一岗位族至少跑完官方、精确 title、部门反向、人员反向四种查询，才允许记录 unresolved。
- 招聘广告只能证明岗位或部门存在，不能证明现任者是谁。
- 未来任命、已宣布但未到岗人员与当前在职人员分开，不提前移动车队归属。
- 每次更新保存查询日期、使用的车队别名、岗位同义词、采纳/拒绝理由和来源 URL。

本轮在私有编译数据中补入此前因 title alias 和岗位族缺失而漏掉的策略、比赛工程、车辆性能、仿真、控制电子、轮胎、赛道气动和可靠性人员；所有新增记录均保留英文原始职位。公开仓库只发布岗位分类、方法论和虚构样例，不发布真实人员数据。
