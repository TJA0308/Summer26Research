import pandas as pd
import matplotlib.pyplot as plt

def plot_files_grid(file_list, rows):
    df_init = pd.read_csv(file_list[0], nrows=1)
    channels = [col for col in df_init.columns if col not in ['X_Value', 'Comment']]
    
    num_channels = len(channels)
    num_files = len(file_list)
    plt.figure(figsize=(6 * num_files, 3 * num_channels))

    for col_idx, file in enumerate(file_list):
        df = pd.read_csv(file, nrows=rows)
        for row_idx, col_name in enumerate(channels):
            plot_index = (row_idx * num_files) + col_idx + 1
            ax = plt.subplot(num_channels, num_files, plot_index)
            ax.plot(df['X_Value'], df[col_name], color=f'C{row_idx}')
            ax.grid(True)
            if row_idx == 0:
                ax.set_title(f'Data: {file}')
            if col_idx == 0:
                ax.set_ylabel(col_name)
            if row_idx == num_channels - 1:
                ax.set_xlabel('Time (s)')
                
    plt.tight_layout()
    plt.show()

files_to_plot = ['run2.csv', 'run3.csv'] 

plot_files_grid(files_to_plot, rows=20000)