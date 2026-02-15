import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class RectangleSelector:
    def __init__(self, ax):
        self.ax = ax
        self.start_point = None
        self.rect = None
        self.color_index = 0
        self.colors = [[1, 0, 0, 1],    # Red
                       [0, 1, 0, 1],    # Green
                       [0, 0, 1, 1],    # Blue
                       [1, 1, 0, 1],    # Yellow
                       [1, 0, 1, 1],    # Magenta
                       [0, 1, 1, 1]]    # Cyan
        self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    def on_press(self, event):
        if event.inaxes == self.ax:
            self.start_point = (event.xdata, event.ydata)
            self.rect = Rectangle(self.start_point, 0, 0, edgecolor='red', alpha=0.2)
            self.ax.add_patch(self.rect)
    def on_motion(self, event):
        if self.start_point is not None and event.inaxes == self.ax:
            width = event.xdata - self.start_point[0]
            height = event.ydata - self.start_point[1]
            self.rect.set_width(width)
            self.rect.set_height(height)
            self.ax.figure.canvas.draw()
    def on_release(self, event):
        if self.start_point is not None:
            # Determine the data points within the rectangle and perform actions as needed
            selected_data = self.get_data_within_rectangle()
            print("Selected Data:", selected_data)
            self.change_selected_color(selected_data)
            self.start_point = None
            self.rect.remove()
            self.ax.figure.canvas.draw()
    def get_data_within_rectangle(self):
        # Get rectangle bounds
        x_min = min(self.start_point[0], self.start_point[0] + self.rect.get_width())
        x_max = max(self.start_point[0], self.start_point[0] + self.rect.get_width())
        y_min = min(self.start_point[1], self.start_point[1] + self.rect.get_height())
        y_max = max(self.start_point[1], self.start_point[1] + self.rect.get_height())
        
        # Find indices of points within rectangle
        indices = []
        for collection in self.ax.collections:
            offsets = collection.get_offsets()
            for i, (x, y) in enumerate(offsets):
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    indices.append(i)
        
        return indices
    
    def change_selected_color(self, indices):
        # Change color of selected points to next color in rotation
        if indices and len(self.ax.collections) > 0:
            collection = self.ax.collections[0]
            colors = collection.get_facecolors()
            if len(colors) == 0:
                colors = np.tile([0, 0, 1, 1], (len(collection.get_offsets()), 1))
            elif len(colors) == 1:
                colors = np.tile(colors[0], (len(collection.get_offsets()), 1))
            else:
                colors = colors.copy()
            
            current_color = self.colors[self.color_index]
            for idx in indices:
                colors[idx] = current_color
            
            collection.set_facecolors(colors)
            self.color_index = (self.color_index + 1) % len(self.colors)
      
# Create a scatter plot with random data
import numpy as np
np.random.seed(42)
x_data = np.random.rand(50)
y_data = np.random.rand(50)
fig, ax = plt.subplots()
ax.scatter(x_data, y_data)
# Initialize the RectangleSelector
rect_selector = RectangleSelector(ax)
plt.show()