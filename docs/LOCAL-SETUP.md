# 本机配置

本 fork 使用上游已经适配的 **剪映专业版 11.5.0**。引擎、原生导出接口、
蓝图和桥接二进制的固定哈希沿用上游配置，未增加对 11.5.3 的支持。

首页登记补充了 macOS 27 的新文件权限元数据处理：源索引没有 `com.apple.macl`
时，保留新文件在复制属性之前已经具有的系统标签，并验证其字节始终不变。
已有源标签被修改或丢失、复制过程中出现新标签，以及其他安全属性变化仍会被拒绝。
相关 Python 源码修改后，重新测试并更新入口的对应源码指纹。

原生导出也使用桥接程序记录的精确工具链，并明确指定 SDK 和最低系统版本。
本机测试发现系统默认工具链生成的导出程序会漏掉画中画；固定到
Apple clang `2100.1.1.101`、SDK 26.5、linker 1267 和部署目标 26.0 后通过画面检查。
导出报告会记录实际工具链；选择不匹配时停止编译。

## 安装位置

- 项目使用的应用：`/Applications/VideoFusion-macOS.app`（11.5.0）。
- 保留的原应用：`/Applications/VideoFusion-11.5.3.app`。
- 独立编译工具：`~/.local/share/jianying-headless/toolchains/26.5/CommandLineTools`。
- FFmpeg / ffprobe：`~/.local/bin/`。
- 安装记录、合成测试素材及验证报告：本项目的 `work/compatible-runtime/` 和 `work/package-smoke-*/`。
- 切换版本前的草稿目录备份：`~/.local/share/jianying-headless/backups/`。

系统的 `xcode-select` 保持原设置；启动器仅为本次命令设置 `DEVELOPER_DIR`。
已显式设置的 `DEVELOPER_DIR` 优先。编译工具或应用升级后，重新执行检查；
版本或哈希不匹配时，原有检查会停止运行。

## 使用

在项目目录运行：

```bash
python3 tools/local.py doctor
python3 tools/local.py build-codec
python3 tools/local.py smoke-test --export
```

本机另有 `jianying-headless` 命令，等同于 `python3 tools/local.py`。
VS Code 的“终端 → 运行任务”提供环境检查、桥接构建和草稿与导出验证。

正常剪辑沿用上游的命令和参数：

```bash
jianying-headless build --plan /absolute/path/to/plan.json --out "$PWD/work/new-build"
jianying-headless verify-build --build "$PWD/work/new-build"
jianying-headless export --build "$PWD/work/new-build" --out "$PWD/work/new-export"
```

首页登记仍要求保存并退出剪映，并先初始化默认草稿目录；详见
[首次草稿教程](GETTING-STARTED.md)。测试草稿使用合成视频和声音。
自动测试不代表所有效果或实际素材都已经通过视听验收。

## 本机验证结果

2026-09-20，在 Apple Silicon、macOS 27.0 上完成：

- 环境检查通过；11.5.0 引擎与重建桥接程序的哈希均匹配上游。
- 52 项项目测试、30 项原生导出防护测试通过。
- 合成草稿在剪映首页登记，播放、保存、完全退出后重新打开成功；
  3 条轨道及视频、画中画、中文字幕保留，4 份草稿镜像一致。
- 修正工具链后的原生导出为 640×360、30 fps、60/60 帧、H.264/AAC MP4；
  时长约 2 秒，完整解码通过，源素材与构建快照未改变。
- 实际查看 0.5 秒与 1.5 秒导出帧，旋转画中画、中文字幕和变速后的主画面可见。
  合成音频检测到非静音信号，峰值 -29.8 dB。

首页保存与重开记录在 `work/package-smoke-q8zdy8io/`；
最终导出和抽帧记录在 `work/package-smoke-rb2iwser/`。

## 来源与校验

11.5.0 安装包来自剪映官方更新接口返回的
[官方下载地址](https://lf3-package.vlabstatic.com/obj/faceu-packages/Jianying_11_5_0_13199_jianyingpro_0_creatortool_nosandbox.dmg)。
安装包 SHA-256 为 `3a90f96e93edef11df58dd8d2c61a584b73b54235cadb328cd71dd039ef1a775`；
安装前核验完整 Apple Developer ID 签名和上游固定的引擎哈希：
`2041482a1aaeffa4d8bd69b836f8cf38807aaad8021bca410d567c59af3bccfa`。

Command Line Tools 26.5 从 Apple Software Update 产品 `047-91568` 提取，
核验 Apple 软件签名、目录指定的 XAR 压缩目录摘要以及各载荷摘要。
SDK 使用本机已安装的 `MacOSX26.5.sdk`。
FFmpeg / ffprobe 来自 [ffmpeg-static 的 b6.1.1 发布](https://github.com/eugeneware/ffmpeg-static/releases/tag/b6.1.1)，
下载后按 GitHub 发布资产的 SHA-256 校验；实际可执行版本为 FFmpeg 6.0。

安装包、官方程序库、编译产物和个人草稿留在本机，不提交到 GitHub。
