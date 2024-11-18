import pygame,random,math,colorsys
pygame.init()

size=500,500
win=pygame.display.set_mode((size))
clock=pygame.time.Clock()
run=True


class partical():
    def __init__(self,x,y,radius,color=((255,255,255))):
        self.x,self.y=x,y
        self.velx=0
        self.vely=0


        F=15
        self.velx=F*math.asin(((y/250)-1))
        self.vely=F*math.asin(1-(x/250))
        
        
        
        self.drag=0.99
        self.speed=0.05*0
        self.radius=radius
        self.color=color

    
    def physics(self):
        #move to cursor
        mp=pygame.mouse.get_pos()
        mp=[250,250]
        dx=mp[0]-self.x
        dy=mp[1]-self.y
        dist=((dx**2)+(dy**2))**0.5

        self.velx+=dx*self.speed/dist
        self.vely+=dy*self.speed/dist

        #drag
        self.velx*=self.drag
        self.vely*=self.drag

    def collision(self,i,particals):
        self.color=(255,255,255)
        for op in particals:
            i-=1
            if not(i==0):
                dx=op.x-(self.x+self.velx)
                dy=op.y-(self.y+self.vely)
                
                dist=((dx**2)+(dy**2))**0.5
                r=(self.radius+op.radius)
                padding=r*3
                
                if dist <= r:
                    
                    #op.velx,self.velx=self.velx*self.drag,op.velx*self.drag
                    #op.vely,self.vely=self.vely*self.drag,op.vely*self.drag
                    #print("Impact at ",dist)
                    
                    Fmax=r/2
                    rep=Fmax/(dist+1)

                    if dx>0:
                        self.velx-=rep
                        op.velx+=rep
                    elif dx<0:
                        self.velx+=rep
                        op.velx-=rep
                        
                    if dy>0:
                        self.vely-=rep
                        op.vely+=rep
                    elif dy<0:
                        self.vely+=rep
                        op.vely-=rep

                    c=((dist/r)*255)
                    self.color=(int(c),255-int(c),255-int(c))
                    #self.color=colorsys.hsv_to_rgb(0,1,1)
                    #print(self.color)
                    
                else:
                    
                    if (dist-r)>0 and (dist-r)<padding/2:
                        Fmax=-r/10
                        
                        rep=Fmax/(2*abs(dist-r+(padding/2))+1)

                        
                        if dx<0:
                            self.velx-=rep
                            op.velx+=rep
                        elif dx>0:
                            self.velx+=rep
                            op.velx-=rep
                            
                        if dy<0:
                            self.vely-=rep
                            op.vely+=rep
                        elif dy>0:
                            self.vely+=rep
                            op.vely-=rep
                            
                            
                    elif (dist-r)>padding/2 and (dist-r)<padding:
                        Fmax=r/10
                        
                        grav=Fmax/(2*abs(dist-r+(padding/2))+1)

                            
                        if dx>0:
                            self.velx-=grav
                            op.velx+=grav
                        elif dx<0:
                            self.velx+=grav
                            op.velx-=grav
                            
                        if dy>0:
                            self.vely-=grav
                            op.vely+=grav
                        elif dy<0:
                            self.vely+=grav
                            op.vely-=grav
                            
                            
                    elif (dist-r)==(padding/2):
                        self.velx*=self.drag/4
                        self.vely*=self.drag/4
                        
                    else:
                        Fmax=r/40
                        
                        
                        grav=Fmax/(2*(dist-r)+1)

                        
                        if dx<0:
                            self.velx-=grav
                            op.velx+=grav
                        elif dx>0:
                            self.velx+=grav
                            op.velx-=grav
                            
                        if dy<0:
                            self.vely-=grav
                            op.vely+=grav
                        elif dy>0:
                            self.vely+=grav
                            op.vely-=grav
                            

    def move(self,subs):
        self.x+=self.velx/subs
        self.y+=self.vely/subs


    def draw(self,win):
        if self.radius==1:
            pygame.draw.rect(win,self.color,((self.x,self.y),(1,1)))
        else:
            pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
            #pygame.draw.circle(win,self.color,(self.x,self.y),self.radius*4,2)
            #pygame.draw.circle(win,self.color,(self.x,self.y),self.radius*8,1)
            


def Update_particals(particals,window):
    i=0
    substeps=10
    for partical in particals:
        i+=1
        partical.physics()
        partical.collision(i,particals)
        partical.move(1)
        partical.draw(window)




particals=[]
for i in range(300):
    particals.append(partical(random.randrange(int(size[0]/4),int(size[0]*3/4)),random.randrange(int(size[1]/4),int(size[1]*3/4)),5))

while run:
    win.fill((50,50,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    Update_particals(particals,win)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
