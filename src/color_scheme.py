
class ColorScheme:
    # call next_color to change color of turtle drawing

    def __init__(self):

        # colors from https://flatuicolors.com/palette/defo
        self.colors = ['#1abc9c', '#3498db', '#9b59b6',
                       '#2980b9', '#8e44ad', '#16a085', '#7f8c8d',
                       '#27ae60', '#e74c3c', '#95a5a6', '#d35400', '#c0392b']

        self.color_idx = 0

        self.bg_color = '#2c3e50'
        self.bg_color2 = '#bdc3c7'
        self.bg_color3 = '#ecf0f1'
        self.drawing_color = '#ecf0f1'

    def next_color(self, turtle_color):
        turtle_color(self.colors[self.color_idx % len(self.colors)])
        self.color_idx += 1
