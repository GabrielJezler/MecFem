import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mc
import numpy as np

plt.rcParams.update({
    "figure.figsize": (10, 8),
    "figure.titlesize": 24,
    "figure.autolayout":True,
    "axes.titlesize": 20,
    "font.family": "Courier New",
    "font.size": 16,
    "savefig.format": "pdf",
})

class RectangleSelector:
    COLORS_ID = 0
    COLORS = [
        "dimgrey",
        "orangered",
        "darkorange",
        "green",
        "dodgerblue",
        "indigo"
    ]
    
    def __init__(self, ax:plt.Axes):
        self.ax = ax

        self.ax_table = None
        self.table = None

        self.start_point = None
        self.rect = None

        self.selections = []  # Store each selection

        self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes == self.ax:
            self.start_point = (event.xdata, event.ydata)
            self.rect = Rectangle(self.start_point, 0, 0, edgecolor='k', facecolor=self.COLORS[self.COLORS_ID], alpha=0.4)
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
            if selected_data:
                color = self.COLORS[self.COLORS_ID]
                self.selections.append({
                    'id': len(self.selections) + 1,
                    'color': color,
                    'count': len(selected_data),
                    'indices': selected_data
                })

                self.change_selected_color(selected_data)
                self.update_table()
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
        
        return np.unique(indices).tolist()
    
    def change_selected_color(self, indices):
        if indices and len(self.ax.collections) > 0:
            collection = self.ax.collections[0]
            colors = collection.get_facecolors()
            if len(colors) == 0:
                colors = np.tile([0, 0, 1, 1], (len(collection.get_offsets()), 1))
            elif len(colors) == 1:
                colors = np.tile(colors[0], (len(collection.get_offsets()), 1))
            else:
                colors = colors.copy()
            
            for idx in indices:
                colors[idx] = mc.to_rgba(self.COLORS[self.COLORS_ID])
            
            collection.set_facecolors(colors)
            self.COLORS_ID = (self.COLORS_ID + 1) % len(self.COLORS)

    @staticmethod
    def format_two_per_line(nums:list[str], n_per_line:int=3):
        lines = [",".join(map(str, nums[i:i+n_per_line])) for i in range(0, len(nums), n_per_line)]
        return "\n".join(lines)
    
    def update_table(self):
        # Remove existing table if present
        if self.table is not None:
            self.table.remove() 
        if self.ax_table is None:
            self.ax.figure.set_constrained_layout(False)
            pos = self.ax.get_position()  # get current position
            self.ax.set_position([pos.x0, pos.y0, pos.width * 0.7, pos.height])

            self.ax_table: plt.Axes = self.ax.figure.add_axes([
                pos.x0 + pos.width * 0.7,  # start where first axis ends
                pos.y0,
                pos.width * 0.3,
                pos.height
            ])
            self.ax_table.axis('off')  # Hide axes for the table
        
        # Prepare table data
        nodes_str = [s['indices'] for s in self.selections]
        nodes_str = [[id_str for id, id_str in enumerate(str(n).removeprefix(r'[').removesuffix(r']').split(','))] for n in nodes_str]
        nodes_str = [self.format_two_per_line(ids) for ids in nodes_str]

        cell_text = [[sel['id'], nodes_str[i]] for i, sel in enumerate(self.selections)]
        cell_colors = [['white', 'white'] for s in self.selections]
        
        # Create table
        self.table = self.ax_table.table(
            cellText=cell_text,
            cellColours=cell_colors,
            colLabels=['Selection', 'Nodes'],
            colWidths=[0.35, 0.6],
            loc='center',
            # bbox=[1.1, 0, 0.3, 1],
            cellLoc='center',
            edges='BRTL'
        )
        self.table.auto_set_font_size(False)
        self.table.set_fontsize(12)
        
        # Style the table
        for (i, _), cell in self.table.get_celld().items():
            if i == 0:  # Header row
                cell.set_facecolor('white')
                cell.set_text_props(weight='bold', color='black')
                cell.set_height(cell.get_height() * 1.2)
            else:
                cell.set_facecolor('white')
                cell.set_text_props(color=self.selections[i-1]['color'])
                cell.set_height(cell.get_height() * 1.2 * np.ceil(self.selections[i-1]['count'] / 3))
            cell.set_edgecolor('black')
            cell.set_linewidth(1)
        
        self.ax_table.figure.canvas.draw()

if __name__ == "__main__":
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