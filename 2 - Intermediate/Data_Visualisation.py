import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def data_visualisation(csv_path, plot_type='pairplot', save_plot=False, filename='plot.png'):
    try:
        data = pd.read_csv(csv_path)
        if plot_type == 'pairplot':
            sns.pairplot(data)
        elif plot_type == 'heatmap':
            sns.heatmap(data.corr(), annot=True)
        elif plot_type == 'histogram':
            data.hist(figsize=(10, 10))

        if save_plot:
            plt.savefig(filename)
        else:
            plt.show()
    except Exception as e:
        print(f'Error: {e}')

# Example usage
# data_visualisation('sample_data.csv', plot_type='heatmap', save_plot=True, filename='heatmap.png')
