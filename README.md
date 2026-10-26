<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/profile-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/profile-light.svg">
  <img alt="Louisss — build quietly, ship often." src="assets/profile-light.svg" width="100%">
</picture>

**Backend engineering · AI agents · Open source**

我是 Louisss，专注 Java / Python 后端与 AI Agent 工程化。把重复的事做成工具，把真实的问题修进开源。

[我的作品](#selected-work) ↗ &nbsp; / &nbsp; [开源足迹](#open-source) ↗ &nbsp; / &nbsp; [玩一道 Debug 题](#debug-lab) ↗

### Selected work

<table>
<tr>
<td width="50%" valign="top">
<sub>01 / FIND THE RIGHT PROBLEM</sub>
<h3><a href="https://github.com/louisss1016/contrib-radar">Contrib Radar ↗</a></h3>
<p>找到值得投入的开源贡献：发现项目、筛选 Issue、检查冲突，持续跟进 PR。</p>
<p><code>Python</code> <code>Agent Skill</code></p>
<a href="https://github.com/louisss1016/contrib-radar#readme">探索项目 →</a>
</td>
<td width="50%" valign="top">
<sub>02 / BUILD WITH A PLAN</sub>
<h3><a href="https://github.com/louisss1016/vibecoding-navigator">Vibecoding Navigator ↗</a></h3>
<p>给 AI 编程一条清晰路线：从需求拆解、分步实现，到验收与上线。</p>
<p><code>Agent Workflow</code> <code>Developer Tools</code></p>
<a href="https://github.com/louisss1016/vibecoding-navigator/blob/main/docs/quickstart.md">跟着做一个项目 →</a>
</td>
</tr>
</table>

### Open source

一些已经合并的小修复，让工具在真实使用中更可靠。

| Project | What I fixed | Patch |
| :-- | :-- | :-- |
| **deer-flow** | 补齐隔离测试子进程所需的 Windows 系统环境变量 | [↗ #6439](https://github.com/bytedance/deer-flow/pull/6439) |
| **Octop** | 修复 Ollama 云端服务被误判为本地运行时的问题 | [↗ #824](https://github.com/TencentCloud/Octop/pull/824) |
| **ouroboros** | 让 Execute 阶段的规划角色遵循指定的模型配置 | [↗ #2462](https://github.com/Q00/ouroboros/pull/2462) |

[查看更多已合并的贡献 →](https://github.com/pulls?q=is%3Apr+author%3Alouisss1016+is%3Amerged)

### Debug lab

<details>
<summary><b>支线任务 01：云端服务，怎么成了本地进程？</b> · 点击开始</summary>

<br>

你配置了 `https://ollama.com/v1`，界面却把它当成本地服务，甚至不让删除。

线索只有一行。你会先改哪里？

```python
is_local = "11434" in url or "ollama" in url
```

<details>
<summary>A / 把连接超时时间调大一点</summary>

超时时间解决不了身份误判。网络请求还没开始，程序已经把云端服务分到了本地分支。

**再看一眼：判断依据是地址，还是地址里的某个单词？**

</details>

<details>
<summary>B / 检查地址是否真指向本地，而不是只匹配服务名称</summary>

**找到了。** `ollama.com` 也包含 `ollama`，所以这个条件会把官方云端地址判成本地服务。

这次修复把判断细化到本地地址、已知本地主机名和默认端口，并添加本地与云端 URL 用例。

这是我在 Octop 修过的真实问题：[查看已合并的补丁 #824 →](https://github.com/TencentCloud/Octop/pull/824)

**通关心得：名称相同，不代表部署位置相同。**

</details>

<details>
<summary>C / 先把删除按钮解锁</summary>

这能绕过一个表象，但服务分类仍然错误，其他依赖分类的行为还会出问题。

**试试沿着错误结果，往上找最早做出判断的地方。**

</details>

</details>

<details>
<summary><b>隐藏抽屉：用字符看看我的贡献记录</b></summary>

<br>

保留一点终端情结。下面是 GitHub 贡献日历的字符版本，由仓库工作流每日生成。

<img src="dist/ascii-contrib.svg" alt="Louisss 的 GitHub 贡献日历，以 ASCII 字符表示每日活跃程度" width="100%">

[查看生成记录 →](https://github.com/louisss1016/louisss1016/actions/workflows/contrib-ascii.yml)

</details>

<br>

---

<sub>Small tools. Real fixes. &nbsp; · &nbsp; build quietly, ship often.</sub>
