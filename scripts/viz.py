import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# Set high resolution for detail
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Color palette from the original image
COLORS = {
    'primary_blue': '#1F77B4',
    'secondary_blue': '#A6C6E9',
    'green': '#2CA02C',
    'orange': '#FF7F0E',
    'grey': '#C0C0C0',
    'light_grey': '#EAEAEA',
    'dark_grey': '#333333',
    'background_light': '#FFFFFF',
    'border_dark': '#000000',
    'decay_decay': '#0000FF', # Adjust to match the decay column
}

def draw_styled_box(ax, xy, width, height, label, color, corner_radius=10, fontsize=12, bold=False, text_color='#FFFFFF'):
    """Draws a rounded, color-bordered text box with a label, optimized for infographic look."""
    # Adjust for clean placement
    corner_radius = height / 5 if corner_radius > height/5 else corner_radius
    x, y = xy
    box = patches.FancyBboxPatch((x, y), width, height, boxstyle=f"round,pad={corner_radius*0.1},rounding_size={corner_radius}",
                                 facecolor=COLORS['background_light'], edgecolor=color, linewidth=2)
    ax.add_patch(box)
    
    label_y = y + height * 0.9 # Adjust label position
    label_bold = 'bold' if bold else 'normal'
    ax.text(x + width/2, label_y, label, horizontalalignment='center', verticalalignment='top', fontsize=fontsize, fontweight=label_bold, color=text_color, transform=ax.transAxes)

def draw_arrow(ax, start_xy, end_xy, color, linewidth=2):
    """Draws a clean flow arrow."""
    x1, y1 = start_xy
    x2, y2 = end_xy
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), xycoords=ax.transAxes, textcoords=ax.transAxes,
                arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle="->", linewidth=linewidth))

def draw_pandas_table(ax, xy, dataframe, fontsize=8, header_color='#EEEEEE', col_widths=None):
    """Draws a table based on a pandas DataFrame."""
    x, y = xy
    table_data = dataframe.values.tolist()
    headers = dataframe.columns.tolist()
    
    # Custom cell drawing for cleaner look
    cell_height = 0.03
    
    if col_widths is None:
        col_widths = [1 / len(headers)] * len(headers)
    
    # Draw headers
    header_y = y + cell_height * (len(table_data) + 1)
    for col_idx, (header, width) in enumerate(zip(headers, col_widths)):
        cell_x = x + sum(col_widths[:col_idx])
        rect = patches.Rectangle((cell_x, header_y), width, cell_height, facecolor=header_color, edgecolor=COLORS['grey'], transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(cell_x + width/2, header_y + cell_height/2, header, horizontalalignment='center', verticalalignment='center', fontsize=fontsize, fontweight='bold', transform=ax.transAxes)
    
    # Draw data cells
    for row_idx, row in enumerate(table_data):
        row_y = y + cell_height * (len(table_data) - row_idx)
        for col_idx, (cell_data, width) in enumerate(zip(row, col_widths)):
            cell_x = x + sum(col_widths[:col_idx])
            rect = patches.Rectangle((cell_x, row_y), width, cell_height, facecolor=COLORS['background_light'], edgecolor=COLORS['grey'], transform=ax.transAxes)
            ax.add_patch(rect)
            ax.text(cell_x + width/2, row_y + cell_height/2, str(cell_data), horizontalalignment='center', verticalalignment='center', fontsize=fontsize, transform=ax.transAxes)

# Main function to create the entire infographic
def create_infographic():
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off') # Hide axes

    # --- Draw Main Title ---
    ax.text(0.5, 0.95, "PL/SQL PROCEDURE 'EXPONENTIAL_SMOOTHING' LOGIC VISUALIZATION", 
            horizontalalignment='center', fontsize=24, fontweight='bold', transform=ax.transAxes, color=COLORS['dark_grey'])

    # --- Draw Parameters ---
    ax.text(0.05, 0.90, "INITIALIZATION (alpha = 0.2)", fontsize=14, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.88, "PARAMETERS caltiable parameters: MAX_K = 30 I = 0", fontsize=12, transform=ax.transAxes)

    # --- 1. Initial Data Lookup & Setup ---
    y1_start = 0.80
    ax.text(0.05, y1_start, "1. INITIAL DATA LOOKUP & SETUP", fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    # Boxes
    draw_styled_box(ax, (0.05, 0.70), 0.2, 0.08, "SOURCE_TABLE", COLORS['dark_grey'])
    draw_styled_box(ax, (0.75, 0.70), 0.2, 0.08, "EXECUTE IMMEDIATE 'truncate table analytics.var_x'", COLORS['dark_grey'], fontsize=10)
    
    # Arrows
    draw_arrow(ax, (0.25, 0.74), (0.35, 0.74), COLORS['secondary_blue'], linewidth=4)
    draw_arrow(ax, (0.70, 0.74), (0.75, 0.74), COLORS['secondary_blue'], linewidth=4)
    
    # Table (simulated)
    data1 = {
        'Date': ['2022-06-11', '2022-06-17', '2022-06-23'],
        'Sum Kuendiger': [30, 34, 45],
        'Row Number Asc': [1, 2, 3]
    }
    df1 = pd.DataFrame(data1)
    draw_pandas_table(ax, (0.35, 0.70), df1, fontsize=9, col_widths=[0.1, 0.1, 0.12])
    
    # Text for MAX_K
    ax.text(0.40, 0.77, "MAX_K = calculates of total data points with non-null 'KUENDIGER'", fontsize=10, transform=ax.transAxes)
    ax.text(0.65, 0.74, "MAX_K = 30 (simulated)", fontsize=14, fontweight='bold', transform=ax.transAxes)

    # --- 2. Iteration Loop (Timeline) ---
    y2_start = 0.60
    ax.text(0.05, y2_start, "2. ITERATION LOOP (FOR I in 0..10)", fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    timeline_y = 0.55
    ax.text(0.05, timeline_y, "TIME", fontsize=12, fontweight='bold', transform=ax.transAxes)
    
    # I=0 and I=1 markers
    timeline_x_base = 0.1
    timeline_width = 0.8
    # Sliding windows
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.1, timeline_y - 0.015), 0.2, 0.03, facecolor=COLORS['secondary_blue'], transform=ax.transAxes)) # Window 1
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.5, timeline_y - 0.015), 0.2, 0.03, facecolor=COLORS['secondary_blue'], transform=ax.transAxes)) # Window 2
    
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.1, timeline_y - 0.005), 0.01, 0.01, facecolor=COLORS['orange'], transform=ax.transAxes)) # I=0 box
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.5, timeline_y - 0.005), 0.01, 0.01, facecolor=COLORS['orange'], transform=ax.transAxes)) # I=1 box
    
    ax.text(timeline_x_base + 0.1, timeline_y + 0.01, "I=0", color=COLORS['orange'], fontweight='bold', fontsize=12, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.5, timeline_y + 0.01, "I=1", color=COLORS['orange'], fontweight='bold', fontsize=12, transform=ax.transAxes)
    
    # Timeline labels and dots
    ax.text(timeline_x_base + 0.2, timeline_y + 0.01, "Window", fontweight='bold', fontsize=10, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.6, timeline_y + 0.01, "WindowA Python script that creates the PL/SQL procedure visualization:

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# Set high resolution for detail
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Color palette from the original image
COLORS = {
    'primary_blue': '#1F77B4',
    'secondary_blue': '#A6C6E9',
    'green': '#2CA02C',
    'orange': '#FF7F0E',
    'grey': '#C0C0C0',
    'light_grey': '#EAEAEA',
    'dark_grey': '#333333',
    'background_light': '#FFFFFF',
    'border_dark': '#000000',
    'decay_decay': '#0000FF', # Adjust to match the decay column
}

def draw_styled_box(ax, xy, width, height, label, color, corner_radius=10, fontsize=12, bold=False, text_color='#FFFFFF'):
    """Draws a rounded, color-bordered text box with a label, optimized for infographic look."""
    # Adjust for clean placement
    corner_radius = height / 5 if corner_radius > height/5 else corner_radius
    x, y = xy
    box = patches.FancyBboxPatch((x, y), width, height, boxstyle=f"round,pad={corner_radius*0.1},rounding_size={corner_radius}",
                                 facecolor=COLORS['background_light'], edgecolor=color, linewidth=2)
    ax.add_patch(box)
    
    label_y = y + height * 0.9 # Adjust label position
    label_bold = 'bold' if bold else 'normal'
    ax.text(x + width/2, label_y, label, horizontalalignment='center', verticalalignment='top', fontsize=fontsize, fontweight=label_bold, color=text_color, transform=ax.transAxes)

def draw_arrow(ax, start_xy, end_xy, color, linewidth=2):
    """Draws a clean flow arrow."""
    x1, y1 = start_xy
    x2, y2 = end_xy
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), xycoords=ax.transAxes, textcoords=ax.transAxes,
                arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle="->", linewidth=linewidth))

def draw_pandas_table(ax, xy, dataframe, fontsize=8, header_color='#EEEEEE', col_widths=None):
    """Draws a table based on a pandas DataFrame."""
    x, y = xy
    table_data = dataframe.values.tolist()
    headers = dataframe.columns.tolist()
    
    # Custom cell drawing for cleaner look
    cell_height = 0.03
    
    if col_widths is None:
        col_widths = [1 / len(headers)] * len(headers)
    
    # Draw headers
    header_y = y + cell_height * (len(table_data) + 1)
    for col_idx, (header, width) in enumerate(zip(headers, col_widths)):
        cell_x = x + sum(col_widths[:col_idx])
        rect = patches.Rectangle((cell_x, header_y), width, cell_height, facecolor=header_color, edgecolor=COLORS['grey'], transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(cell_x + width/2, header_y + cell_height/2, header, horizontalalignment='center', verticalalignment='center', fontsize=fontsize, fontweight='bold', transform=ax.transAxes)
    
    # Draw data cells
    for row_idx, row in enumerate(table_data):
        row_y = y + cell_height * (len(table_data) - row_idx)
        for col_idx, (cell_data, width) in enumerate(zip(row, col_widths)):
            cell_x = x + sum(col_widths[:col_idx])
            rect = patches.Rectangle((cell_x, row_y), width, cell_height, facecolor=COLORS['background_light'], edgecolor=COLORS['grey'], transform=ax.transAxes)
            ax.add_patch(rect)
            ax.text(cell_x + width/2, row_y + cell_height/2, str(cell_data), horizontalalignment='center', verticalalignment='center', fontsize=fontsize, transform=ax.transAxes)

# Main function to create the entire infographic
def create_infographic():
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off') # Hide axes

    # --- Draw Main Title ---
    ax.text(0.5, 0.95, "PL/SQL PROCEDURE 'EXPONENTIAL_SMOOTHING' LOGIC VISUALIZATION", 
            horizontalalignment='center', fontsize=24, fontweight='bold', transform=ax.transAxes, color=COLORS['dark_grey'])

    # --- Draw Parameters ---
    ax.text(0.05, 0.90, "INITIALIZATION (alpha = 0.2)", fontsize=14, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.88, "PARAMETERS caltiable parameters: MAX_K = 30 I = 0", fontsize=12, transform=ax.transAxes)

    # --- 1. Initial Data Lookup & Setup ---
    y1_start = 0.80
    ax.text(0.05, y1_start, "1. INITIAL DATA LOOKUP & SETUP", fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    # Boxes
    draw_styled_box(ax, (0.05, 0.70), 0.2, 0.08, "SOURCE_TABLE", COLORS['dark_grey'])
    draw_styled_box(ax, (0.75, 0.70), 0.2, 0.08, "EXECUTE IMMEDIATE 'truncate table analytics.var_x'", COLORS['dark_grey'], fontsize=10)
    
    # Arrows
    draw_arrow(ax, (0.25, 0.74), (0.35, 0.74), COLORS['secondary_blue'], linewidth=4)
    draw_arrow(ax, (0.70, 0.74), (0.75, 0.74), COLORS['secondary_blue'], linewidth=4)
    
    # Table (simulated)
    data1 = {
        'Date': ['2022-06-11', '2022-06-17', '2022-06-23'],
        'Sum Kuendiger': [30, 34, 45],
        'Row Number Asc': [1, 2, 3]
    }
    df1 = pd.DataFrame(data1)
    draw_pandas_table(ax, (0.35, 0.70), df1, fontsize=9, col_widths=[0.1, 0.1, 0.12])
    
    # Text for MAX_K
    ax.text(0.40, 0.77, "MAX_K = calculates of total data points with non-null 'KUENDIGER'", fontsize=10, transform=ax.transAxes)
    ax.text(0.65, 0.74, "MAX_K = 30 (simulated)", fontsize=14, fontweight='bold', transform=ax.transAxes)

    # --- 2. Iteration Loop (Timeline) ---
    y2_start = 0.60
    ax.text(0.05, y2_start, "2. ITERATION LOOP (FOR I in 0..10)", fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    timeline_y = 0.55
    ax.text(0.05, timeline_y, "TIME", fontsize=12, fontweight='bold', transform=ax.transAxes)
    
    # I=0 and I=1 markers
    timeline_x_base = 0.1
    timeline_width = 0.8
    # Sliding windows
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.1, timeline_y - 0.015), 0.2, 0.03, facecolor=COLORS['secondary_blue'], transform=ax.transAxes)) # Window 1
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.5, timeline_y - 0.015), 0.2, 0.03, facecolor=COLORS['secondary_blue'], transform=ax.transAxes)) # Window 2
    
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.1, timeline_y - 0.005), 0.01, 0.01, facecolor=COLORS['orange'], transform=ax.transAxes)) # I=0 box
    ax.add_patch(patches.Rectangle((timeline_x_base + 0.5, timeline_y - 0.005), 0.01, 0.01, facecolor=COLORS['orange'], transform=ax.transAxes)) # I=1 box
    
    ax.text(timeline_x_base + 0.1, timeline_y + 0.01, "I=0", color=COLORS['orange'], fontweight='bold', fontsize=12, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.5, timeline_y + 0.01, "I=1", color=COLORS['orange'], fontweight='bold', fontsize=12, transform=ax.transAxes)
    
    # Timeline labels and dots
    ax.text(timeline_x_base + 0.2, timeline_y + 0.01, "Window", fontweight='bold', fontsize=10, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.6, timeline_y + 0.01, "Window", fontweight='bold', fontsize=10, transform=ax.transAxes)
    
    # Dynamic values on timeline (1+i, max_k - (10-i))
    ax.text(timeline_x_base + 0.10, timeline_y - 0.02, "1+i", fontsize=10, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.25, timeline_y - 0.02, "max_k - (10-i)", fontsize=10, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.50, timeline_y - 0.02, "1+i", fontsize=10, transform=ax.transAxes)
    ax.text(timeline_x_base + 0.65, timeline_y - 0.02, "max_k - (10-i)", fontsize=10, transform=ax.transAxes)
    
    # ... more timeline details (dots, arrows)... skip for brevity

    # --- Branch A: Calculate Weighted Historical Sum (X) ---
    y3_start = 0.45
    box_a = patches.Rectangle((0.05, 0.15), 0.3, 0.3, facecolor=COLORS['background_light'], edgecolor=COLORS['primary_blue'], linewidth=2, transform=ax.transAxes)
    ax.add_patch(box_a)
    ax.text(0.06, y3_start - 0.01, "A. CALCULATE WEIGHTED HISTORICAL SUM (X)", fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.06, y3_start - 0.03, "X = SUM(alpha * POWER((1-alpha), k) * KUENDIGER)", fontsize=10, transform=ax.transAxes)
    
    # Table (simulated Branch A)
    data_a = {
        'K': [1, 2, '...'],
        'KUENDIGER': [30, 40, 45],
        'DECAY WEIGHT': ['0.00* (alpha)', '0.00* (alpha)', '0.56*'],
        'VALUE': [30.4, 45.7, 45.3]
    }
    df_a = pd.DataFrame(data_a)
    draw_pandas_table(ax, (0.06, 0.20), df_a, fontsize=8, header_color='#EEEEEE', col_widths=[0.05, 0.08, 0.12, 0.08])
    
    # ANZ brace and value
    ax.text(0.35, 0.30, "}", fontsize=30, transform=ax.transAxes)
    ax.text(0.36, 0.30, "ANZ\n3", fontsize=12, fontweight='bold', horizontalalignment='center', transform=ax.transAxes)
    
    # Flow arrow to combined result
    draw_arrow(ax, (0.35, 0.25), (0.45, 0.25), COLORS['primary_blue'], linewidth=4)
    ax.text(0.39, 0.25, "+", fontsize=20, fontweight='bold', transform=ax.transAxes)

    # --- Branch B: Calculate Initial Value Adjustment ---
    y4_start = 0.15
    box_b = patches.Rectangle((0.05, 0.01), 0.3, 0.12, facecolor=COLORS['background_light'], edgecolor=COLORS['green'], linewidth=2, transform=ax.transAxes)
    ax.add_patch(box_b)
    ax.text(0.06, y4_start - 0.01, "B. CALCULATE INITIAL VALUE ADJUSTMENT", fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.06, y4_start - 0.03, "Adjustment = POWER((1-alpha), ANZ+1) * START_VALUE", fontsize=10, transform=ax.transAxes)
    
    # Table (simulated Branch B)
    data_b = {
        'K': [1],
        'KUENDIGER': [45]
    }
    df_b = pd.DataFrame(data_b)
    draw_pandas_table(ax, (0.06, 0.03), df_b, fontsize=8, header_color='#EEEEEE', col_widths=[0.05, 0.08])
    
    # Text for variables
    ax.text(0.06, 0.01, "Row Number Desc = max_k - (10-i)", fontsize=9, transform=ax.transAxes)
    ax.text(0.20, 0.04, "START_VALUE =\nKUENDIGER", fontsize=10, horizontalalignment='center', transform=ax.transAxes)
    draw_arrow(ax, (0.15, 0.04), (0.20, 0.04), COLORS['secondary_blue'], linewidth=2)

    # --- Combined Result Block ---
    draw_styled_box(ax, (0.45, 0.20), 0.15, 0.1, "prog_1 = X + Adjustment\n45.3\n(simulated)", COLORS['dark_grey'], fontsize=11)

    # --- 3. Insert into analytics.var_x ---
    y3_start_section = 0.40
    ax.text(0.65, y3_start_section, "3. INSERT INTO ANALYTICS.VAR_X", fontsize=14, fontweight='bold', transform=ax.transAxes)
    draw_arrow(ax, (0.60, 0.25), (0.65, 0.25), COLORS['primary_blue'], linewidth=4)
    
    # Table (simulated analytics.var_x entry)
    data3 = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'prog_1': ['prog_1'] + [''] * 10
    }
    df3 = pd.DataFrame(data3)
    draw_pandas_table(ax, (0.65, 0.05), df3, fontsize=9, col_widths=[0.05, 0.1])
    
    # Label for ANALYTICS.VAR_X
    ax.text(0.65, 0.35, "ANALYTICS.VAR_X", fontweight='bold', fontsize=12, transform=ax.transAxes)

    # --- 4. Results Summary ---
    y4_start_section = 0.40
    ax.text(0.85, y4_start_section, "4. RESULTS SUMMARY", fontsize=14, fontweight='bold', transform=ax.transAxes)
    draw_arrow(ax, (0.80, 0.25), (0.85, 0.25), COLORS['primary_blue'], linewidth=4)
    
    # Table (simulated final results)
    data4 = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11],
        'prog_1': ['prog_1'] * 12
    }
    df4 = pd.DataFrame(data4)
    draw_pandas_table(ax, (0.85, 0.05), df4, fontsize=9, col_widths=[0.05, 0.1])

    # --- Charts in Results Summary ---
    # Draw smaller axes for the charts within the main axis
    chart_ax1 = fig.add_axes([0.91, 0.30, 0.08, 0.08])
    chart_ax2 = fig.add_axes([0.91, 0.15, 0.08, 0.08])
    
    # Simulated data for charts
    x_chart = np.arange(12)
    y_raw = np.array([30, 34, 45, 38, 41, 35, 48, 52, 49, 55, 60, 58])
    y_smoothed = np.array([30, 31, 34, 35, 36, 36, 38, 40, 42, 44, 47, 49]) # Simple approx

    # Chart 1: Raw Data
    chart_ax1.plot(x_chart, y_raw, color=COLORS['primary_blue'], marker='.', linestyle='-')
    chart_ax1.set_title("prog_1", fontsize=9)
    chart_ax1.set_xticks([])
    chart_ax1.set_yticks([])
    chart_ax1.grid(True, which='both', color=COLORS['light_grey'], linewidth=0.5)

    # Chart 2: Raw vs Smoothed
    chart_ax2.plot(x_chart, y_raw, color=COLORS['primary_blue'], marker='.', linestyle='', label='Raw')
    chart_ax2.plot(x_chart, y_smoothed, color=COLORS['green'], linestyle='-', label='Smoothed')
    # chart_ax2.legend(fontsize=7, loc='upper left') # skip legend to avoid clutter in tiny axes
    chart_ax2.set_xticks([])
    chart_ax2.set_yticks([])
    chart_ax2.grid(True, which='both', color=COLORS['light_grey'], linewidth=0.5)

# ... [previous code for Chart 2 remains exactly the same] ...

    plt.tight_layout()
    
    # --- NEW CODE TO SAVE THE IMAGE ---
    # This saves a high-resolution PNG file in the same directory as the script
    filename = 'plsql_logic_visualization.png'
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Success! The visualization has been saved to your current folder as: {filename}")
    
    # Display the plot in the window
    plt.show()

# Run the function to create, save, and display the infographic
create_infographic()
        
