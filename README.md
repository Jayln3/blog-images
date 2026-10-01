# Jayln3 博客图片库

为中文、英文博客统一管理图片、版本和文章对应关系。

- GitHub：<https://github.com/Jayln3/blog-images>
- 本地：`~/blog-images`，与 `~/blog`、`~/blog_en` 同级。
- 本轮新增图片：`covers/2026/`，每篇现有文章对应一张无文字概念插画。
- 图片索引与中英文替代文本：`assets.json`。
- 缩略预览与文章对应表：`ASSET-CATALOG.md`。
- 完整生成提示词：`docs/generation-prompts.json`。

## 放入新图片

1. 把待整理的图片放进 `inbox/`，告诉助手对应哪篇文章、用途是封面还是正文配图。
2. 整理后的封面放在 `covers/<年份>/`；正文图片可放在 `posts/<文章标识>/`。
3. 文件名使用小写英文、数字和连字符，例如 `agent-memory-v2.png`。已发布图片更新时增加版本号，不覆盖旧图。
4. 验证真实图片格式、文件大小和预览，更新 `assets.json` 后再提交、推送到 `master`。
5. 图片推送完成后，更新同级博客仓库 `config/images.json` 的固定 commit、原图 SHA256 与中英文 alt，再在文章中设置对应的 `translation_key` 和 `cover`。2026-09-29 修复已将这 13 张配图接入博客源码；博客构建会生成 WebP 和缩略图，原图不变。

`inbox/` 是本地待整理区，文件默认不进入 Git；整理到正式目录后再发布。

生成清单时先在 `docs/generation-prompts.json` 与 `docs/asset-briefs.json` 中登记图片，再运行 `python3 scripts/build_catalog.py`。脚本使用 Python 标准库检查 PNG 文件签名、数据块校验、尺寸与单图体积，并重建索引和预览文档；不会生成图片、改动博文或自动推送。

## 引用方式

GitHub 原始文件链接示例：

```text
https://raw.githubusercontent.com/Jayln3/blog-images/master/covers/2026/agent-memory-v1.png
```

需要固定版本时，把 `master` 替换为发布提交 SHA。生产构建建议从这个仓库按提交 SHA 取图，复制到博客的 `/assets/images/`，使用同域资源路径。

现有 jsDelivr 风格的地址仍可构造：

```text
https://cdn.jsdelivr.net/gh/Jayln3/blog-images@master/covers/2026/agent-memory-v1.png
```

**这不是国内外速度保证。** 2026-09-29 的本轮请求中，现有图片的 jsDelivr URL 返回 301 并跳到 `raw.githubusercontent.com`；固定提交 SHA 的 URL 也出现同样情况。因此不应将该地址作为唯一图片分发链路。GitHub 原图链接同样只是访问入口，不代表国内可用性或速度承诺。

## 新配图说明

使用内置 `image-gen` 生成。用户已接受该工具当前使用的图片模型；工具未返回可核验的具体模型编号，因此不宣称这些文件由某一固定型号生成。

配图采用象牙白、深蓝、青绿与铜色的统一横版风格，不含标题文字，可由中英文文章共用。这些是概念插画，不是工具真实界面、广告后台截图、网络测速结果或产品照片。

生成原稿保存在 `covers/2026/`。未来接入博客时，建议制作经过预览检查的 WebP/AVIF 展示版本、保留原稿，并设置尺寸和懒加载；本轮保存的是原始 PNG 文件。

## 实操截图

[Dynadot 域名与邮箱文章截图](posts/dynadot-domain-email/README.md)包含三张作者提供的原始截图，独立清单位于该目录的 assets.json。它们不属于上面的 AI 概念插画清单，不通过生成提示词脚本维护。博客使用固定提交和 SHA256 校验，并注明截图时的配置状态。

[LisaHost 使用记录与 VPS 配置截图](posts/lisahost-vps-experience/README.md)包含旧实例、优惠结算及 AKE 测速四张作者原图，分开注明服务器来源与测试条件。

## 历史文件

根目录旧图片保留原样。检查发现 `home-design-2.jpg` 与 `man.jpg` 实际均为 2 字节换行文本，不能作为图片使用。`home-design-5.jpg` 和 `logo_ln3_bull_v8.png` 是有效图片。
