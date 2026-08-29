# 策略型奇幻写作

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个面向 Codex 的写作 Skill，用于分析策略型长篇叙事、设计原创升级流奇幻故事、检验剧情因果，并生成贴合人物经历的原创古风叙事诗。

项目最初来自对用户合法提供的《蛊真人》EPUB 所做的高层结构研究。仓库不包含小说正文、模型权重或训练语料，也不会模仿原作作者的散文、诗歌或其他独特表达。

## 主要能力

- 从目标、资源、规则、信息、选择、代价和持续后果分析人物决策。
- 设计原创世界、资源闭环、人物、势力、冲突链和前 12 章大纲。
- 使用 20 分剧情压力测试检查对手是否合理、胜利是否有代价、因果是否延续。
- 根据人物阶段、关键转折和具体场景生成原创古风叙事诗。
- 将单独获取的 `chinese-poetry` JSON 数据整理为本地 SQLite 索引。
- 按情绪和意象检索古典作品，并检查诗歌字数、内部重复和可疑连续重合。

## 安装

```bash
git clone https://github.com/jeffxuan/strategic-fantasy-writing.git \
  ~/.codex/skills/strategic-fantasy-writing
```

安装后重启 Codex。

## 快速使用

分析原创章节：

```text
请使用 $strategic-fantasy-writing 分析下面的原创章节。
说明人物目标、资源、约束、信息差、代价和持续后果，
最后使用剧情压力测试评分，并给出两个最小修改方案。

原创章节：……
```

写贴合人物的古风诗：

```text
请使用 $strategic-fantasy-writing 为这个原创人物写一首七言四句古风短诗。
人物阶段：……
关键转折：……
出现位置：章末
必须出现的意象：残灯
避免使用：剑、血、天命
```

Skill 会区分两种执行状态：

- 提供本地诗词索引时，先检索古典参照，生成后再执行语料重合检查。
- 没有本地索引时，只执行结构化创作自检，并明确说明没有进行语料检索。

## 可选诗词索引

本仓库不会重新分发外部诗词数据。请单独获取数据并检查来源，再建立本地索引：

```bash
git clone https://github.com/chinese-poetry/chinese-poetry.git /path/to/chinese-poetry
python3 scripts/build_poetry_index.py \
  --source /path/to/chinese-poetry \
  --output /path/to/poetry.sqlite
```

默认索引以下诗词类目录：

- `全唐诗`
- `宋词`
- `诗经`
- `五代诗词`

也可以用多个 `--include` 参数自行选择目录。

## 检索与检查

按人物处境和意象检索古典参照：

```bash
python3 scripts/retrieve_poems.py \
  --index /path/to/poetry.sqlite \
  --query '少年 远行 春光 酒' \
  --top-k 5
```

检查七言四句草稿：

```bash
python3 scripts/check_poem.py \
  --index /path/to/poetry.sqlite \
  --text $'第一句\n第二句\n第三句\n第四句' \
  --expected-chars 7
```

检查器会报告：

- 每句实际字数；
- 每句句末字；
- 跨行重复短语；
- 与本地语料可疑的连续重合；
- 是否实际执行了语料检查。

它不会假装完成中古音韵、平仄或严格近体诗校验。需要使用“绝句”或“律诗”等严格标签时，还应接入经过核验的韵书与格律工具。

使用外部语料前，请阅读 [数据清单](references/DATA-MANIFEST.md)；完整诗歌流程见 [古风叙事诗模块](references/CLASSICAL-POETRY-MODULE.md)。

## 项目结构

```text
SKILL.md                    Skill 主入口与任务路由
agents/openai.yaml          Codex 界面元数据
references/                分任务写作方法、数据与来源说明
scripts/                   诗词索引、检索与检查工具
tests/                     可重复运行的工具测试
```

重要参考文件：

- [剧情弧卡片](references/ARC-CARDS.md)
- [行动者与势力模型](references/ACTOR-SYSTEMS.md)
- [原创故事工作流](references/ORIGINAL-STORY-WORKFLOW.md)
- [剧情压力测试](references/NARRATIVE-STRESS-TEST.md)
- [古风叙事诗模块](references/CLASSICAL-POETRY-MODULE.md)
- [未来 4090 训练计划](references/TRAINING-PLAN.md)

## 验证

运行工具测试：

```bash
python3 -m unittest discover -s tests -v
```

当前测试覆盖：

- 从 JSON 建立 SQLite 索引；
- 按意象检索作品；
- 检测连续措辞重合；
- 检测五言或七言的字数错误。

## 使用边界

- 当前项目是知识与工具 Skill，不是已经训练完成的诗歌模型。
- 不提供特定现代作者或作品的模仿、续写和轻度改写。
- 超出仓库来源锚点的原作分析，需要用户提供相应合法文本。
- `chinese-poetry` 仓库本身采用 MIT License，但其 README 说明底层数据来自互联网。训练或重新分发前仍需检查具体数据的来源与权利。
- 对虚构权谋的分析不能转化成现实中的欺骗、胁迫、暴力或违法操作指导。

## 许可证

本仓库中新编写的代码和文档使用 [MIT License](LICENSE)。外部作品与数据集继续受各自的权利和许可证约束。
