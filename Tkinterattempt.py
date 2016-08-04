import pygame, numpy, math, subprocess, os, signal, __future__, thread, time
from Tkinter import *
from pyo import *
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

XWINDOW = 640
YWINDOW = 480
XMENUHEIGHT = 30
YMENUHEIGHT = 30
XEFFECT = "x"
YEFFECT = "y"
PAGE = "pad"

class Display:
        def __init__(self, surface):
                
                self.effect = Effect()
                
                self.surface = surface
                self.background_image = PhotoImage(file = "texture.gif")
                self.background_label = Label(self.surface, image = self.background_image)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.surface.geometry('{}x{}'.format(XWINDOW, YWINDOW))
                self.surface.bind('<Motion>', self.motion)
                self.topFrame = Frame(self.surface)
                self.sideFrame = Frame(self.surface)
                self.chorusX = PhotoImage(file = "chorusX.gif")
                self.chorusY = PhotoImage(file = "chorusY.gif")
                self.distortionX = PhotoImage(file = "distortionX.gif")
                self.distortionY = PhotoImage(file = "distortionY.gif")
                self.flangeX = PhotoImage(file = "flangeX.gif")
                self.flangeY = PhotoImage(file = "flangeY.gif")
                self.waveguideX = PhotoImage(file = "waveguideX.gif")
                self.waveguideY = PhotoImage(file = "waveguideY.gif")
                self.reverbX = PhotoImage(file = "reverbX.gif")
                self.reverbY = PhotoImage(file = "reverbY.gif")
                self.harmoniserX = PhotoImage(file = "harmX.gif")
                self.harmoniserY = PhotoImage(file = "harmY.gif")
                self.freqshiftX = PhotoImage(file = "FreqShiftX.gif")
                self.freqshiftY = PhotoImage(file = "FreqShiftY.gif")
                self.effX1 = Button(self.topFrame, image = self.distortionX, text = "Disto", fg = "black", bg = "white", command = lambda: self.effectPress("Disto", self.effX1, "X"))
                self.effX2 = Button(self.topFrame, image = self.flangeX, text = "Flange", fg = "black", bg = "white", command = lambda: self.effectPress("Flange", self.effX2, "X"))
                self.effX3 = Button(self.topFrame, image = self.chorusX, text = "Chorus", fg = "black", bg = "white", command = lambda: self.effectPress("Chorus", self.effX3, "X"))
                self.effX4 = Button(self.topFrame, image = self.waveguideX, text = "WG", fg = "black", bg = "white", command = lambda: self.effectPress("WG", self.effX4, "X"))
                self.effX5 = Button(self.topFrame, image = self.reverbX, text = "Reverb", fg = "black", bg = "white", command = lambda: self.effectPress("Reverb", self.effX5, "X"))
                self.effX6 = Button(self.topFrame, image = self.harmoniserX, text = "Harm", fg = "black", bg = "white", command = lambda: self.effectPress("Harm", self.effX6, "X"))
                self.effX7 = Button(self.topFrame, image = self.freqshiftX, text = "fShift", fg = "black", bg = "white", command = lambda: self.effectPress("fShift", self.effX7, "X"))
                
                self.effY1 = Button(self.sideFrame, image = self.distortionY, text = "Disto", fg = "black", bg = "white", command = lambda: self.effectPress("Disto", self.effY1, "Y"))
                self.effY2 = Button(self.sideFrame, image = self.flangeY, text = "Flange", fg = "black", bg = "white", command = lambda: self.effectPress("Flange", self.effY2, "Y"))
                self.effY3 = Button(self.sideFrame, image = self.chorusY, text = "Chorus", fg = "black", bg = "white", command = lambda: self.effectPress("Chorus", self.effY3, "Y"))
                self.effY4 = Button(self.sideFrame, image = self.waveguideY, text = "WG", fg = "black", bg = "white", command = lambda: self.effectPress("WG", self.effY4, "Y"))
                self.effY5 = Button(self.sideFrame, image = self.reverbY, text = "Reverb", fg = "black", bg = "white", command = lambda: self.effectPress("Reverb", self.effY5, "Y"))
                self.effY6 = Button(self.sideFrame, image = self.harmoniserY, text = "Harm", fg = "black", bg = "white", command = lambda: self.effectPress("Harm", self.effY6, "Y"))
                self.effY7 = Button(self.sideFrame, image = self.freqshiftY, text = "fShift", fg = "black", bg = "white", command = lambda: self.effectPress("fShift", self.effY7, "Y"))
                
                self.menu = Button(self.topFrame, text = "Menu", fg = "red", bg = "green", command = self.displayMenu)
                self.pad = Button(self.topFrame, text = "Back", fg = "red", bg = "green", command = self.displayPad)
                self.displayPad()
                self.surface.resizable(width=False, height = False)

        def effectPress(self, button, obj, axis):
                if(axis == "X"):
                        global XEFFECT
                        XEFFECT = button
                        self.effect.setXEffect(button)
                        for widget in self.topFrame.winfo_children():
                                widget.config(relief = RAISED)
                elif(axis == "Y"):
                        global YEFFECT
                        YEFFECT = button
                        self.effect.setYEffect(button)
                        for widget in self.sideFrame.winfo_children():
                                widget.config(relief = RAISED)
                obj.config(relief = SUNKEN)
                
        def displayPad(self):
                global PAGE
                PAGE = "pad"
                self.pad.pack_forget()
                self.topFrame.pack(side = TOP)
                self.sideFrame.pack(side = LEFT)
                for widget in self.topFrame.winfo_children():
                        widget.pack(side = LEFT)
                        self.pad.pack_forget()
                for widget in self.sideFrame.winfo_children():
                        widget.pack(side = TOP)

        def displayMenu(self):
                global PAGE
                PAGE = "menu"
                self.sideFrame.pack_forget()
                for widget in self.topFrame.winfo_children():
                        widget.pack_forget()
                for widget in self.sideFrame.winfo_children():
                        widget.pack_forget()
                self.pad.pack()

        def motion(self,event):
                global PAGE
                if(PAGE == "pad"):
                        if(event.x >= 26 and event.y >=26):
                                x, y = self.convertXtoPercentage(event.x), self.convertYtoPercentage(event.y)
                                #print('{}, {}'.format(x,y))

        def convertYtoPercentage(self,y_coordinate):
                if(y_coordinate >= 26):
                        y_coordinate -= 26
                        var1 = int(float(format(float(y_coordinate)/(YWINDOW - 26), '.2f')) * 100)
                        self.effect.modYEffect(var1, YEFFECT, "Y")
                        return var1
                else:
                        return ''

        def convertXtoPercentage(self,x_coordinate):
                if(x_coordinate >= 26):
                        x_coordinate -= 26
                        var1 = int(float(format(float(x_coordinate)/(XWINDOW - 26), '.2f')) * 100)
                        self.effect.modXEffect(var1, XEFFECT, "X")
                        return var1
                else:
                        return ''

class Effect:
        def __init__(self):

                self.s = Server(nchnls = 1).boot()
                self.s.start()
                #a = Input(chnl=0)
                self.s.amp = 0.1
                self.a = Sine()

        def setXEffect(self, effect):
                if(effect == "Disto"):
                        self.lfo = Sine(freq = [.2, .25], mul = .2, add = .2)
                        self.XEffect = Disto(self.a, drive = self.lfo, slope = .3, mul = 0.5).out()
                elif(effect == "Chorus"):
                        self.XEffect = Chorus(self.a, depth = .5, feedback = 0.5, bal= 0.5).out()
                elif(effect == "WG"):
                        self.rnd = Randi(min=.5, max=1.0, freq=[.13,.22,.155,.171])
                        self.rnd2 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])
                        self.XEffect = AllpassWG(self.a, freq=self.rnd2*[74.87,75,75.07,75.21], feed=1, detune=self.rnd, mul=.15).out()
                elif(effect == "Reverb"):
                        self.XEffect = Freeverb(self.a, size=[.79,.8], damp=.9, bal=.3).out()
                elif(effect == "Harm"):
                        self.XEffect = Harmonizer(self.a, transpo = -5, winsize = 0.05).out()
                elif(effect == "fShift"):
                        self.lf1 = Sine(freq=.04, mul=10)
                        self.lf2 = Sine(freq=.05, mul=10)
                        self.XEffect = FreqShift(self.a, shift=self.lf1, mul=.5).out()
                        self.XEffect2 = FreqShift(self.a, shift=self.lf2, mul=.5).out()
                elif(effect == "flange"):
                        self.srPeriod = 1. / self.s.getSamplingRate()
                        self.dlys = [self.srPeriod * i * 5 for i in range(1, 7)]
                        self.XEffect = SDelay(self.a, delay = self.dlys, mul = .1).out()

        def setYEffect(self, effect):
                if(effect == "Disto"):
                        self.lfo = Sine(freq = [.2, .25], mul = .2, add = .2)
                        self.XEffect = Disto(self.a, drive = self.lfo, slope = .3, mul = 0.5).out()
                elif(effect == "Chorus"):
                        self.XEffect = Chorus(self.a, depth = .5, feedback = 0.5, bal= 0.5).out()
                elif(effect == "WG"):
                        self.rnd = Randi(min=.5, max=1.0, freq=[.13,.22,.155,.171])
                        self.rnd2 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])
                        self.XEffect = AllpassWG(self.a, freq=self.rnd2*[74.87,75,75.07,75.21], feed=1, detune=self.rnd, mul=.15).out()
                elif(effect == "Reverb"):
                        self.XEffect = Freeverb(self.a, size=[.79,.8], damp=.9, bal=.3).out()
                elif(effect == "Harm"):
                        self.XEffect = Harmonizer(self.a, transpo = -5, winsize = 0.05).out()
                elif(effect == "fShift"):
                        self.lf1 = Sine(freq=.04, mul=10)
                        self.lf2 = Sine(freq=.05, mul=10)
                        self.XEffect = FreqShift(self.a, shift=self.lf1, mul=.5).out()
                        self.XEffect2 = FreqShift(self.a, shift=self.lf2, mul=.5).out()
                elif(effect == "flange"):
                        self.srPeriod = 1. / self.s.getSamplingRate()
                        self.dlys = [self.srPeriod * i * 5 for i in range(1, 7)]
                        self.XEffect = SDelay(self.a, delay = self.dlys, mul = .1).out()

        def modXEffect(self, value, effect, axis):
                global XEFFECT
                
                if(effect == "Disto"):
                        value = float(value)/100
                        self.XEffect.set("mul", value)
                        print "distortion change"
                elif(effect == "Chorus"):
                        value = float(value)/100
                        self.XEffect.set("feedback", value)
                elif(effect == "WG"):
                        value = float(value)/100
                        self.XEffect.set("mul", value)
                elif(effect == "Reverb"):
                        value = float(value)/100
                        self.XEffect.set("damp", value)
                elif(effect == "Harm"):
                        value = float(value)/100
                        self.XEffect.set("winsize", value)
                elif(effect == "fShift"):
                        value = float(value)/100
                        self.XEffect.set("freq", value)
                elif(effect == "flange"):
                        value = float(value)/100
                        self.XEffect.set("mul", value)

        def modYEffect(self, value, effect, axis):
                global XEFFECT
                
                if(effect == "Disto"):
                        value = float(value)/100
                        self.XEffect.set("mul", value)
                        print "distortion change"
                elif(effect == "Chorus"):
                        value = float(value)/100
                        self.XEffect.set("feedback", value)
                elif(effect == "WG"):
                        value = float(value)/100
                        self.XEffect.set("mul", value)
                elif(effect == "Reverb"):
                        value = float(value)/100
                        self.XEffect.set("damp", value)
                elif(effect == "Harm"):
                        value = float(value)/100
                        self.XEffect.set("winsize", value)
                elif(effect == "fShift"):
                        value = float(value)/100
                        self.XEffect.set("freq", value)
                elif(effect == "flange"):
                        value = float(value)/100
                        self.XEffect.set("mul", value)
                        
#initialise TKinter window
surface = Tk()
app = Display(surface)
surface.mainloop()

#Disto pic                      1-
#Delay pic                      2-
#        Smoothdelay
#Waveguide pic                  3-
#AllPassWG 
#Freeverb pic                   4
#       Convolve 
#WGVerb
#Harmoniser pic                 5-
#FreqShift pic                  6
#Chorus                         7-
