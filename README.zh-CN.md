# paddock-cv

> 逆向工程"围场工作是怎么得到的"——一份有出处的职业路径图谱，
> 覆盖 F1、F2、WEC / 勒芒、Formula E 与 F1 Academy 中可公开识别的赛道工程人员。

[English](./README.md) | 简体中文

**▶ [paddockcv.com](https://paddockcv.com)** —— 正式站点：完整真实数据集
（约 480 人、5 个系列赛），7 种语言。本仓库就是它的构建方式。

**知道站点缺了谁、或哪里写错了？**
[提交 person-info issue](../../issues/new?template=person-info.yml)，
附上来源链接——经核实的贡献会直接进入正式站点。
联系：[hello@paddockcv.com](mailto:hello@paddockcv.com)

选定一个围场岗位 → 找到当前所有在职者 → 逐个读懂他们怎么走到这里。
这就是全部方法论。本仓库是把这件事在 ~480 人 × 5 个系列赛规模上
可复刻化的工具链与方法文档。

## ⚠️ 数据说明

**真实数据集不在本仓库中，永远也不会在。** 它包含约 480 位在职人员的
聚合履历与本地缓存的编辑类照片——公开分发它是隐私与版权双重问题。
仓库中附带的是：

- `data/sample/` —— 一套明显**虚构**的示例数据（Alex Example 这类假名、
  假车队、example.com 来源），结构与真实数据 100% 同构，保证开箱即跑；
- **方法论**文档 —— 如何从公开来源构建你自己的数据集，这才是真正有价值的部分。

本项目与 FIA、Formula 1、FOM 及任何车队均无关联。

## 快速开始

需要 Python 3.10+（纯标准库，无需 pip），跑测试则需要 Node 20+。

```bash
git clone https://github.com/<you>/paddock-cv.git
cd paddock-cv

python3 scripts/make_sample_data.py                     # 生成虚构示例数据
F1E_DATA_DIR=data/sample python3 scripts/build_data.py  # 编译 web/data.json + data.js
F1E_DATA_DIR=data/sample python3 scripts/seed_db.py     # 构建 SQLite 层
F1E_DATA_DIR=data/sample python3 server.py              # http://localhost:8000
```

## 方法论（四层循环）

| 层 | 问题 | 主要信源 |
|---|---|---|
| L1 岗位 | 这个岗位做什么、在组织里的位置 | 车队 careers 博客、编辑访谈 |
| L2 名单 | 本赛季每支车队这个岗位是谁 | 赛季前瞻、官宣、转播口播——≥2 个独立信源交叉 |
| L3 履历 | 每个人怎么走到这个位置 | LinkedIn 公开摘要、大学校友专题、系列赛官方人物栏目 |
| L4 资产 | 头像，且身份绑定真正可验证 | 官方 CDN 命名图说、单主体专访头图——见绑定强度谱 |

搜索层是 AI 辅助的：LLM 研究代理通过 **[Tavily](https://tavily.com)**
（搜索 + 全文读取）和 **[Firecrawl](https://firecrawl.dev)**（结构化抽取）
逐岗位跑查询，把候选信源的产出规模拉到单人手工远达不到的量级。
但判断权在人：代理只负责*提出*，每条采纳/拒绝都过下面的信源规则，
且每条信息保留原始 URL——你完全可以不信任管线、自己复核。

两条铁律：

1. **宁缺毋假。** 找不到就留空，缺口本身作为数据记录。错误的脸比首字母占位符伤害大得多。
2. **每次采纳/拒绝都留痕。** 审计表（`lookup_runs`）是数据集的一部分，覆盖率声明可以被检验。

完整文档：[docs/SEARCH_METHODOLOGY.md](docs/SEARCH_METHODOLOGY.md)（中文）·
[docs/DATA_METHOD.md](docs/DATA_METHOD.md) ·
[docs/ROUTES.md](docs/ROUTES.md)（研究结论摘要）。

## 主要发现（来自真实数据集）

2026 F1 围场 26 位比赛工程师的履历显示：**15/26** 走"大学 → 初级方程式 →
F1"路线；**8/26** 以数据/性能工程师身份入行后转岗；赛车工程专业硕士
（Cranfield、Oxford Brookes）出现频率远高于其他任何履历项。方法论文档
展示了如何对任何其他围场岗位复刻这套统计。

## 许可

- **代码与文档：** [MIT](LICENSE)。
- **示例数据**（`data/sample/`）：[CC0](https://creativecommons.org/publicdomain/zero/1.0/)——它是虚构的。
- **你用这套工具构建的真实数据集：** 归你所有，也由你负责。
