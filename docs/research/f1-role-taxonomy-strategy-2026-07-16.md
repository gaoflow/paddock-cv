# 2026 F1 工程/技术岗位分类策略

Research date: 2026-07-16

## 结论摘要

`data/series_engineering.json` 当前的 11 个 F1 `role_templates` 适合做赛道工程概览，但不足以支撑“F1 工程师职业路径”仪表盘。主要问题不是缺少更多 seniority，而是把不同专业、不同入口和不同晋升路径压成了同一个槽位：

- `technical-leadership` 把全局 CTO、工程/设计、气动、性能和 Chief Designer 混在一起；McLaren 官方组织公告明确把 Engineering、Aerodynamics、Performance 设为不同技术责任域，2026 官方赛车专题又同时列出 Chief Designer 和 Technical Director, Performance。[McLaren 2024 organisational update](https://www.mclaren.com/racing/formula-1/2024/mclaren-formula-1-team-announces-organisational-updates/)；[McLaren MCL40 2026 technical feature](https://www.mclaren.com/racing/formula-1/2026/behind-the-design-of-the-mcl40/)
- `test-simulation-engineer` 混合了车辆动力学/模型开发、仿真研究和 Driver-in-the-Loop 设施运行。Williams 的 2026 careers 内容把 Vehicle Dynamics、Simulation Concepts 和 DiL Test 明确描述为不同工作对象。[Williams graduate opportunities](https://careers.williamsf1.com/graduate-opportunities)；[Simulation Concepts Engineer](https://careers.williamsf1.com/job/simulation-concepts-engineer-in-grove-jid-146)；[DiL Test Engineer](https://careers.williamsf1.com/job/dil-test-engineer-in-grove-wantage-jid-624)
- `systems-controls-engineer` 混合了系统架构/电子、嵌入式控制和数据处理软件。Williams 官方职位分别要求系统级电气电子架构、实时控制算法，以及实时遥测数据处理软件，三者不是同一条职业路径。[Senior Systems Engineer](https://careers.williamsf1.com/job/senior-systems-engineer-in-grove-wantage-jid-363)；[Senior Control Systems Engineer](https://careers.williamsf1.com/job/senior-control-systems-engineer-in-grove-jid-167)；[Data Processing Software Engineer](https://careers.williamsf1.com/job/data-processing-software-engineer-in-grove-jid-177)
- `tyre-aero-trackside` 把轮胎和气动合并，缺乏组织依据。Mercedes 官方赛道工程专题把 tyre engineer 与 aerodynamicist 列为不同席位；Williams 也把 tyre performance/science 与 development/CFD/trackside aerodynamics 分开。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers)；[Williams Aerodynamics](https://careers.williamsf1.com/aerodynamics-jobs)；[Williams tyre roles](https://careers.williamsf1.com/blog/2025-10/exploring-the-role-of-tyre-jobs-in-formula-1)
- 现有模板没有机械设计、车辆动力学、气动研发、性能软件/数据、可靠性/验证和动力单元集成等主要岗位族。Williams 2026 官方早期职业页面将 Vehicle Engineering、Vehicle Dynamics、Aerodynamics、Performance Systems 分列，并在 Vehicle Engineering 下进一步列出 materials、powertrain、structures、systems、design quality、suspension/steering/brakes 等组。[Williams graduate opportunities](https://careers.williamsf1.com/graduate-opportunities)；[Vehicle Engineering placement](https://careers.williamsf1.com/job/vehicle-engineering-industrial-placement-in-grove-jid-278)

建议将模板从“公开人物常见 title 列表”改成“可稳定跨车队映射的岗位族”。title 只作为 alias；最终归类依据职责范围（remit），而不是字符串。

## 分类原则

1. **岗位族必须代表可区分的工作对象或职业路径。** 例如机械设计、气动研发、车辆动力学、控制开发所需技能和常见入口不同，应有独立 `role_key`。
2. **领导岗按责任域分类，不按 `Technical Director` 字样分类。** McLaren 的官方结构说明 Technical Director 可以分别负责 Engineering、Aerodynamics、Performance；Aston Martin 也曾公开把 Performance、Engineering 和 Technical responsibility 分开。[McLaren 2023 organisational changes](https://www.mclaren.com/racing/formula-1/2023/mclaren-formula-1-team-announces-organisational-changes/)；[Aston Martin technical structure](https://www.astonmartinf1.com/en-GB/news/announcement/explained-aston-martin-cognizant-formula-one-tm-teams-new-technical)
3. **赛道岗位与工厂研发岗位分开。** `trackside-aero-engineer` 不等于 `aerodynamics-development-engineer`；`tyre-performance-engineer` 不等于 `tyre-modelling-engineer`。
4. **不要用人物背景制造岗位。** Team Principal 是否有工程背景是人物属性，不是工程岗位族。
5. **不强求每队都有同名槽位。** 车队规模、外包和动力单元供应关系不同；模板表示岗位族存在，不表示每队组织图必须一一对应。
6. **公开证据不足时保留 family-level 映射。** 例如只公开 `Technical Director` 而没有 remit 时，先映射到 `technical-executive`，不要猜为气动或设计负责人。

## 可执行岗位矩阵

优先级含义：`P0` 为修复当前错误合并或职业路径核心缺口；`P1` 为第二批扩展；`P2` 为保留/清理规则。建议 title 为英文 UI 主标题，中文可在落库时按同一岗位族翻译。

| Priority | Action | Recommended `role_key` | Normalized role / aliases | 职责边界与映射规则 | 当前模板迁移 |
| --- | --- | --- | --- | --- | --- |
| P0 | Replace | `technical-executive` | Chief Technical Officer / overall Technical Director | 对整车开发、技术战略和工具体系负总责；仅在公开 remit 是全局时使用。Aston Martin 对 CTO 的公开定义覆盖 concept、aero、vehicle dynamics、wind tunnel、CFD 和 validation tools。[Aston Martin CTO interview](https://www.astonmartinf1.com/en-GB/news/feature/undercut-enrico-cardile?rendr_audience=public%2C+non-connected) | 从 `technical-leadership` 拆出 |
| P0 | Add | `technical-director-engineering-design` | Technical Director, Engineering / Engineering Director | 负责工程设计、结构、可靠性、R&D 或 factory engineering support；不要与全局 CTO 合并。[McLaren Rob Marshall appointment](https://www.mclaren.com/racing/formula-1/2023/rob-marshall-to-join-mclaren-formula-1-team-as-technical-director-engineering-design/)；[Aston Martin technical structure](https://www.astonmartinf1.com/en-GB/news/announcement/explained-aston-martin-cognizant-formula-one-tm-teams-new-technical) | 从 `technical-leadership` 拆出 |
| P0 | Add | `technical-director-aerodynamics` | Technical Director, Aerodynamics / Head of Aerodynamics | 负责整个 aero function 或 aero development；只有部门负责人进入该 key，普通 aerodynamicist 不进入。[McLaren Peter Prodromou profile](https://www.mclaren.com/racing/team/peter-prodromou/) | 从 `technical-leadership` 拆出 |
| P0 | Add | `technical-director-performance` | Technical Director, Performance / Performance Director | 负责 vehicle/car performance、performance simulation/software 或 factory-to-track performance；与 race engineer 管理线区分。[McLaren 2024 organisational update](https://www.mclaren.com/racing/formula-1/2024/mclaren-formula-1-team-announces-organisational-updates/)；[Aston Martin technical structure](https://www.astonmartinf1.com/en-GB/news/announcement/explained-aston-martin-cognizant-formula-one-tm-teams-new-technical) | 从 `technical-leadership` 拆出 |
| P1 | Add | `chief-designer` | Chief Designer / Head of Car Design | 整车架构与设计协调领导岗；不等同于 CTO，也不等同于单一 mechanical design engineer。McLaren 当前公开结构同时存在 Chief Designer 与 performance/aero technical leadership。[McLaren MCL40 2026 technical feature](https://www.mclaren.com/racing/formula-1/2026/behind-the-design-of-the-mcl40/) | 从 `technical-leadership` 拆出 |
| P2 | Retire as role | `team-principal` | Team Principal | 可保留在管理层数据，但 `engineering_authority` / `engineering_background` 应为人物属性。Haas 官方公告说明 Komatsu 从工程岗晋升并把 engineering 放在管理核心，这证明的是背景和授权，不构成一种独立工程职位。[Haas Komatsu appointment](https://www.haasf1team.com/news/moneygram-haas-f1-team-appoints-ayao-komatsu-team-principal) | 退役 `engineering-principal` |
| P0 | Normalize | `head-trackside-engineering` | Head/Director of Race Engineering / Trackside Engineering Director | 统筹两车赛道性能、工程标准及工厂支持。按 remit 映射；`Chief Race Engineer` 若实际管理全部 trackside engineering，也进入这里。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers)；[Haas Komatsu profile](https://www.haasf1team.com/season/team/ayao-komatsu) | 合并 `head-race-engineering`；条件迁移 `chief-race-engineer` |
| P1 | Add | `trackside-reliability-engineer` | Chief Engineer, Trackside / Trackside Reliability Engineer | 负责两车实时可靠性、技术合规和是否停车/降载的判断。不能仅凭 `Chief Engineer` title 映射，必须有 reliability/compliance remit。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers) | `chief-race-engineer` 的另一种职责映射 |
| P0 | Keep | `race-engineer` | Race Engineer | 单车 front-of-house、车手主联络、session plan、设定与跨团队协调。F1 官方说明 race engineer 与 performance engineer 是标准单车核心且职责不同。[F1 practice engineering guide](https://www.formula1.com/en/latest/article/the-insiders-guide-to-preparing-a-car-through-practice.5xWpgp8nsTh6PCowm7bDEE.5xWpgp8nsTh6PCowm7bDEE) | 保留 |
| P0 | Keep, clarify | `performance-engineer` | Performance Engineer / Car Performance Engineer | 单车遥测、驾驶与电子/性能子系统分析，向 race engineer 提供优化建议；不要泛化成所有 factory vehicle performance 工作。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers) | 保留，收紧定义 |
| P0 | Keep | `strategy-engineer` | Strategy Engineer / Strategist / Race Strategist | 进站、轮胎、对手、概率与情景决策；Head/Chief Strategy 可用同 family 加 seniority，而非再建一个技术完全相同的 key。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers) | 保留 |
| P0 | Add | `trackside-controls-engineer` | Controls Engineer, Race Team | 单车赛道控制参数、换挡/差速器等电子控制和可靠性支持；与 factory control algorithm development 分开。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers) | 从 `systems-controls-engineer` 拆出 |
| P1 | Rename | `trackside-power-unit-engineer` | Engine/PU Performance Engineer; Engine/PU Systems Engineer | 车队与 PU 供应方接口下的能量、模式、性能与系统可靠性赛道支持。Performance/Systems 可作为 specialty，不必先拆成两个 family。[Mercedes Trackside Engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers) | 重命名并收紧 `pu-engineer` |
| P0 | Add | `tyre-performance-engineer` | Tyre Engineer / Tyre Performance Engineer | 赛前预测、赛道温度/压力/退化监控及设定、策略支持；不包括纯轮胎建模研究。[Williams tyre roles](https://careers.williamsf1.com/blog/2025-10/exploring-the-role-of-tyre-jobs-in-formula-1) | 从 `tyre-aero-trackside` 拆出 |
| P0 | Add | `trackside-aero-engineer` | Trackside Aerodynamicist / Trackside Aero Engineer | 赛道气动数据、相关性、升级验证与 race support；与 CFD/风洞开发分开。[Williams Aerodynamics](https://careers.williamsf1.com/aerodynamics-jobs) | 从 `tyre-aero-trackside` 拆出 |
| P0 | Add | `aerodynamics-development-engineer` | Development Aerodynamicist / CFD Engineer / Aerothermal Engineer | 工厂气动概念、CFD、风洞、冷却气动开发。初版用一个 family，以 `specialty` 区分 development、CFD、aerothermal；不要为每个工具建顶层 key。[Williams Aerodynamics](https://careers.williamsf1.com/aerodynamics-jobs)；[Williams Senior Aerothermal Engineer](https://careers.williamsf1.com/job/senior-aerothermal-engineer-in-grove-jid-30) | 新增缺口 |
| P0 | Add | `mechanical-design-engineer` | Mechanical Design Engineer / Chassis, Bodywork & Wings / Suspension, Steering & Brakes | 从概念到详细 CAD、部件设计、制造与测试支持。子系统以 `specialty` 表示，不为 suspension、brakes、hydraulics 各建 family。[Williams mechanical design role](https://careers.williamsf1.com/blog/2026-3/responsibilities-of-an-f1-mechanical-design-engineer) | 新增缺口 |
| P0 | Add | `vehicle-dynamics-engineer` | Vehicle Dynamics / Vehicle Performance / Performance Optimisation Engineer | 车辆行为、属性目标、圈速/ride dynamics、设定和整车性能研究；与赛道单车 `performance-engineer` 通过 factory/trackside scope 区分。[Williams Performance Optimisation Engineer](https://careers.williamsf1.com/job/senior-performance-optimisation-engineer-in-grove-jid-134) | 从 `test-simulation-engineer` 拆出并补缺 |
| P0 | Add | `simulation-modelling-engineer` | Simulation Development / Simulation Concepts / Modelling Engineer | 开发物理模型、仿真方法、圈速与 ride simulation；工作产物是 model/tool/methodology，不是运行 DiL session。[Williams Simulation Development Engineer](https://careers.williamsf1.com/job/senior-simulation-development-engineer-in-grove-jid-196) | 从 `test-simulation-engineer` 拆出 |
| P0 | Add | `simulator-test-engineer` | DiL Test / Simulator Engineer / Simulator Operations Engineer | 规划、配置、执行驾驶员在环 session，维护 ECU/SECU 与设施集成；与模型开发分开。[Williams DiL Test Engineer](https://careers.williamsf1.com/job/dil-test-engineer-in-grove-wantage-jid-624) | 从 `test-simulation-engineer` 拆出 |
| P0 | Add | `systems-electronics-engineer` | Systems Engineer / Electronics Systems Engineer | 电气电子系统需求、架构、传感器、线束、数据记录与系统集成；不承担控制算法或通用数据平台的默认归类。[Williams Senior Systems Engineer](https://careers.williamsf1.com/job/senior-systems-engineer-in-grove-wantage-jid-363) | 从 `systems-controls-engineer` 拆出 |
| P0 | Add | `control-systems-engineer` | Control Systems / Embedded Controls Engineer | 工厂实时控制算法、模型、嵌入式软件、HiL 和部署；赛道支援只是职责之一，不等于 `trackside-controls-engineer`。[Williams Senior Control Systems Engineer](https://careers.williamsf1.com/job/senior-control-systems-engineer-in-grove-jid-167) | 从 `systems-controls-engineer` 拆出 |
| P1 | Add | `performance-software-data-engineer` | Performance Software / Data Processing / Engineering Data Engineer | 建设实时遥测处理、仿真、分析与决策工具；不要把企业 IT 或通用 UX 自动纳入。Williams 官方说明此类软件直接支持 aero、vehicle dynamics、real-time race data 和 performance analysis。[Williams Lead Software Engineer](https://careers.williamsf1.com/job/lead-software-engineer-in-grove-wantage-jid-562)；[Data Processing Software Engineer](https://careers.williamsf1.com/job/data-processing-software-engineer-in-grove-jid-177) | 从 `systems-controls-engineer` 的“data”语义拆出 |
| P1 | Add | `reliability-validation-engineer` | Reliability / Test & Validation / Structural Integrity Engineer | 工厂故障分析、寿命/强度、rig validation 与设计反馈；若 title 只是 quality/process 且无车辆技术 remit，则不进入。Aston Martin 的公开结构把 Structures、Reliability、R&D 置于 Engineering Director 范围；Williams Vehicle Engineering 也明确列出 structural integrity、materials fault analysis 和 test/validation。[Aston Martin technical structure](https://www.astonmartinf1.com/en-GB/news/announcement/explained-aston-martin-cognizant-formula-one-tm-teams-new-technical)；[Williams Vehicle Engineering placement](https://careers.williamsf1.com/job/vehicle-engineering-industrial-placement-in-grove-jid-278) | 新增缺口 |
| P1 | Add | `power-unit-integration-engineer` | Power Unit Integration / Powertrain Design Engineer | 车队侧 PU 包装、冷却、接口、变速箱壳体及 chassis integration；不同于 PU 厂的核心燃烧/电机研发，也不同于赛道 PU engineer。[Williams PUI Design Engineer](https://careers.williamsf1.com/job/senior-design-engineer-mechanical-pui-in-grove-wantage-jid-402) | 新增缺口；不并入 `pu-engineer` |
| P1 | Add specialty | `tyre-modelling-engineer` | Tyre Science / Tyre Modelling Engineer | 建立轮胎物理模型、参数化、相关性与仿真工具。技能路径足够独立，且 Williams 将其置于 Vehicle Dynamics/Tyre Science；不要和赛道 tyre engineer 合并。[Williams Tyre Modelling Engineer](https://careers.williamsf1.com/job/tyre-modelling-engineer-in-grove-jid-94) | 从 `test-simulation-engineer` 与 `tyre-aero-trackside` 的交叉处新增 |

## 建议的数据判定字段

为了让上述 keys 跨车队可用，模板或后续人员映射至少应能表达以下维度；这些是分类字段建议，不是本次数据修改：

| Field | Allowed values / example | Purpose |
| --- | --- | --- |
| `role_key` | 矩阵中的规范 key | 稳定岗位族 |
| `scope` | `executive`, `factory`, `trackside`, `car`, `remote-support` | 区分同名岗位的工作环境与责任范围 |
| `discipline` | `aerodynamics`, `vehicle-dynamics`, `design`, `controls`, `strategy` 等 | 支持导航与职业路径聚合 |
| `specialty` | `CFD`, `aerothermal`, `SSB`, `PUI`, `tyre-science` 等 | 避免为每个子系统制造顶层 key |
| `seniority` | `entry`, `engineer`, `senior`, `principal`, `head`, `director`, `executive` | 把层级从 title 字符串中分离 |
| `title_raw` | 官方原始 title | 保留来源忠实度和各队差异 |
| `remit_evidence` | 官方职责页或任命链接 | 解决 `Chief Engineer`、`Technical Director` 等歧义 title |

建议采用“先 remit，后 title”的映射顺序：

1. 有官方职责描述：按职责映射 `role_key`，原 title 存入 `title_raw`。
2. 只有明确专业 title（如 `Tyre Performance Engineer`）：按专业映射，`scope` 不确定时留空。
3. 只有宽泛 title（如 `Technical Director`、`Chief Engineer`）：映射到最宽的可靠 family，或保持 unresolved；不得猜测具体专业。
4. 同一人兼任多个真实责任域：允许多个 role assignment，不创建拼接 key。

## 不建议进入首批 `role_templates` 的范围

以下岗位确实存在于 F1 公开招聘中，但若当前仪表盘目标仍是“通向赛道/赛车性能工程的职业路径”，建议先作为第二层 taxonomy，而不是继续扩大首页模板：

- Model Maker、composites manufacturing、machining、assembly、production control
- Methods Engineering、Design Quality、Quality Inspection
- Inventory、logistics、procurement、garage equipment
- Enterprise IT、cybersecurity、通用产品/UX、商业数据
- Sporting Director、Team Coordinator、Chief Mechanic 等非工程或边界岗位

Williams 官方 careers 把 manufacturing、assembly、quality、test、inventory/logistics 放在 Operations 范围，而 Mercedes 也把 Technical、Operations、Race Team 分成不同组织入口。这些岗位应保留在更完整的 F1 workforce taxonomy 中，但不应与本矩阵的 engineering/performance role families 混为同一层。[Williams graduate opportunities](https://careers.williamsf1.com/graduate-opportunities)；[Mercedes careers teams](https://www.mercedesamgf1.com/careers/team)

## 推荐实施顺序

1. **第一批修正错误语义：** 退役 `engineering-principal`；拆分 `tyre-aero-trackside`、`systems-controls-engineer`、`test-simulation-engineer`；保留并收紧 `race-engineer`、`performance-engineer`、`strategy-engineer`。
2. **第一批补核心职业路径：** 加入 `aerodynamics-development-engineer`、`mechanical-design-engineer`、`vehicle-dynamics-engineer`、`simulation-modelling-engineer`、`simulator-test-engineer`、`systems-electronics-engineer`、`control-systems-engineer`。
3. **按 remit 重做领导层：** 用 `technical-executive` 加 Engineering/Design、Aerodynamics、Performance 三个 domain leadership keys；`Chief Designer` 独立；不根据 title 自动推断。
4. **第二批补数字化与交付链：** 加入 `performance-software-data-engineer`、`reliability-validation-engineer`、`power-unit-integration-engineer`、`tyre-modelling-engineer`。
5. **最后再迁移具体人：** 本研究不搜索各队完整人员名单。迁移现有人物时逐条读取已有官方来源的 remit；证据不足的宽泛 title 保持 unresolved，不为填满矩阵而猜测。

## 来源质量与限制

- 本研究只采用 Formula 1、F1 车队官网、车队官方 careers/任命/技术专题。没有使用媒体报道或 LinkedIn 作为岗位分类依据。
- Williams careers 提供了截至研究日最完整、最接近 2026 的公开岗位结构，因此承担了较多 practitioner-level 分类证据；McLaren、Aston Martin、Haas、Mercedes 的官方材料用于交叉验证领导层和赛道组织，避免把单一车队的命名直接当成全 F1 标准。
- 车队组织会变，旧官方页面可证明某类职责和组织边界真实存在，但不能证明页面中的人员仍任同一职位。本研究不据此更新任何 2026 人员名单。
- 公开 title 并无全行业统一语义，尤其是 `Chief Engineer`、`Chief Race Engineer`、`Performance Director` 和 `Technical Director`。因此矩阵刻意采用 remit-based normalization，而不是 title dictionary 的一对一替换。
