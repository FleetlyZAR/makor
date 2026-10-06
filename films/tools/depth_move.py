#!/usr/bin/env python3
"""Free 2.5D motion for still keyframes: a slow push in where near things move a
little more than far things, from a depth map (Depth Anything V2 Small, Apache 2.0,
runs locally). Run with the makor-audio venv (torch, transformers, Pillow).

    makor-audio/.venv/bin/python films/tools/depth_move.py IN.jpg OUT.mp4 SECONDS [push|pull|drift]
"""
import subprocess, sys

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image, ImageFilter
from transformers import pipeline

W, H, FPS = 1920, 1080, 30
DEV = "mps" if torch.backends.mps.is_available() else "cpu"


def depth_map(img):
    p = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=DEV)
    d = p(img)["predicted_depth"].float().cpu().numpy()
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)          # 1 = near, 0 = far
    dimg = Image.fromarray((d * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(dimg.resize((W, H), Image.BILINEAR), dtype=np.float32) / 255.0


def render(src, out, seconds, mode="push"):
    img = Image.open(src).convert("RGB")
    d = torch.from_numpy(depth_map(img)).to(DEV)
    t_img = torch.from_numpy(np.asarray(img, dtype=np.float32) / 255.0).permute(2, 0, 1)[None].to(DEV)
    ys, xs = torch.meshgrid(torch.linspace(-1, 1, H, device=DEV), torch.linspace(-1, 1, W, device=DEV), indexing="ij")
    n = round(seconds * FPS)
    enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / max(1, n - 1)
        e = t * t * (3 - 2 * t)                                # ease in and out
        if mode == "drift":
            zoom = 1.06 + 0.0 * e
            gx = xs / zoom + 0.05 * e * (d - 0.35)             # near layers slide further sideways
            gy = ys / zoom
        elif mode == "pull":
            zoom = 1.02 + (1 - e) * (0.05 + 0.07 * d)          # the push played backwards
            gx, gy = xs / zoom, ys / zoom
        else:
            zoom = 1.02 + e * (0.05 + 0.07 * d)                # near layers grow faster than far ones
            gx, gy = xs / zoom, ys / zoom
        grid = torch.stack([gx, gy], dim=-1)[None]
        f = F.grid_sample(t_img, grid, mode="bilinear", padding_mode="border", align_corners=True)
        enc.stdin.write((f[0].permute(1, 2, 0).clamp(0, 1) * 255).byte().cpu().numpy().tobytes())
    enc.stdin.close()
    enc.wait()


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "push")
