# Gu Zhen Ren Narrative Analysis Skill

一个用于研究策略型长篇叙事，并协助创作独立原创奇幻故事的 Codex Skill。

它从用户提供的《蛊真人》EPUB 中提炼高层结构：资源约束、组织激励、信息差、计划更新、势力博弈与持续代价。它不包含小说正文，不复刻作者文风，也不生成原作续写。

本项目与原作作者、出版方及 `chinese-poetry` 项目均无隶属或背书关系。

## 内容

- `SKILL.md`：主入口，包含使用范围、核心模型与质量检查。
- `SOURCE-LEDGER.md`：材料元数据、章节锚点与证据规范。
- `references/ARC-CARDS.md`：十个剧情机制的分析卡片。
- `references/ACTOR-SYSTEMS.md`：人物、机构、势力和联盟的决策画布。
- `references/ORIGINAL-STORY-WORKFLOW.md`：从设定到前 12 章大纲的原创工作流。
- `references/NARRATIVE-STRESS-TEST.md`：20 分剧情逻辑压力测试。
- `references/CLASSICAL-POETRY-MODULE.md`：基于古典诗词意象与形式的原创古风叙事诗模块。

## 安装

将仓库克隆到 Codex 的个人 Skills 目录：

```bash
git clone https://github.com/jeffxuan/gu-zhen-ren-analysis-skill.git \
  ~/.codex/skills/gu-zhen-ren-narrative-analysis
```

重启 Codex 后即可加载。也可以只阅读 `SKILL.md` 与 `references/`，把它当作独立的创作方法手册使用。

## 快速使用

在对话中明确要求使用该 Skill，并提供原创剧情素材：

```text
请使用 gu-zhen-ren-narrative-analysis 分析下面的原创章节。
按“目标、资源、规则、信息、选项、代价、后果”输出，
最后用 20 分压力测试评分，并指出两个最小修改方案。

原创章节：……
```

生成古风叙事诗时，建议同时给出人物、转折、场景和禁用意象：

```text
请为这个原创人物写一首七言四句古风短诗。
人物：……
关键转折：……
出现位置：章末
必须出现：残灯
避免使用：剑、血、天命
```

## 使用原则

1. 只输出原创内容，不模仿或延续任何特定作者/小说。
2. 将“聪明”写成可推导的选择：目标、资源、规则、信息、代价与后果。
3. 结论要区分源材料观察与分析推断。
4. 古典诗词仅作形式、意象和题材参考；训练前必须核验每项数据的来源与权利。

## 当前边界

- 这是知识与提示词 Skill，不是已经训练完成的模型。
- 不包含《蛊真人》正文、章节摘要全集、训练数据或模型权重。
- 不提供特定作者模仿、原作续写或现实中的欺骗、操纵和伤害建议。
- `chinese-poetry` 仓库本身采用 MIT License，但其 README 说明底层数据来自互联网；用于模型训练前仍需逐项核查来源与权利。

## 训练状态

当前版本是检索与提示词优先的知识 Skill，不含模型权重或训练语料。后续若在 RTX 4090 上实验，训练目标应为独立原创的古风叙事诗生成，并建立数据清单、许可记录、保留集与相似度评估。

## License

本仓库内由本项目新写的文档采用 [MIT License](LICENSE)。外部材料、书籍与数据集仍分别受其自身权利和许可约束。
