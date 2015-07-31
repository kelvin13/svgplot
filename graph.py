import math
import os
import statistics as stat

def line(x1, y1, x2, y2, color = '#444', width = 1):
    if x1 == x2 and width % 2 == 1:
        x_ = round(x1) + 0.5
        x__ = x_
    else:
        x_ = int(round(x1))
        x__ = int(round(x2))
    if y1 == y2 and width % 2 == 1:
        y_ = round(y1) + 0.5
        y__ = y_
    else:
        y_ = int(round(y1))
        y__ = int(round(y2))
    return '\n<line x1="' + str(x_) + '" y1="' + str(y_) + '" x2="' + str(x__) + '" y2="' + str(y__) + '" style="stroke:' + color + ';stroke-width:'+ str(width) + '" />'

def rectangle(x, y, width, height, color = '#ff50a0'):
    return '\n<rect x="' + str(int(round(x))) + '" y="' + str(int(round(y))) + '" width="' + str(int(round(width))) + '" height="' + str(int(round(height))) + '" style="fill: ' + color + ';" />'

def circle(x, y, r, color = '#ff50a0', opacity = 1):
    return '\n<circle cx=\"' + str(x) + '\" cy=\"' + str(y) + '\" r=\"' + str(r) + '\" style=\"fill:' + color + '; opacity:' + str(opacity) + ';\"/>'
    
def text(x, y, text, align = 0, size = 12, color = '#444', font = 'Neue Frutiger 45', letterspacing=0):
    anchor = None
    if align == -1:
        anchor = 'start'
    if align == 0:
        anchor = 'middle'
    if align == 1:
        anchor = 'end'
    return '\n<text text-anchor="' + anchor + '" x="' + str(int(round(x))) + '" y="' + str(int(round(y))) + '" style="font-family: ' + font + '; font-size: ' + str(size) + '; fill: ' + color + '; letter-spacing:' + str(letterspacing) + '; ">' + str(text) + '</text>'
    
    
    
    
class graph(object):
    def __init__():
        pass
    
    def canvas(canvaswidth = 700,
            canvasheight = 700
            ):
        self.canvaswidth = canvaswidth
        self.canvasheight = canvasheight
        
        self.graphheight = self.canvasheight - 250
    
    def _gridlines(self, ceiling, margin, datarange):
        svgdata = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg viewBox="0 0 700 700" version="1.1"\nxmlns="http://www.w3.org/2000/svg" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n'
        
        # calculate a good tic increment
        whale = math.log(ceiling, 10)
        print (whale)
        increment = 10**(int(math.ceil(whale)) - 1)

        if whale - math.floor(whale) < 0.5:
            increment = increment//4
        elif whale - math.floor(whale) < 0.6:
            increment = increment//2
            
        # make sure there is no division by zero
        if increment == 0:
            increment = 1
            
        increments = int(ceiling//increment + 2)
        self.scale = self.graphheight/(increments*increment)
        

        # vertical marks
        for y in range(increments + 1):
            svgdata += line(100, margin - increment*self.scale*y, 80, margin - increment*self.scale*y)
            
            svgdata += text(75, margin - increment*self.scale*y + 3, increment*y, align=1)
            
            if y != range(increments + 1)[-1]:
                svgdata += line(100, margin - increment*self.scale*(y + 0.5), 90, margin - increment*self.scale*(y + 0.5))
            
        for x in range(datarange):
            # horizontal marks
            if x % self.skip == 0:
                svgdata += line(self.width*x + 100, margin, self.width*x + 100, margin + 20)
                svgdata += text(self.width*x + 100, margin + 20 + 15, self.start + self.step*x)
            if self.skip % 2 == 0 and x % int(self.skip/2) == 0 and x % self.skip != 0:
                svgdata += line(self.width*x + 100, margin, self.width*x + 100, margin + 10) 
        
        # print title
        if self.title:
            svgdata += text(700/2, 80, self.title[0], size=self.title[1], font=self.title[2], color=self.title[3], letterspacing=self.title[4])
        if self.subtitle:
            svgdata += text(700/2, 80 + self.title[1], self.subtitle[0], size=self.subtitle[1], font=self.subtitle[2], color=self.subtitle[3], letterspacing=self.subtitle[4])
            
        # print axis labels
        if self.xaxis:
            svgdata += text(700/2, margin + 60, self.xaxis, size=13, font='Neue Frutiger 65', letterspacing=1)
        
        if self.yaxis:
            svgdata += text(100 - 20, margin - self.graphheight - 30, self.yaxis, size=13, font='Neue Frutiger 65', letterspacing=1)
            
        return svgdata
        
    # clips the '</svg>' from the end of the file and appends new data
    def _frostbyte(self, svgdata):
        with open(self.output, 'rb+') as hh:
                hh.seek(-6, os.SEEK_END)
                hh.truncate()
        with open(self.output, 'a+') as h:
                h.write(svgdata + '</svg>')

def meredith(sprinkles, start, step, bins):
    sprinkles[0].sort()
    kookies = [0] * bins
    for p in sprinkles[0]:
        kookie = int((p - start)//step)
        if kookie >= 0 and kookie < bins:
            kookies[kookie] += 1
    return kookies

class histogram(graph):
    
    def __init__(self, points, 
            start = 0, 
            step = 10, 
            bins = 13,
            
            skip = 4,
            
            width = 10,
            
            title = '',
            subtitle = '',
            
            xaxis = '',
            yaxis = '',
            
            output = 'graph.svg'
            ):
        self.points = points
        self.start = start
        self.step = step
        self.bins = bins
        
        self.skip = skip
        
        self.width = width
        
        self.title = title
        self.subtitle = subtitle
        
        self.xaxis = xaxis
        self.yaxis = yaxis
        
        self.output = output
        
        self.canvaswidth = 700
        self.canvasheight = 700
        self.graphheight = self.canvasheight - 250
    
    
    def bake(self):

        margin = (self.graphheight + 700)//2 + 25

        beckys_poptart = meredith(self.points[0], self.start, self.step, self.bins)
        # draw scales
        ceiling = max(beckys_poptart)
        print (ceiling)
        
        svgdata = self._gridlines(ceiling, margin, len(beckys_poptart) + 1)
        
        for i, s in enumerate(self.points):
            if i != 0:
                poptarts = meredith(s, self.start, self.step, self.bins)
            else:
                poptarts = beckys_poptart
            for x, poptart in enumerate(poptarts):
                svgdata += rectangle(self.width*x + 100, margin - self.scale*poptart, self.width, self.scale*poptart, s[1])
                

        svgdata += '</svg>'
        with open(self.output, 'w') as h:
                h.write(svgdata)

    
    def flavors(self):
        self._frostbyte()
        # print keys
        svgdata = ''
        for i, s in enumerate([l for l in self.points if self.points[2]]):
            svgdata += rectangle(self.width*self.bins - 30, 
                                        self.canvasheight - self.graphheight - 20 + i*30, 
                                        30, 
                                        10, 
                                        s[1]
                                        )
            svgdata += text(self.width*self.bins + 10, 
                                        self.canvasheight - self.graphheight - 10 + i*30, 
                                        s[2], 
                                        align = -1,
                                        color = s[1]
                                        )
        self._frostbyte(svgdata)

    def nutritionfacts(self):
                    
        # print keys
        svgdata = ''
        frame_x = self.width*self.bins + 100 - 90
        frame_y = (self.graphheight + 700)//2 + 25 - self.graphheight
        for i, s in enumerate([l for l in self.points if l[2]]):
            mu = 'μ = —'
            sigma = 'σ = —'
            if len(s[0]) != 0:
                mean = stat.mean(s[0])
                mu = 'μ = ' + str(round(mean, 4))
                sigma = 'σ = ' + str(round(stat.pstdev(s[0], mean), 4))
            line_y = frame_y + i*65
            svgdata += rectangle(frame_x, 
                                        line_y, 
                                        5, 
                                        57, 
                                        s[1]
                                        )
            svgdata += text(frame_x + 20, 
                                        line_y + 10, 
                                        s[2], 
                                        align = -1,
                                        color = s[1],
                                        font = 'Neue Frutiger 65'
                                        )
            svgdata += text(frame_x + 28, 
                                        line_y + 25, 
                                        'n = ' + str(len(s[0])),
                                        align = -1,
                                        color = s[1]
                                        )
            svgdata += text(frame_x + 28, 
                                        line_y + 40, 
                                        mu,
                                        align = -1,
                                        color = s[1]
                                        )
                                         
            svgdata += text(frame_x + 28, 
                                        line_y + 55, 
                                        sigma,
                                        align = -1,
                                        color = s[1]
                                        )
        self._frostbyte(svgdata)

class scatterplot(graph):
    
    def __init__(self, points, 
            start = 0, 
            stop = 100,
            skip = 4,
            
            width = 10,
            
            title = '',
            subtitle = '',
            
            xaxis = '',
            yaxis = '',
            
            output = 'graph.svg'
            ):
        self.points = points
        self.start = start
        self.step = 1
        self.bins = stop - start + 1
        
        self.skip = skip
        
        self.width = width
        
        self.title = title
        self.subtitle = subtitle
        
        self.xaxis = xaxis
        self.yaxis = yaxis
        
        self.output = output
        
        self.canvaswidth = 700
        self.canvasheight = 700
        self.graphheight = self.canvasheight - 250

    
    def bake(self):

        margin = (self.graphheight + 700)//2 + 25

        # draw scales
        ceiling = max([p[1] for p in self.points[0][0]])
        print (ceiling)
        
        svgdata = self._gridlines(ceiling, margin, self.bins)
        
        for i, s in enumerate(self.points):
            for x, poptart in enumerate(s[0]):
                svgdata += circle(poptart[0]*self.width + 100, margin - self.scale*poptart[1], 2, s[1])
                

        svgdata += '</svg>'
        with open(self.output, 'w') as h:
                h.write(svgdata)
                
    def nutritionfacts(self):
                    
        # print keys
        svgdata = ''
        frame_x = self.width*self.bins + 100 - 90
        frame_y = (self.graphheight + 700)//2 + 25 - self.graphheight
        for i, s in enumerate([l for l in self.points if l[2]]):
            mu = 'μ = —'
            sigma = 'σ = —'
            if len(s[0]) != 0:
                xmean = stat.mean([t[0] for t in s[0]])
                xsigma = stat.pstdev([t[0] for t in s[0]], xmean)
                
                ymean = stat.mean([t[1] for t in s[0]])
                ysigma = stat.pstdev([t[1] for t in s[0]], ymean)
                
                mu = 'μ = (' + str(round(xmean, 4)) + ', ' + str(round(ymean, 4)) + ')'
                sigma = 'σ = (' + str(round(xsigma, 4)) + ', ' + str(round(ysigma, 4)) + ')'

                
            line_y = frame_y + i*65
            svgdata += circle(frame_x - 4, line_y + 3, 2, s[1])
            svgdata += circle(frame_x + 4, line_y + 4, 2, s[1])
            svgdata += circle(frame_x - 1, line_y + 10, 2, s[1])
            
            svgdata += text(frame_x + 20, 
                                        line_y + 10, 
                                        s[2], 
                                        align = -1,
                                        color = s[1],
                                        font = 'Neue Frutiger 65'
                                        )
            svgdata += text(frame_x + 28, 
                                        line_y + 25, 
                                        'n = ' + str(len(s[0])),
                                        align = -1,
                                        color = s[1]
                                        )
            svgdata += text(frame_x + 28, 
                                        line_y + 40, 
                                        mu,
                                        align = -1,
                                        color = s[1]
                                        )
                                         
            svgdata += text(frame_x + 28, 
                                        line_y + 55, 
                                        sigma,
                                        align = -1,
                                        color = s[1]
                                        )
        self._frostbyte(svgdata)
