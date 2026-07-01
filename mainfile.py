from PIL import Image , ImageDraw
import os, subprocess

OUTPUT_DIR="frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class Motion:
    def __init__(self, height=720, width=1280, fps=30, duration=2):
        self.height = height
        self.width = width
        self.fps = fps
        self.duration=duration
        self.frameCount = self.fps*self.duration
    def selectColorCode(self,forgraund="#dd17dc",background="black",forgraund2="white"):
        self.forgraund = forgraund
        self.background = background
        self.forgraund2 = forgraund2
        self.object=[]

    def makeCoordinatePlane(self, scale=1,draw=0, start=0,frame=0,end=15):
        if draw == 0:
            return "draw is undifind"
        elif frame < start:
            return
        progress = (frame-start)/(end-start)
        print(frame,progress,end)
        draw.line([(self.width/2, 0), (self.width/2, progress*self.height)], fill=self.forgraund)
        draw.line([(0, self.height/2), (progress*self.width, self.height/2)], fill=self.forgraund)


    def render(self):
        print("working on it letter")
        for frame in range(self.frameCount):
            img = Image.new("RGB", (self.width,self.height),self.background)
            draw = ImageDraw.Draw(img)
            self.makeCoordinatePlane(draw=draw,start=15,frame=frame, end=45)
            img.save(f"{OUTPUT_DIR}/{frame:05d}.png")

        subprocess.run([
        "ffmpeg",
        "-y",
        "-framerate", str(self.fps),
        "-i", f"{OUTPUT_DIR}/%05d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "output.mp4"
    ])
        subprocess.run([
            "rm",
            "-rf",
            f"{OUTPUT_DIR}"
        ])

    def rect(self,x,y,w,h,color="white"):
        pass