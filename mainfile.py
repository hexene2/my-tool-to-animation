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

    def convertToCoordinate(self,x,y):return [self.width+x,self.height-y]

    def makeCoordinatePlaneAtSingleFrame(self, scale=100,draw=0, start=0,frame=0,end=15,centerx=0,centery=0):
        if draw == 0:
            print("nahi work kar raha he bhai draw 0 he")
            return "draw is undifind"
        elif frame < start:
            print("nahi work kar raha he bhai probem in if start 0 he")
            return

        progress = (frame-start)/(end-start)
        

        print(frame,progress,end)
        draw.line([(centerx+self.width/2, 0), (centerx+(self.width/2), progress*self.height)], fill=self.forgraund ,width=5)
        draw.line([(0, (self.height/2)-centery), (progress*self.width, (self.height/2)-centery)], fill=self.forgraund,width=5)
        i =1
        print(scale)
        while ((i*scale) < self.width):
            draw.line([(centerx+self.width/2-i*scale, 0), (centerx+(self.width/2)-i*scale, progress*self.height)], fill=self.forgraund,width=1)
            draw.line([(centerx+self.width/2+i*scale, 0), (centerx+(self.width/2)+i*scale, progress*self.height)], fill=self.forgraund,width=1)
            i=i+1
        i =1
        print(scale)
        while ((i*scale) < self.width):
            draw.line([(0, ((self.height/2)-centery+(i*scale))), (progress*self.width, (self.height/2)-centery+(i*scale))], fill=self.forgraund,width=1)
            draw.line([(0, ((self.height/2)-centery-(i*scale))), (progress*self.width, (self.height/2)-centery-(i*scale))], fill=self.forgraund,width=1)

            i=i+1
            
        
        print("this ran currecly___________________________________________________________________________________________this")

    def makeRectAtSingleFrame(self,draw=0,height=400,width=100, start=0,frame=0,end=15,centerx=0,centery=0,color=0,fillColor=0):
        if color ==0:
            color = self.forgraund
        if frame < start or draw ==0:
            return
        
        progress = (frame-start)/(end-start)
        x1 = ((self.width/2)+centerx-width/2)   
        y1 = ((self.height/2)-centery-height/2)
        print("this is the progress of the rect ",progress)
        if progress > 1:
            if fillColor == 0:
                draw.rectangle((x1,y1,x1+width,y1+height),outline=color)
                return
            draw.rectangle((x1,y1,x1+width,y1+height),outline=color, fill=fillColor )
            return
        elif fillColor == 0:
            draw.rectangle((x1,y1,x1+(width*progress),y1+(height*progress)),outline=color)
            return
        draw.rectangle((x1,y1,x1+(width*progress),y1+(height*progress)),outline=color,fill=fillColor)
         
        
    def makeCoordinatePlane(self, scale=100, start=0,end=15,centerx=0,centery=0):
        self.object.append([Motion.makeCoordinatePlaneAtSingleFrame, {"scale":scale, "start":start,"end":end,"centerx":centerx,"centery":centery}])
        print("this is the main object",self.object)

    def makeRect(self, height=200,width=200, start=0,end=15,centerx=0,centery=0,color=0,fillColor=0):
        self.object.append([Motion.makeRectAtSingleFrame, {"height":height,"width":width, "start":start,"end":end,"centerx":centerx,"centery":centery,"color":color,"fillColor":fillColor}])
        print("this is the main object",self.object)
    
    def render(self):
        print("working on it letter")
        for frame in range(self.frameCount):
            img = Image.new("RGB", (self.width,self.height),self.background)
            draw = ImageDraw.Draw(img)
            # self.makeCoordinatePlaneAtSingleFrame(draw=draw,start=15,frame=frame, end=45)
            for methord in self.object:
                print("this is methord line 56",methord[1])
                methord[0](self,draw=draw,frame=frame,**methord[1])#,*methord[1])#draw=draw)
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