import matplotlib.pyplot as plt


# Simple function to make bar plot from given dataframe
def make_bar(dataframe):
    dataframe.plot(kind='bar', stacked=True, colormap='Paired')
    plt.tick_params(axis='x', labelrotation=0)
    plt.title("Распределение моделей по версиям операционных систем")
    plt.show()
