import pygame
import pygame.camera
from pygame.locals import *
import datetime

DEVICE = '/dev/video0'
sw = 640
sh = 640
cw = 640
ch = 480
scale = 50
buttons = []
textRect = 0
screen = 0

class Button:
    def __init__(self, image, position, callback, num):
        self.image = image
        self.rect = image.get_rect(center=position)
        self.callback = callback
        self.num = num
        self.pos = position
 
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self)
                
def onclick(btn):
    if btn.num==8:
        time = datetime.datetime.now()
        filename = "capture" + time.strftime("%Y_%m_%d_%I_%M_%S") + ".png"
        pygame.image.save(screen, filename)
        

def place_buttons():
    global textRect
    
    buttons[0].pos = (sw/4-scale, ch+(sh-ch)/2)
    buttons[1].pos = (sw/4*3-scale, ch+(sh-ch)/2)
    buttons[2].pos = (sw/4+scale, ch+(sh-ch)/2)
    buttons[3].pos = (sw/4*3+scale, ch+(sh-ch)/2)
    buttons[4].pos = (sw/4, ch+(sh-ch)/2-scale)
    buttons[5].pos = (sw/4*3, ch+(sh-ch)/2-scale)
    buttons[6].pos = (sw/4, ch+(sh-ch)/2+scale)
    buttons[7].pos = (sw/4*3, ch+(sh-ch)/2+scale)
    buttons[8].pos = (sw/2, ch+(sh-ch)/2)
    
    for button in buttons:
        button.rect = button.image.get_rect(center=button.pos)
    
    textRect.center = buttons[8].pos
    
def start():
    global textRect, screen
    pygame.init()
    pygame.camera.init()

    font = pygame.font.Font("arial.ttf", 20)
   
    imgl = pygame.image.load('left.png')
    imgl = pygame.transform.scale(imgl, (scale, scale))
    imgr = pygame.image.load('right.png')
    imgr = pygame.transform.scale(imgr, (scale, scale))
    imgu = pygame.image.load('up.png')
    imgu = pygame.transform.scale(imgu, (scale, scale))
    imgd = pygame.image.load('down.png')
    imgd = pygame.transform.scale(imgd, (scale, scale))
    imgb = pygame.image.load('btn.png')
    imgb = pygame.transform.scale(imgb, (2*scale, scale))
    
    display = pygame.display.set_mode((sw, sh), 0)
    camera = pygame.camera.Camera(DEVICE, (cw, ch))
    camera.start()
    
    screen = pygame.surface.Surface((cw, ch), 0, display)
    run = True
    
    buttons.append(Button(imgl, (0, 0), onclick, 0))
    buttons.append(Button(imgl, (0, 0), onclick, 1))
    buttons.append(Button(imgr, (0, 0), onclick, 2))
    buttons.append(Button(imgr, (0, 0), onclick, 3))
    buttons.append(Button(imgu, (0, 0), onclick, 4))
    buttons.append(Button(imgu, (0, 0), onclick, 5))
    buttons.append(Button(imgd, (0, 0), onclick, 6))
    buttons.append(Button(imgd, (0, 0), onclick, 7))
    buttons.append(Button(imgb, (0, 0), onclick, 8))
    
    text = font.render('Capture', True, (0,0,0))
    textRect = text.get_rect()
    
    place_buttons()
    
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                for button in buttons:
                    button.on_click(event)
        
        display.fill((255,255,255))
        
        screen = camera.get_image(screen)
        display.blit(screen, (0,0))
        
        for button in buttons:
            display.blit(button.image, button.rect)
        
        display.blit(text, textRect)
        pygame.display.flip()
        
    camera.stop()
    pygame.quit()
    return
    
if __name__ == '__main__':
    start()
