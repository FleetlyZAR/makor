# Rendering the whole Bible on a rented GPU

The whole Bible, all four voices, full study, is weeks on a laptop CPU but about
a day on one modern GPU. This is a one-time job: rent a GPU box, run one script,
shut it down.

## 1. Rent a GPU box

Any provider works (RunPod, Vast.ai, Lambda, Paperspace). Pick:

- One GPU. An RTX 4090, L4, A10, or A100 are all more than enough.
- An image that already has PyTorch and CUDA (for example RunPod's "PyTorch 2"
  template, or Lambda's PyTorch image), Ubuntu 22.
- Cost is roughly 0.40 to 1.20 US dollars an hour, so the whole run lands well
  under about 30 dollars. You only pay while it is on.

Note the box's SSH connection details.

## 2. Send it what it needs (from your Mac)

The runner needs the scripts, the study JSON, and your R2 keys. Package just
those, preserving the folder layout, and copy them over:

```
cd ~/Documents/Developer/makor
tar czf /tmp/makor-run.tgz \
  makor-audio/generate_audio.py makor-audio/build_and_upload.py \
  makor-audio/gpu_run.py makor-audio/pronounce.json makor-audio/.env \
  src/content/studies
scp /tmp/makor-run.tgz root@YOUR_BOX_IP:~/
```

Replace `root@YOUR_BOX_IP` with the box's SSH target (the provider shows it).

## 3. On the box: set up and run

SSH in, then:

```
tar xzf makor-run.tgz
apt-get update && apt-get install -y espeak-ng ffmpeg
pip install kokoro soundfile boto3

cd makor-audio
tmux new -s makor          # a session that survives disconnects
python3 gpu_run.py --all
```

The first study downloads the Kokoro model once, then it moves fast; each study
prints how many seconds it took. Detach from tmux with Ctrl-b then d, and you can
close your laptop; reattach later with `tmux attach -t makor`.

It is resumable: if it stops, rerun `python3 gpu_run.py --all` and it skips what
is already on R2. It uploads straight to R2, so as books finish, their players
appear on the live site on their own.

If `torch.cuda.is_available()` is false, the script prints a warning and would be
slow: that means the box has no usable GPU, so pick a proper GPU image.

## 4. Verify, then tear down

Open a freshly rendered file in a browser to confirm it plays, for example
`https://audio.makor.co.za/studies/john/the-word-became-flesh/audio/am_michael/full.mp3`.
When the run reports it is finished and a spot check sounds right, terminate the
box in the provider dashboard so billing stops.

## 5. Security: rotate the R2 key afterward

Your `.env` with the R2 secret lived on a rented machine. After you tear the box
down, rotate that key: in Cloudflare R2, delete the `makor-audio-upload` token
and create a fresh one, then update `makor-audio/.env` on your Mac. Cheap
insurance, and good practice.

## Notes

- Same content as the laptop path: this reuses the exact text assembly,
  pronunciation map, and build stamp, so audio is identical and the site reads
  it the same way.
- To render a subset: `python3 gpu_run.py --book genesis` or
  `python3 gpu_run.py --study ../src/content/studies/ruth/01-....json`.
- Default voices are all four; narrow with `--voices am_michael,bf_emma`.
