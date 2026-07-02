from mainfile import Motion

m = Motion(duration=2)
Motion.selectColorCode(m)
# Motion.makeCoordinatePlane(m)
Motion.makeCoordinatePlane(m,start=5,end =45,centerx=0,centery=0)
Motion.makeRect(m,color="white",end=15,height=400,width=900)
Motion.render(m)