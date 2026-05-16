# AGENTS.md

## Project shape
- Python proxy/subscription aggregator; there is no package manifest beyond `requirements.txt` (`PyYAML`, `tqdm`, `customtkinter`). Install with `pip3 install -r requirements.txt`.
- Main entrypoints: `subscribe/collect.py` (收集), `subscribe/process.py` (处理), `main.py` (Windows GUI / CLI).
- `subscribe/__init__.py` mutates `sys.path`, so modules inside `subscribe/` use bare imports (`import crawl`, `import utils`); keep that style unless doing a larger import cleanup.
- Vendored native binaries are part of the runtime: `clash/` and `subconverter/`; `subscribe/executable.py` selects the OS-specific names.

## Commands that matter
- 主收集路径（Docker/CI）：`python -u subscribe/collect.py --all --overwrite --skip`.
  - 旧版 `--all --both` 已由 `-t/--targets` 替代，默认输出 clash/v2ray/singbox.
- 仅刷新已有订阅：`python -u subscribe/collect.py --refresh --overwrite --skip`.
- 重新处理配置：`python -u subscribe/process.py --overwrite`.
- 启动 GUI：`python main.py`（需 `pip install -r requirements.txt`）.
- 本地构建 Windows exe：`build_exe.bat`（需 `pip install pyinstaller customtkinter`）.
- CI 构建 exe：推送 `v*` tag 或手动触发 `Build Windows exe` 工作流.
- Docker 构建（amd64）：`docker buildx build --platform linux/amd64 -f Dockerfile -t wzdnzd/aggregator:tag .`.
- 无测试/lint/typecheck 配置；修改 Python 文件后使用 `python -m py_compile` 做基本语法检查.

## Config and environment gotchas
- `subscribe/config/config.default.json` 是 domains / crawl / scripts / push 的可执行配置模式；`subscribe/config/config.json` 被 gitignore，用于本地/私密配置.
- `process.py` 默认通过 `utils.load_dotenv` 加载 `.env`；`--environment` 参数指定环境文件路径，`-s/--server` 覆盖 `SUBSCRIBE_CONF` 环境变量.
- CI/process 环境变量说明见中文 README_CN.md；关键变量：`GIST_PAT`、`GIST_LINK`、`CUSTOMIZE_LINK`、`SUBSCRIBE_CONF`、`PUSH_TOKEN`、`ENABLE_SPECIAL_PROTOCOLS`、`REACHABLE`、`SKIP_ALIVE_CHECK`、`SKIP_REMARK`、`WORKFLOW_MODE`、`LOCAL_BASEDIR`.
- `collect.py` 新增对 `LOCAL_BASEDIR` 的支持，用于输出到本地目录（覆盖默认 `data/`）.
- `ENABLE_SPECIAL_PROTOCOLS` 代码中默认 true，但仅在 clash 运行时为 meta 兼容版本时生效.
- `subconverter/pref.toml`、`subconverter/snippets/`、`subconverter/config/*.ini` 是运行时转换输入，不要删除.
- 日志输出到 stdout 和根目录 `workflow.log`；不要提交日志、data 输出、`.env*`、`subscribe/config/config.json`、`config.local.json`.

## Architecture notes
- `workflow.TaskConfig` 是传递给 `workflow.execute()`/multiprocessing 再到 `AirPort` 解析的核心任务载荷.
- `collect.py` 从 `data/subscribes.txt`、爬取/自定义域名列表、以及可选的 Gist 状态构建任务；`--refresh` 在加载已有订阅后提前结束.
- `process.py` 期望 JSON 配置来自 `SUBSCRIBE_CONF`/`--server`，按 `push_to` 分组任务，可选启动 Clash 二进制做活性检查，然后推送转换后的输出.
- `subscribe/scripts/` 是 `crawl.scripts` 引用的插件系统；配置项使用 `"script": "file#function"` 并传入 `params` 字典.
- 推送后端实现在 `subscribe/push.py`（Gist / local / PasteGG / Imperial / Pastefy / QBin）；避免记录未脱敏的订阅 URL 或令牌.

## Windows GUI 与 PyInstaller 打包

### 入口文件 main.py
- 直接运行 `python main.py` 启动 CustomTkinter 图形界面.
- 通过打包后的 exe 使用 `--cli` 参数运行时，将后续参数转发给 `subscribe/collect.py` 或 `subscribe/process.py`，使用 `runpy.run_path` 动态加载.

### 文件结构
- `main.py` — 入口，判断 GUI 模式还是 `--cli` 模式.
- `gui/app.py` — 主窗口：标题栏、配置/日志分区、运行/停止/保存/加载按钮.
- `gui/config_panel.py` — Collect/Process 双模式配置表单.
- `gui/log_panel.py` — 实时子进程日志显示.
- `gui/runner.py` — 子进程管理（启动/停止、stdout 捕获）.
- `gui/pyinstaller_preload.py` — PyInstaller 打包时预加载依赖，使动态加载的脚本所需的标准库/第三方包被正确打入 exe.

### 裸导入注意事项
`subscribe/*.py` 内部使用裸导入（`import crawl`、`import utils`）。从打包 exe 通过 `runpy.run_path` 加载时，`main.py` 会在执行前将目标脚本所在目录注入 `sys.path`。

这些模块**不得**出现在 `aggregator.spec` 的 `hiddenimports` 中。否则 `_pyinstaller_hooks_contrib` 会匹配到与第三方包同名的本地模块（尤其是 `workflow`），触发 `hook-workflow.py` 尝试 `copy_metadata('workflow')` 导致构建失败。

### PyInstaller spec：aggregator.spec
- 使用 `onedir` 模式（非 onefile）—— vendored 二进制文件（clash ~35 MB、subconverter）体积过大，不适合单文件打包.
- `subscribe/*.py`、`clash/*`、`subconverter/*` 作为 `datas` 打包（运行时文件），不参与 import 分析.
- `hiddenimports` 仅列出标准库和第三方依赖（`uuid`、`tqdm`、`yaml`、`geoip2`、`Cryptodome`、`fofa_hack`、`customtkinter` 等）.
- `console=False` 使 exe 为窗口应用；CLI 模式仍通过 `aggregator.exe --cli subscribe/collect.py ...` 正常工作.

### 构建命令
- 本地：`build_exe.bat` 或 `python -m PyInstaller aggregator.spec --clean --noconfirm`.
- GitHub Actions 工作流：`.github/workflows/build-windows-exe.yml`.
  - 触发方式：手动触发或推送 `v*` tag.
  - 产出物：`aggregator-windows.zip`，作为 workflow artifact 和 Release asset.

## CI details worth matching
- 工作流均通过 `pip3 install -r requirements.txt` 安装依赖；`Get Subscription.yml` 额外安装 `pyYAML requests`，并将 `data/*.txt`/`proxies.yaml` 推送到 gist.
- `collect.yaml`/`refresh.yaml` 检出 `main` 分支；`checkin.yml` 检出 `master` 分支并运行 `.github/actions/checkin/universal.py`.
- `collect.yaml` 和 `refresh.yaml` 使用并发组 `${{ github.repository }}` 并设置 `cancel-in-progress: true`.
- `build-windows-exe.yml` 使用 `windows-latest` 环境，构建 `aggregator.exe` 并压缩为 `aggregator-windows.zip`.
