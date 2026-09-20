# Mentor Match

[English](README.md) | [简体中文](README.zh-CN.md)

Mentor Match 是一个基于公开证据的 Agent Skill，用于寻找、核验、比较和持续关注研究导师、实验室、学术项目、博士后合作导师、科研助理岗位及资助机会。

它面向全球申请者，支持高校、公共或非营利研究机构，以及企业研究实验室。核心 Skill 遵循开放的 Agent Skills 目录结构，并封装为 ChatGPT/Codex 插件。

## 功能

- 读取简历和一次性申请问卷。
- 实时搜索网络，不内置容易过时的导师数据库。
- 可将检索范围限定在指定高校、学院、系所、研究机构或企业。
- 支持硕士、博士、博士后和科研助理申请。
- 区分已核实事实、合理推断、轶事性团队文化信号和未知信息。
- 使用公开、可调整的评分权重；团队文化信号最多占总分的 10%。
- 同时生成 Markdown、CSV 和 JSON 结果。
- 可制作申请前材料包，包括个性化联系邮件草稿、简历修改建议、研究计划切入点和个人陈述证据表。
- 在宿主支持定时任务时持续检查已保存名单，并只提醒有实际意义的变化。
- 在本地保存多个申请人档案、申请项目和不可变的历次检索记录。

Mentor Match 不保证录取、资助、受聘或获得回复。未经用户明确授权，它不会发送消息或提交申请表单。

## 项目结构

```text
mentor-match/
├── .codex-plugin/plugin.json
├── skills/mentor-match/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   ├── scripts/mentor_match.py
│   └── references/
├── scripts/mentor_match.py  # 仓库级便捷入口
├── tests/
├── evals/
├── submission/
├── PRIVACY.md
├── SECURITY.md
├── TERMS.md
└── LICENSE
```

## 使用方法

安装插件后，可以显式调用，也可以直接用自然语言提出需求：

```text
$mentor-match 根据我的简历寻找计算生物学方向的博士导师。
```

```text
在这三所大学中寻找适合我的机器人实验室，并生成完整的申请前材料包。
```

```text
刷新我保存的 2027 年博士后候选名单，只报告有实际意义的变化。
```

首次建立申请人档案时，Mentor Match 会一次性展示完整问卷。在首次持久化写入前，它会说明本地存储路径并请求一次知情同意。

## 本地数据

默认数据目录是 `~/.mentor-match/`。可通过 `MENTOR_MATCH_HOME` 环境变量或 `--root` 参数修改。

随附的管理脚本只使用 Python 标准库：

```bash
python scripts/mentor_match.py --help
python scripts/mentor_match.py init
python scripts/mentor_match.py init --accept-storage
python scripts/mentor_match.py list
```

第一次执行 `init` 只会说明存储内容，不会写入文件。第二条命令会记录用户同意并创建本地目录。导出、归档和永久删除命令可通过 `--help` 查看；破坏性命令必须提供完全匹配的申请人或申请项目 ID 作为确认。

## 研究来源

高校、项目、院系、实验室、导师、职位和资助机构的官方网站是主要证据来源。DOI 页面、Crossref、公开 ORCID 档案和 OpenAlex 记录等学术资料可用于交叉核验身份和近期研究方向。论坛、社交媒体和匿名评价只作为低置信度的团队文化信号，不视为已证实事实。

插件不强制要求任何 API 密钥。对于需要凭证或使用限制可能变化的可选数据源，它会自动降级到公开网页或其他证据。

## 开发与验证

运行确定性检查：

```bash
python -m unittest discover -s tests -v
python scripts/mentor_match.py validate path/to/candidates.json
```

打包前验证 Skill 和插件：

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/mentor-match
python /path/to/plugin-creator/scripts/validate_plugin.py .
```

行为评测提示和约束位于 `evals/`。提交审核所需的商店文案、测试案例和发布说明位于 `submission/`。发布者身份验证、审核门户权限、最终开放国家或地区以及正式发布仍由发布者操作。

## 隐私与使用条款

参见 [PRIVACY.md](PRIVACY.md)、[SECURITY.md](SECURITY.md) 和 [TERMS.md](TERMS.md)。问题与支持请求可提交至 [GitHub Issues](https://github.com/GPDdev/mentor-match/issues)，或发送邮件至 `hejiale@outlook.com`。

## 许可证

本项目采用 Apache License 2.0，详见 [LICENSE](LICENSE)。
