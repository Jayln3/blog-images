#!/usr/bin/env python3
"""Validate the curated PNG covers and rebuild the bilingual image catalog."""

import hashlib
import json
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]


def inspect_png(path):
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Not a PNG image: {path}")
    offset, dimensions, ended = 8, None, False
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError(f"Truncated PNG chunk: {path}")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 8 + length
        if end + 4 > len(data):
            raise ValueError(f"Truncated PNG payload: {path}")
        payload = data[offset + 8:end]
        expected = struct.unpack(">I", data[end:end + 4])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != expected:
            raise ValueError(f"PNG CRC mismatch: {path}")
        if kind == b"IHDR":
            dimensions = struct.unpack(">II", payload[:8])
        offset = end + 4
        if kind == b"IEND":
            ended = True
            break
    if not ended or not dimensions or min(dimensions) <= 0:
        raise ValueError(f"Incomplete PNG: {path}")
    return dimensions, len(data), hashlib.sha256(data).hexdigest()


def main():
    prompts = json.loads((ROOT / "docs/generation-prompts.json").read_text())
    briefs = {x["id"]: x for x in json.loads((ROOT / "docs/asset-briefs.json").read_text())}
    assets = []
    for job in prompts["jobs"]:
        brief = briefs[job["slug"]]
        path = ROOT / job["path"]
        dimensions, size, digest = inspect_png(path)
        if size > 10 * 1024 * 1024:
            raise ValueError(f"Cover exceeds the 10 MiB source budget: {path}")
        assets.append({
            "id": job["slug"], "file": job["path"],
            "article": job["article"], "abbrlink": brief["abbrlink"],
            "article_url": "https://jayln3.github.io/posts/" + brief["abbrlink"] + "/",
            "proposed_category": brief["proposed_category"], "alt": brief["alt"],
            "width": dimensions[0], "height": dimensions[1], "bytes": size,
            "sha256": digest, "format": "png", "kind": "conceptual-illustration",
            "raw_url": "https://raw.githubusercontent.com/Jayln3/blog-images/master/" + job["path"],
            "generation_tool": "image-gen", "model_id": None,
            "blog_attachment_status": "applied-in-blog-source",
        })
    manifest = {"schema_version": 1, "repository": "Jayln3/blog-images",
                "created_date": "2026-09-29", "model_note": prompts["model_note"],
                "source_format_note": "Original PNG covers; web-optimized variants are not generated yet.",
                "assets": assets}
    (ROOT / "assets.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    lines = ["# 博客配图预览与对应关系", "",
             f"{len(assets)} 张无文字概念插画，由内置 image-gen 生成，可由中英文文章共用。", "",
             "当前状态：13 张配图已接入博客中英文文章的封面与正文。原始 PNG 保留，博客构建生成 WebP 展示图和缩略图。", "",
             "完整提示词见 [generation-prompts.json](docs/generation-prompts.json)，结构化清单见 [assets.json](assets.json)。", "",
             "| 图片 | 对应文章 | 建议分类 | 尺寸 | 原稿体积 |", "|---|---|---|---|---|"]
    for asset in assets:
        size_mib = asset["bytes"] / 1024 / 1024
        lines.append(f'| [{asset["id"]}]({asset["file"]}) | `{asset["article"]}` | {asset["proposed_category"]} | {asset["width"]} × {asset["height"]} | {size_mib:.2f} MiB |')
    for i, asset in enumerate(assets, 1):
        lines += ["", f'## {i}. {asset["id"]}', "",
                  f'对应文章：[{asset["article"]}]({asset["article_url"]})', "",
                  f'![{asset["alt"]["zh-CN"]}]({asset["file"]})', "",
                  "中文 alt：" + asset["alt"]["zh-CN"], "",
                  "English alt: " + asset["alt"]["en"]]
    (ROOT / "ASSET-CATALOG.md").write_text("\n".join(lines) + "\n")
    print(f"Validated {len(assets)} PNG images; wrote assets.json and ASSET-CATALOG.md.")
    print(f"Total source image bytes: {sum(a['bytes'] for a in assets)}")


if __name__ == "__main__":
    main()
