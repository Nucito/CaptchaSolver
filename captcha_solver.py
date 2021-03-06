import torch
import cv2
import numpy as np

class CaptchaSolver:
    def __init__(self) -> None:
        self.boxes = []
        self.js = {}
    
    def toText(self, cords):
        solved = ""
        
        for cord in cords:
            for x in range(0, len(self.boxes)):
                if list(self.boxes[x].values())[0]['y1'] == cord:
                    solved += str(list(self.boxes[x].keys())[0])
        
        self.text = solved
    
    def SolveCaptcha(self, img, best_path, percent_required):
        if type(img) == np.ndarray  and best_path and percent_required:
            model = torch.hub.load('.', 'custom', best_path, source='local')
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            results = model(img, size=416)  
            #results.show()

            if results.xyxy[0].shape[0] >= 1:
                for box in range(0, results.xyxy[0].shape[0]):
                    y1, x1, y2, x2, percent, pred = results.xyxy[0][box]
                    if percent >= percent_required:
                        self.boxes.append({str(int(pred.item())):{"x1":round(x1.item(), 2), "y1":round(y1.item(), 2), "x2":round(x2.item(), 2), "y2":round(y2.item(), 2), "per":round(percent.item(), 2)}})
                
                xCord = sorted([self.boxes[x][list(self.boxes[x].keys())[0]]['y1'] for x in range(0, len(self.boxes))])
                
                self.toText(xCord)
                
                self.js["Captcha"] = str(self.text)
                self.js["Cods"] = self.boxes
                                        
            return self.js

img = cv2.imread("image.jpeg")
cp = CaptchaSolver()

print(cp.SolveCaptcha(img, "bomb_captcha.pt", 0.7))
