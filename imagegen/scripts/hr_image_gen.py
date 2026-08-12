#!/usr/bin/env python3
"""Generate images through this deployment's model broker.

Added by HarnessRouter; not part of the upstream skill.

Why this exists rather than the upstream CLI: `scripts/image_gen.py` builds the client with
`OpenAI()`, which reads `OPENAI_API_KEY` and `OPENAI_BASE_URL` from the environment. On a Codex
harness those names already carry the CHAT connection, which is usually a different provider — one
env pair cannot hold two credentials. So the broker credential is passed under `HR_IMAGE_*` and
handed to the SDK explicitly here, which also means image generation behaves identically on Claude
Code, Codex and Hermes instead of only where the chat provider happens to be OpenAI.

The value in HR_IMAGE_KEY is a per-turn credential for this deployment, not a provider key. It is
scoped to one session, expires with the turn, and only the paths the broker allows.
"""
import argparse
import base64
import os
import pathlib
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate an image through the model broker.")
    ap.add_argument("prompt", help="what to draw")
    ap.add_argument("-o", "--output", required=True, help="output file (.png)")
    ap.add_argument("--size", default="1024x1024",
                    help="1024x1024 | 1536x1024 (landscape) | 1024x1536 (portrait)")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--background", default=None, choices=["transparent", "opaque"],
                    help="transparent needs a .png output")
    ap.add_argument("--edit", default=None, metavar="IMAGE",
                    help="edit this image instead of generating from scratch")
    a = ap.parse_args()

    base = os.environ.get("HR_IMAGE_BASE_URL")
    key = os.environ.get("HR_IMAGE_KEY")
    model = os.environ.get("HR_IMAGE_MODEL") or "gpt-image-1"
    if not base or not key:
        # Say which side is missing. "401" or "connection refused" would send the agent looking
        # for a bug in its own prompt instead of at a Harness with no image integration.
        print("error: image generation is not configured for this Harness. An operator needs to "
              "add an integration that serves an image model; no API key belongs in the task.",
              file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("error: the openai SDK is not installed in this image.", file=sys.stderr)
        return 2

    client = OpenAI(api_key=key, base_url=base)
    kwargs = {"model": model, "prompt": a.prompt, "size": a.size, "quality": a.quality}
    if a.background:
        kwargs["background"] = a.background

    if a.edit:
        src = pathlib.Path(a.edit)
        if not src.is_file():
            print(f"error: no such image: {src}", file=sys.stderr)
            return 1
        with src.open("rb") as fh:
            res = client.images.edit(image=fh, **kwargs)
    else:
        res = client.images.generate(**kwargs)

    b64 = res.data[0].b64_json
    if not b64:
        print("error: the provider returned no image data", file=sys.stderr)
        return 1
    out = pathlib.Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(b64))
    print(f"wrote {out} — {out.stat().st_size:,} bytes, {a.size}, quality={a.quality}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
