import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# Set high resolution for detail
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Color palette
COLORS = {
    'primary_blue': '#1F77B4',
    'secondary_blue': '#A6C6E9',
    'green': '#2CA02C',
    'orange': '#FF7F0E',
    'grey': '#C0C0C0',
    'light_grey': '#EAEAEA',
    'dark_grey': '#333333',
    'background_light': '#FFFFFF',
    'text_dark': '#111111'
}

def draw_styled_box(ax, xy, width, height, label, color, corner_radius=0.02, fontsize=10, bold=False):
    """Draws a rounded box with perfectly centered text."""
    x, y = xy
    box = patches.FancyBboxPatch((x, y), width, height, boxstyle=f"round,pad={corner_radius},rounding_size={corner_radius}",
                                 facecolor=COLORS['background_light'], edgecolor=color, linewidth=2)
    ax.add_patch(box)
    
    # Perfectly center the text horizontally and vertically
    label_bold = 'bold' if bold else 'normal'
    ax.text(x + width/2, y + height/2, label, ha='center', va='center', 
            fontsize=fontsize, fontweight=label_bold, color=COLORS['text_dark'], transform=ax.transAxes)

def draw_arrow(ax, start_xy, end_xy, color, linewidth=2):
    """Draws a clean flow arrow."""
    x1, y1 = start_xy
    x2, y2 = end_xy
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), xycoords=ax.transAxes, textcoords=ax.transAxes,
                arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle="->", linewidth=linewidth))

def draw_pandas_table_topdown(ax, xy, dataframe, fontsize=8, header_color='#EEEEEE', col_widths=None):
    """Draws a table from top to bottom so it doesn't overlap text above it."""
    x, y = xy
    table_data = dataframe.values.tolist()
    headers = dataframe.columns.tolist()
    cell_height = 0.035
    
    if col_widths is None:
        col_widths = [0.1] * len(headers)
    
    # Draw headers (Top row)
    for col_idx, (header, width) in enumerate(zip(headers, col_widths)):
        cell_x = x + sum(col_widths[:col_idx])
        rect = patches.Rectangle((cell_x, y - cell_height), width, cell_height, facecolor=header_color, edgecolor=COLORS['grey'], transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(cell_x + width/2, y - cell_height/2, header, ha='center', va='center', fontsize=fontsize, fontweight='bold', transform=ax.transAxes)
    
    # Draw data cells (Flowing downwards)
    for row_idx, row in enumerate(table_data):
        row_y = y - cell_height * (row_idx + 2)
        for col_idx, (cell_data, width) in enumerate(zip(row, col_widths)):
            cell_x = x + sum(col_widths[:col_idx])
            rect = patches.Rectangle((cell_x, row_y), width, cell_height, facecolor=COLORS['background_light'], edgecolor=COLORS['grey'], transform=ax.transAxes)
            ax.add_patch(rect)
            ax.text(cell_x + width/2, row_y + cell_height/2, str(cell_data), ha='center', va='center', fontsize=fontsize, transform=ax.transAxes)

def create_infographic():
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('off') 

    # --- Title & Parameters ---
    ax.text(0.5, 0.95, "PL/SQL PROCEDURE 'EXPONENTIAL_SMOOTHING' LOGIC VISUALIZATION", ha='center', fontsize=22, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.90, "INITIALIZATION (alpha = 0.2)", fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.88, "PARAMETERS: MAX_K = 30, I = 0", fontsize=11, transform=ax.transAxes)

    # --- 1. Initial Data Lookup ---
    ax.text(0.05, 0.82, "1. INITIAL DATA LOOKUP & SETUP", fontsize=12, fontweight='bold', transform=ax.transAxes)
    
    # Source Table Box
    draw_styled_box(ax, (0.05, 0.72), 0.15, 0.08, "SOURCE_TABLE", COLORS['dark_grey'], bold=True)
    draw_arrow(ax, (0.20, 0.76), (0.25, 0.76), COLORS['secondary_blue'], linewidth=3)
    
    # Setup Table (Draws downward from y=0.81)
    df1 = pd.DataFrame({'Date': ['2022-06-11', '2022-06-17', '2022-06-23'], 'Sum Kuendiger': [30, 34, 45], 'Row Asc': [1, 2, 3]})
    draw_pandas_table_topdown(ax, (0.25, 0.81), df1, fontsize=9, col_widths=[0.08, 0.1, 0.08])
    
    # Logic Text and Final Box
    ax.text(0.53, 0.79, "MAX_K calculates\ntotal data points", fontsize=10, ha='center', transform=ax.transAxes)
    ax.text(0.53, 0.74, "MAX_K = 30", fontsize=14, fontweight='bold', ha='center', transform=ax.transAxes)
    draw_arrow(ax, (0.60, 0.76), (0.65, 0.76), COLORS['secondary_blue'], linewidth=3)
    draw_styled_box(ax, (0.65, 0.72), 0.25, 0.08, "EXECUTE IMMEDIATE\n'truncate table analytics.var_x'", COLORS['dark_grey'], fontsize=10)

    # --- 2. Iteration Loop (Timeline) ---
    ax.text(0.05, 0.62, "2. ITERATION LOOP (FOR I in 0..10)", fontsize=12, fontweight='bold', transform=ax.transAxes)
    timeline_y = 0.55
    ax.text(0.05, timeline_y, "TIME", fontsize=12, fontweight='bold', transform=ax.transAxes)
    
    timeline_x = 0.15
    # Window 1 (I=0)
    ax.add_patch(patches.Rectangle((timeline_x, timeline_y - 0.015), 0.25, 0.03, facecolor=COLORS['secondary_blue'], transform=ax.transAxes))
    ax.add_patch(patches.Rectangle((timeline_x, timeline_y - 0.005), 0.01, 0.01, facecolor=COLORS['orange'], transform=ax.transAxes)) 
    ax.text(timeline_x, timeline_y + 0.02, "I=0", color=COLORS['orange'], fontweight='bold', transform=ax.transAxes)
    ax.text(timeline_x + 0.12, timeline_y + 0.02, "Window", fontweight='bold', fontsize=10, ha='center', transform=ax.transAxes)
    ax.text(timeline_x, timeline_y - 0.03, "1+i", fontsize=10, transform=ax.transAxes)
    ax.text(timeline_x + 0.25, timeline_y - 0.03, "max_k-(10-i)", fontsize=10, ha='right', transform=ax.transAxes)

    # Window 2 (I=1)
    ax.add_patch(patches.Rectangle((timeline_x + 0.4, timeline_y - 0.015), 0.25, 0.03, facecolor=COLORS['secondary_blue'], transform=ax.transAxes))
    ax.add_patch(patches.Rectangle((timeline_x + 0.4, timeline_y - 0.005), 0.01, 0.01, facecolor=COLORS['orange'], transform=ax.transAxes)) 
    ax.text(timeline_x + 0.4, timeline_y + 0.02, "I=1", color=COLORS['orange'], fontweight='bold', transform=ax.transAxes)
    ax.text(timeline_x + 0.52, timeline_y + 0.02, "Window", fontweight='bold', fontsize=10, ha='center', transform=ax.transAxes)

    # --- Branch A (Historical Sum) ---
    # Container Box for A
    box_a = patches.Rectangle((0.04, 0.22), 0.40, 0.24, facecolor='none', edgecolor=COLORS['primary_blue'], linewidth=2, transform=ax.transAxes)
    ax.add_patch(box_a)
    ax.text(0.05, 0.48, "A. CALCULATE WEIGHTED HISTORICAL SUM (X)", fontsize=11, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.43, "X = SUM(alpha * POWER((1-alpha), k) * KUENDIGER)", fontsize=10, style='italic', transform=ax.transAxes)
    
    # Detailed Table A
    df_a = pd.DataFrame({
        'K': [1, 2, '...'], 
        'KUENDIGER': [30, 40, 45], 
        'DECAY WEIGHT': ['0.20', '0.16', '...'],
        'VALUE': [6.0, 6.4, '...']
    })
    draw_pandas_table_topdown(ax, (0.05, 0.40), df_a, fontsize=9, col_widths=[0.05, 0.08, 0.12, 0.08])
    
    # ANZ indicator
    ax.text(0.39, 0.32, "}", fontsize=45, color=COLORS['dark_grey'], transform=ax.transAxes)
    ax.text(0.42, 0.34, "ANZ\n= 3", fontsize=11, fontweight='bold', transform=ax.transAxes)

    # --- Branch B (Initial Adjustment) ---
    # Container Box for B
    box_b = patches.Rectangle((0.04, 0.02), 0.40, 0.15, facecolor='none', edgecolor=COLORS['green'], linewidth=2, transform=ax.transAxes)
    ax.add_patch(box_b)
    ax.text(0.05, 0.19, "B. CALCULATE INITIAL VALUE ADJUSTMENT", fontsize=11, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.14, "Adj = POWER((1-alpha), ANZ+1) * START_VALUE", fontsize=10, style='italic', transform=ax.transAxes)
    
    # Table B
    df_b = pd.DataFrame({'K': [1], 'KUENDIGER': [45]})
    draw_pandas_table_topdown(ax, (0.05, 0.11), df_b, fontsize=9, col_widths=[0.05, 0.08])
    ax.text(0.20, 0.07, "Row Desc = max_k-(10-i)", fontsize=9, transform=ax.transAxes)

    # --- Combined Result Block ---
    draw_arrow(ax, (0.45, 0.32), (0.50, 0.32), COLORS['primary_blue'], linewidth=3)
    ax.text(0.47, 0.33, "+", fontsize=18, fontweight='bold', transform=ax.transAxes)
    draw_styled_box(ax, (0.50, 0.28), 0.15, 0.08, "prog_1 = X + Adj\n= 45.3", COLORS['dark_grey'], fontsize=11, bold=True)

    # --- 3. Insert into VAR_X ---
    ax.text(0.70, 0.42, "3. INSERT INTO VAR_X", fontsize=12, fontweight='bold', transform=ax.transAxes)
    draw_arrow(ax, (0.65, 0.32), (0.70, 0.32), COLORS['primary_blue'], linewidth=3)
    df3 = pd.DataFrame({'ID': [1, 2, 3], 'prog_1': ['45.3', '...', '...']})
    draw_pandas_table_topdown(ax, (0.70, 0.38), df3, fontsize=9, col_widths=[0.05, 0.08])

    # --- 4. Results ---
    ax.text(0.85, 0.42, "4. RESULTS", fontsize=12, fontweight='bold', transform=ax.transAxes)
    draw_arrow(ax, (0.83, 0.32), (0.85, 0.32), COLORS['primary_blue'], linewidth=3)
    
    # Insert mini chart
    chart_ax = fig.add_axes([0.85, 0.22, 0.10, 0.12]) # [left, bottom, width, height]
    x_val = np.linspace(0, 10, 10)
    y_raw = np.random.normal(50, 5, 10)
    chart_ax.plot(x_val, y_raw, color=COLORS['secondary_blue'], label='Raw')
    chart_ax.plot(x_val, pd.Series(y_raw).ewm(alpha=0.2).mean(), color=COLORS['orange'], linewidth=2)
    chart_ax.set_xticks([])
    chart_ax.set_yticks([])
    chart_ax.set_title("Trend vs Data", fontsize=9)

    # --- Save & Show ---
    filename = 'plsql_logic_visualization_fixed.png'
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Success! The perfectly aligned visualization has been saved as: {filename}")
    
    plt.show()

if __name__ == "__main__":
    create_infographic()