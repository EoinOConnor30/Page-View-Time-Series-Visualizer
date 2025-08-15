import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df = df.set_index('date')
df.index = pd.to_datetime(df.index)

# Clean data
df = df[~((df.value < df.value.quantile(.025)) | (df.value > df.value.quantile(.975)))]


def draw_line_plot():
    # Draw line plot
    ax = df.plot(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    fig = ax.get_figure()
    fig.set_size_inches(10,4)




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('ME').mean()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
              'December']
    df_bar['year'] = df_bar.index.year
    df_bar['month']= df_bar.index.month
    df_bar['month'] = df_bar['month'].apply(lambda data: months[data-1])
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months)
    df_pivot = pd.pivot_table(df_bar, values='value', index='year', columns='month', observed=False)

    # Draw bar plot
    ax = df_pivot.plot(kind='bar')
    fig = ax.get_figure()
    fig.set_size_inches(8,6)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15,5))
    sns.boxplot(ax=axes[0], data=df_box, x='year', y='value')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(ax=axes[1], data=df_box, x='month', y='value', order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                                                      'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
