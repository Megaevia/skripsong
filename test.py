import pybase64
from pathlib import Path

video_folder = Path("D:/testing")

video = open (video_folder / "tester.jpg", "rb").read()

video = pybase64.b64encode(video)

out = open(video_folder / "base64.txt", "wb")
out.write(video)
out.close()