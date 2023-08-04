import plotly.graph_objects as go

def plot_hist(dataset, column , nbinx = 10, title= "Example_title", color='steelblue', y_axis_title = "Example", x_axis_title = "Example"):
# Creating the histogram trace
    trace = go.Histogram(
        x=dataset[column],
        nbinsx=nbinx,
        marker=dict(color=color)
    )

    # Creating the layout
    layout = go.Layout(
        title= title,
        xaxis=dict(title=x_axis_title),
        yaxis=dict(title=y_axis_title)
    )

    # Creating the figure
    fig = go.Figure(data=[trace], layout=layout)

    # Displaying the plot
    return fig
