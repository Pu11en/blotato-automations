# larashero3-dotcom/writing-dna-skill (写作蒸馏器): six-layer Writing DNA distiller

- **Source URL:** https://github.com/larashero3-dotcom/writing-dna-skill
- **Commit:** ee3d97ee27268004b5187d97711161f44fc4aae4 (2026-08-24)
- **Author:** larashero3-dotcom ('lieflat'); account created 2026-02
- **License:** MIT
- **Stars / last push (checked 2026-09-18):** 1,965 stars, 191 forks / 2026-08-24 (repo created 2026-06-27: fast star growth, typical of Chinese AI-skill virality; not proof of output quality)
- **Evidence of success:** Most-starred style-distillation skill found. No published before/after evaluation. Self-check target: DNA doc lets a new writer hit '70/100' likeness; writes at >=7/10.
- **Covers in our flow:** Style extraction (L1 language stats, L2 structure/hook annotation, L3-L5 topic logic and cognitive frame) + a strict 'how to write with the DNA' step (read all layer files + 5 closest raw samples before writing; 'copy the writing method, never the content').
- **Caveats:** Built for articles (20+ samples), not spoken video; L6 visual layer is about article images. Main SKILL.md is Chinese; the English workflow file is included in full.

Text below is copied verbatim from the repo (no edits). Fences use five backticks so inner code blocks survive.

## Verbatim: `references/workflow.en.md (English workflow)`

`````markdown
# Writing DNA Distiller

> Skill name: `writing-dna-skill`
>
> Use this workflow for English-language artifacts and the templates in `templates/author-corpus/en/`.

## Goal

Distill a reusable Writing DNA from the historical work of an author, publication, brand, or account. The result must be an operational rule set rather than a summary.

Use the distilled artifacts to:

1. Understand the subject's language, editorial judgment, topic logic, and visual presentation.
2. Produce style-consistent drafts without claiming they were written by the original author.
3. Compare how different authors or publications approach the same subject.

## Six Layers

| Layer | Analyze | Method | Main Output |
| --- | --- | --- | --- |
| L1 Surface Language | Vocabulary, sentence length, punctuation, rhetoric | Text statistics and close reading | `language-dna.md` |
| L2 Article Structure | Hooks, body architecture, transitions, endings | Structural annotation | `structure-patterns.md` |
| L3 Topic Logic | Timing, angle selection, priorities, exclusions | Classification and synthesis | `cognitive-framework.md` |
| L4 Source Strategy | Authorities, examples, data, screenshots | Source-role analysis | `cognitive-framework.md` |
| L5 Cognitive Frames | Values, assumptions, recurring propositions | Deep reading | `cognitive-framework.md` |
| L6 Visual Style | Images, layout, typography, color | Visual sampling and formatting analysis | `visual-style-guide.md` |

L1-L2 describe how the subject writes. L3-L5 describe how the subject selects and interprets material. L6 describes how the work is presented.

## Image Evidence

Images may carry evidence that is absent from the prose. Open and inspect screenshots, comments, conversations, charts, tables, and interface captures.

For image-heavy corpora, inspect every image in a representative sample of at least 5-10 articles. Record whether each image is evidentiary, explanatory, data-bearing, narrative, emotional, authoritative, or decorative.

## Step 1: Collect The Corpus

- Collect at least 20 complete articles.
- Prefer coverage across different periods, topics, and formats.
- Store `.md` or `.txt` files in `raw/` or `raw-corpus/`.
- Preserve images and meaningful formatting when available.
- Do not publish source material without permission.

Recommended filename format:

```text
YYYY-MM-DD article-type article-title-source.md
```

If the corpus is too small, present the result as a workflow demonstration rather than a reliable style model.

## Step 2: Build Metadata

Create one `_meta/` record per article. Include:

```json
{
  "title": "Article title",
  "date": "YYYY-MM-DD",
  "author": "Author or publication",
  "column": "Series or column name",
  "article_type": "interview | analysis | commentary | observation | review",
  "topic_tags": ["tag-1", "tag-2"],
  "hook_type": "question | scene | data | assertion | suspense",
  "structure_pattern": "thesis-body-conclusion | chronology | comparison | Q&A",
  "source_types": ["primary source", "public reference", "case comparison"],
  "word_count": 0,
  "notable": "Optional notable traits"
}
```

Do not skip metadata. It is the basis for cross-article comparison.

## Step 3: Analyze Surface Language

Measure and interpret:

- recurring nouns, verbs, modifiers, phrases, and terminology
- sentence-length distribution and paragraph rhythm
- short-sentence and long-sentence ratios
- punctuation, quotation, parenthetical, and dash habits
- heading length and title construction
- formality, directness, humor, and mixed-language habits

Do not treat frequency alone as style. Distinguish topic vocabulary from stable voice markers.

Write `language-dna.md`.

## Step 4: Extract Structure Patterns

Annotate each article as:

```text
[opening hook and length]
→ [first turn or central question]
→ [body architecture]
→ [transition pattern]
→ [closing pattern]
```

Group recurring structures by content type. For every structure, record when it is used, what reader expectation it creates, and which variations are allowed.

Write `structure-patterns.md` with at least three recurring structures when the corpus supports them.

## Step 5: Distill Topic Logic And Cognitive Frames

Analyze three connected layers.

### Topic Logic

- Which events or moments trigger publication?
- Which angles are preferred?
- Which topics are ignored or rejected?
- Does the subject lead, follow, reinterpret, or retrospectively explain a conversation?

### Source Strategy

- Which types of sources carry authority?
- How are examples, data, anecdotes, and counterexamples used?
- How is uncertainty or controversial information handled?
- What role do screenshots and other visual evidence play?

### Cognitive Frames

- What recurring assumptions shape interpretation?
- Which values determine what counts as good, bad, important, or credible?
- Which non-obvious propositions recur across unrelated topics?

Write `cognitive-framework.md`. Separate evidence-supported patterns from tentative inferences.

## Step 6: Analyze Visual Style

Record:

- image count, placement rhythm, and image-to-text ratio
- cover-image and illustration patterns
- screenshot, chart, photo, interface, meme, and decorative-image usage
- heading hierarchy, paragraph density, bolding, quotations, and separators
- recurring colors, highlight conventions, backgrounds, and callouts
- the division of labor between prose and images

When HTML is available, inspect typography and color properties. When only Markdown is available, analyze headings, emphasis, quotations, links, and image placement.

Write `visual-style-guide.md`.

## Step 7: Integrate Writing DNA

Combine the findings into `Writing-DNA.md`:

```text
Writing-DNA.md
├── Language characteristics
├── Structure patterns
├── Topic-selection rules
├── Source strategy
├── Core cognitive frames
└── Visual style
```

Keep the document concise enough to reread before every writing task. Preserve the most predictive rules, meaningful exceptions, and clear failure modes.

## Output Structure

```text
author-or-publication/
├── raw/
├── _meta/
├── language-dna.md
├── structure-patterns.md
├── cognitive-framework.md
├── visual-style-guide.md
└── Writing-DNA.md
```

## Quality Checks

- Metadata covers at least 80 percent of the corpus.
- Structure patterns cover at least three content types when supported by the corpus.
- The cognitive analysis contains at least three non-obvious, evidence-backed propositions.
- The visual analysis covers images, layout, typography, and color when those signals exist.
- `Writing-DNA.md` is concise, operational, and internally consistent.
- A draft written from the artifacts can be audited against explicit rules rather than a vague similarity judgment.
- Public output does not impersonate the source author or misrepresent authorship.

## Writing With The Artifacts

Once distillation is done, **complete the reading steps below before every writing task**. Do not write from `Writing-DNA.md` alone, and do not rely on memory from an earlier turn: the integrated document holds compressed conclusions, while the actual cadence, sentence lengths, transitions, and punctuation habits live in the layered artifacts and the source articles.

### Required Reading Before Each Draft

**First, read every artifact** (four layered files plus the integrated document; skip none):

| File | What to take from it |
| - | - |
| `language-dna.md` | Frequent words, sentence-length distribution, punctuation habits |
| `structure-patterns.md` | The pattern matching this piece's content type |
| `cognitive-framework.md` | Angle of entry, source preferences, core propositions |
| `visual-style-guide.md` | Image placement and type, bold density, paragraph rhythm, section breaks |
| `Writing-DNA.md` | Overall constraints and priorities |

**Second, read 5 relevant articles from `raw/`.** Pick the five closest to this piece in content type and subject:

1. Filter on `article_type` and `topic_tags` in `_meta/` first.
2. When more than five match, take the five most recent — recent work better represents the current style.
3. When fewer than five match, fill up to five with the same content type on different subjects.
4. When `_meta/` is missing or incomplete, judge from the dates and titles in the filenames.

Reading the source articles is not about harvesting material; it calibrates what the layered artifacts cannot describe: how sentences actually breathe, how paragraphs connect, when a short sentence lands, how spoken and written registers mix. **Be able to state what these five share in voice** before drafting.

### Priority When Rules Conflict

1. The user's explicit instructions for this piece (subject, length, platform, language)
2. The structure pattern matching the current content type
3. Language characteristics and visual style
4. Cognitive frames — these drive stance and source selection, not sentence construction

Specific claims and facts from the source articles **must not be carried into the new piece**. You are reproducing how the author writes, not what they wrote.

### After Drafting

Clean AI writing tells from the finished draft using the rules in `skills/lieflat-less-ai-tone/`. It rewrites against an explicit whitelist, leaves unmatched text untouched, and does not restructure the piece.

**When the distilled artifacts conflict with the AI-tell rules, the artifacts win** — that is how the target author actually writes, not an AI tell.

`````

## Verbatim: `SKILL.md (Chinese original)`

`````markdown
---
name: writing-dna-skill
description: 从至少 20 篇完整文章中蒸馏可复用的写作 DNA，分析语言、文章结构、选题逻辑、素材策略、认知框架和视觉风格，并生成 Writing-DNA.md；按该 DNA 写作时会读取全部蒸馏产物和 5 篇相关原文。用于中英文作者、账号、品牌或出版物的风格分析与一致性写作。 Distill reusable Writing DNA from at least 20 complete articles for Chinese or English authors, publications, brands, and accounts; use for language, structure, topic logic, source strategy, cognitive-frame, and visual-style analysis.
---

# 写作蒸馏器.skill

> 英文名：`writing-dna-skill`

## 使用语言与模板

将“对话语言”和“产物语言”分开处理：

1. 使用用户的对话语言进行交互，除非用户明确指定其他语言。
2. 用户明确指定产物语言时，以用户选择为准。
3. 未指定时，使用原始语料的主要语言。
4. 语料混合且无法判断时，使用对话语言。

中文产物使用 `templates/author-corpus/zh/`。英文产物使用 `templates/author-corpus/en/`，并按需读取 `references/workflow.en.md` 以获取英文文件名和表达规范。

| 分析产物 | 中文文件名 | 英文文件名 |
| - | - | - |
| L1 语言 DNA | `语言DNA.md` | `language-dna.md` |
| L2 文章结构 | `文章结构模板.md` | `structure-patterns.md` |
| L3-L5 认知框架 | `写作视角与认知框架.md` | `cognitive-framework.md` |
| L6 视觉风格 | `视觉风格指南.md` | `visual-style-guide.md` |
| 最终整合文档 | `Writing-DNA.md` | `Writing-DNA.md` |

下文中出现产物文件名时，始终根据已选定的产物语言使用上表对应的文件名。

## 一、目标

从某个账号/作者的历史文章中，提炼出可复用的**写作 DNA**——不是摘要，而是可操作的规则集，用于：

1. **理解** 该账号/作者的写作视角、选题逻辑、语言风格
2. **复刻** 该账号/作者的写作风格（输出近似风格的文章）
3. **对比** 不同账号/作者在同一议题上的表达差异

---

## 二、蒸馏的六个层次

| 层次 | 分析对象 | 提取方法 | 输出形式 |
| - | - | - | - |
| **L1 表层语言** | 词频、句长、标点、修辞 | 脚本统计 | 词频表 + 句式清单 |
| **L2 文章结构** | 开头 hook、正文架构、结尾收束 | 人工标注 | 结构模板（按类型分类） |
| **L3 选题逻辑** | 发布时机、切入角度、话题优先级 | 归纳分类 | 选题判断树 |
| **L4 素材策略** | 引用来源类型、权威对象选取标准、数据使用方式 | 阅读归纳 | 素材偏好清单 |
| **L5 认知框架** | 作者的世界观、价值判断、对主题的核心假设 | 深度阅读 | 核心命题列表 |
| **L6 视觉风格** | 配图策略、排版格式、字体层级、色彩使用 | 图文统计 + 截图采样 | 视觉风格指南 |

> **原则**：L1-L2 是"怎么写"，L3-L5 是"怎么想"，L6 是"怎么呈现"。完整的风格复刻需要三者结合。

### 跨层原则：图片内容必须纳入分析

许多文章的图片不是装饰——截图、对话记录、数据表格、用户评论中的文字是论证链的一部分。分析时必须**打开图片查看内容**，否则会遗漏：

- **L2 文章结构**：截图在叙事中的承重角色（转折点在截图里、证据链由截图构成）
- **L4 素材策略**：截图是核心素材形式，精确数据往往只存在于图片中
- **L6 视觉风格**：图片的功能分类（证据型/演示型/数据型/叙事推进型/情绪型）和图文协作模式

**执行要求**：Step 3-6 的分析中，至少抽样 5-10 篇文章逐张查看图片内容，评估图片携带的实质性信息比例。

---

## 三、工作流程

### Step 1：原始素材收集

**目标**：建立该账号/作者的文章语料库

- 收集渠道：公众号、博客、Newsletter、官网、社交平台等历史文章
- 数量建议：至少 20 篇完整文章
- 文件格式：`.md` 或 `.txt`，存入对应目录的 `raw/` 或 `raw-corpus/` 文件夹
- 覆盖范围：尽量包含不同时期、不同类型的文章（访谈 / 深度 / 短评）

**文件命名规范**：

```
YYYY-MM-DD 内容类型 文章标题-来源.md
```

---

### Step 2：元数据标注（`_meta/` 目录）

为每篇文章创建元数据记录，字段如下：

```json
{
  "title": "文章标题",
  "date": "YYYY-MM-DD",
  "author": "作者姓名",
  "column": "内容系列名称",
  "article_type": "访谈 | 深度分析 | 短评 | 观察 | 综述",
  "topic_tags": ["AI", "创业", "商业模式"],
  "hook_type": "问题式 | 场景式 | 数据式 | 观点式 | 悬念式",
  "structure_pattern": "总-分-总 | 时间线 | 对比式 | Q&A",
  "source_types": ["一手素材", "公开资料", "案例对比"],
  "word_count": 3200,
  "notable": "值得标注的特殊之处（可留空）"
}
```

> 元数据是后续统计分析和规律归纳的基础，不可跳过。

---

### Step 3：脚本分析（L1 表层语言）

运行以下分析，提取表层语言特征：

**词频分析**

- 高频名词（100 个）
- 高频动词（50 个）
- 高频副词（过度使用的副词 = 需要过滤的噪声）

**句式分析**

- 平均句长（字符数）
- 短句（≤15字）占比
- 长句（≥50字）占比
- 段落平均句数

**标点与格式**

- 破折号 vs 括号的使用比
- 引号使用场景
- 小标题平均字数
- 中英文混用模式

**输出**：中文产物写入 `语言DNA.md`；英文产物写入 `language-dna.md`。内容包含词频表和句式规律总结。

---

### Step 4：结构标注（L2 文章结构）

对每篇文章人工标注结构骨架，记录：

```
[开头 hook 类型] + [字数]
→ [第一转折点/核心问题引入]
→ [正文结构：总-分 / 对比 / 时间线 / Q&A]
→ [结尾处理方式：收束 / 悬念 / 呼吁 / 自然结束]
```

归纳后，按**内容类型**整理为可复用的结构模板，例如：

**访谈类模板**：

```
引题段（150-300字）
  → 为什么此时此人值得聊（1句）
  → 关键背景（2-3句）
  → 本篇核心问题（1-2句）
正文 Q&A
  → 每个大话题前有小标题（4-8字）
  → 每小节 3-6 轮对话
结尾
  → 多为自然收束，无刻意升华
```

**输出**：中文产物写入 `文章结构模板.md`；英文产物写入 `structure-patterns.md`。按内容类型分类。

---

### Step 5：选题与认知框架归纳（L3-L5）

这是最需要深度阅读的部分，无法用脚本替代。

**选题逻辑归纳**（L3）

- 他们倾向于在什么时机切入？（早期判断 / 跟进分析 / 事后复盘）
- 同一话题，他们的切入角度是什么？（当事人视角 / 读者视角 / 系统视角）
- 什么类型的话题他们不写？

**素材策略**（L4）

- 主要依赖哪类素材？（一手观察 / 二手整理 / 数据引用）
- 权威对象选取标准是什么？
- 如何处理敏感或争议性信息？
- **图片作为素材**：截图在论证中承担什么角色？（纯配图 vs 承重结构）精确数据是否只存在于截图中？图文之间的协作模式是什么？

**认知框架**（L5）

- 该账号/作者对主题的核心假设是什么？
- 反复出现的核心命题（3-5 条）
- 他们认为什么是"好对象"、"好作品"？

**输出**：中文产物写入 `写作视角与认知框架.md`；英文产物写入 `cognitive-framework.md`。

---

### Step 6：视觉风格与排版分析（L6）

这一层分析文章的视觉呈现——读者看到的不只是文字，还有图片节奏、字体层级、排版密度。风格复刻如果只复刻文字而忽略视觉，出来的东西"读着像但看着不像"。

**配图策略**

- 图文比：每篇文章平均配图数量、图片间距（每隔多少段落出现一张图）
- 图片类型分布：界面截图 / 数据图表 / 人物照 / 概念示意图 / meme / 纯装饰
- 首图风格：是否有封面图？风格是实拍、插画还是纯文字排版？
- 图片来源模式：原创拍摄 / 官方素材 / 网络素材 / AI 生成
- **图片功能分类**（需逐张查看图片内容）：证据型（社交截图/对话/评论）/ 演示型（界面/过程/代码输出）/ 数据型（排行榜/图表）/ 叙事推进型（故事转折在图中）/ 情绪型（meme）/ 权威型（论文/人物照）
- **图文协作模式**：文字和图片如何分工？（引导语→截图→解读？截图即论证？文字概括+截图精确？）

**排版格式**

- 字号层级：正文字号、标题字号、引用/注释字号（从 HTML `font-size` 提取）
- 加粗使用频率：每千字加粗次数、加粗用于强调关键词还是整句
- 段落长度：平均段落字数、是否有刻意的短段落节奏（如一句一段）
- 分隔方式：用小标题分段 / 用分隔线 / 用空行 / 用加粗句作为"隐性标题"

**色彩与强调**

- 是否使用彩色文字？用于什么场景？（重点标注 / 链接 / 引用）
- 背景色块的使用：灰底引用框 / 高亮色块 / 代码块样式
- 整体色调倾向：素净黑白 / 彩色活泼 / 深色主题

**提取方法**

- 如有原始 HTML：统计 `font-size`、`font-weight`、`color`、`background` 属性分布
- 如仅有 Markdown：从 `**`（加粗）、`##`（标题）、`>`（引用）、`![]()`（图片）等标记提取排版规律
- **必做**：抽样 5-10 篇文章逐张打开图片，分析图片功能类型和图文协作模式
- 统计图片数量、位置分布、功能分类占比

**输出**：中文产物写入 `视觉风格指南.md`；英文产物写入 `visual-style-guide.md`。内容包含配图策略、排版规律和色彩使用总结。

---

### Step 7：蒸馏产物整合

将以上分析整合为一份可直接用于 AI 复刻的文档：

```
写作 DNA 文档（Writing-DNA.md）
├── 语言特征（来自 L1）
├── 结构模板（来自 L2，按类型分类）
├── 选题判断标准（来自 L3）
├── 素材使用规范（来自 L4）
├── 核心认知框架（来自 L5）
└── 视觉风格指南（来自 L6：配图策略 + 排版 + 色彩）
```

这份文档应满足：​**给任何一个没读过该账号/作者的人，他读完下笔能写出 70 分的近似风格文章——不仅文字像，视觉呈现也像。**

---

## 四、目录结构规范

（本节说明蒸馏产物的存放位置，写作阶段的使用方式见第六节。）

每个账号或作者目录建议采用以下结构。中文产物使用左侧文件名，英文产物使用括号中的英文文件名：

```
账号或作者名称/
├── raw/                    # 原始文章语料（.md 格式）
├── _meta/                  # 元数据标注（JSON 或 .md）
├── 语言DNA.md              # English: language-dna.md
├── 文章结构模板.md          # English: structure-patterns.md
├── 写作视角与认知框架.md    # English: cognitive-framework.md
├── 视觉风格指南.md          # English: visual-style-guide.md
├── Writing-DNA.md          # 最终整合文档（可直接嵌入 skill）
└── index.html              # 可选：可视化展示页面
```

---

## 五、质量标准

蒸馏产物完成后，用以下标准自检：

- [ ] 给 AI 喂入 Writing-DNA.md，能否写出该账号/作者风格的文章（评分 ≥7/10）
- [ ] L2 结构模板覆盖了该账号/作者至少 3 种内容类型
- [ ] L5 认知框架提炼出至少 3 条非显而易见的核心命题
- [ ] 元数据覆盖至少 80% 的语料文章
- [ ] L6 视觉分析覆盖配图策略、排版格式、色彩使用三个维度
- [ ] Writing-DNA.md 单文档字数控制在 4000 字以内（过长 = 没蒸馏干净）

---

## 六、使用蒸馏产物写作

蒸馏完成后，每次按该 DNA 写作前，**必须先完成下面的读取步骤**。不允许只凭 `Writing-DNA.md` 或凭上一轮对话的记忆下笔——整合文档是压缩后的结论，具体的语感、句子长短、过渡方式和标点习惯只存在于分层产物和原文里。

### 6.1 每次写作前必读

**第一步：读完全部蒸馏产物**（四份分层产物 + 整合文档，一份都不能跳过）

| 读什么 | 中文文件名 | 英文文件名 | 提取什么 |
| - | - | - | - |
| L1 语言 | `语言DNA.md` | `language-dna.md` | 高频词、句长分布、标点习惯、中英混用方式 |
| L2 结构 | `文章结构模板.md` | `structure-patterns.md` | 匹配本次体裁的结构模板 |
| L3-L5 认知 | `写作视角与认知框架.md` | `cognitive-framework.md` | 切入角度、素材偏好、核心命题 |
| L6 视觉 | `视觉风格指南.md` | `visual-style-guide.md` | 配图位置与类型、加粗密度、段落节奏、分隔方式 |
| 整合 | `Writing-DNA.md` | `Writing-DNA.md` | 总体约束与优先级 |

**第二步：读 5 篇相关的 raw 原文**

从 `raw/` 中选 5 篇与本次写作**体裁和题材最接近**的文章通读。选取方式：

1. 优先用 `_meta/` 的 `article_type` 和 `topic_tags` 筛选匹配项
2. 匹配项超过 5 篇时，取时间最近的 5 篇（近期文章更代表当前风格）
3. 匹配项不足 5 篇时，用同体裁不同题材的文章补齐到 5 篇
4. `_meta/` 不完整或缺失时，直接按文件名中的日期和标题判断

读 raw 的目的不是找素材，而是校准分层产物里描述不出来的东西：句子的实际呼吸感、段落之间怎么接、什么时候突然用一个短句、口语和书面语怎么混。**读完要能说出这 5 篇的共同语感**，再开始写。

### 6.2 写作时的优先级

规则冲突时按此顺序取舍：

1. 用户的明确指令（本次要求的题材、长度、平台、语言）
2. L2 结构模板中匹配当前体裁的那一套
3. L1 语言特征与 L6 视觉风格
4. L3-L5 认知框架（决定观点立场和素材选择，不决定句式）

原文里的具体观点和事实**不能直接搬进新文章**——复刻的是写法，不是内容。

### 6.3 写完之后：清理 AI 痕迹

写作完成后，用 `skills/lieflat-less-ai-tone/` 的规则清理成稿中的 AI 痕迹。它采用白名单式改写，只处理规则清单内的问题，不改文章框架，也不覆盖本次写作已遵循的 DNA 特征。

**蒸馏产物与去 AI 味规则冲突时，以蒸馏产物为准**——那是目标作者的真实写法，不是 AI 痕迹。

`````
