import matplotlib.pyplot as plt
import seaborn as sns


# Define a function to add n=## to show the number of cells per cluster
def show_size(x, color, label=None):
    ax = plt.gca()
    n = len(x)
    ax.text(1, 0.2, 'n={n}'.format(n=n), color=color, ha='left',
            va='center',
            transform=ax.transAxes)


# Define and use a simple function to label the plot in axes
# coordinates
def label(x, color, label=None):
    if label is None:
        return
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="right", va="center", transform=ax.transAxes)


def horizonplot(data, x, row, row_order=None, palette=None,
            xlabel_suffix='log2(UMI + 1)', facet_kws=None, kdeplot_kws=None,
                hline_kws=None, hue=None, label_n_per_group=False):
    facet_kws = dict(aspect=8, size=0.5) if facet_kws is None else facet_kws
    kdeplot_kws = {} if kdeplot_kws is None else kdeplot_kws
    hline_kws = {} if hline_kws is None else hline_kws

    # If the row is set, use the row as the hue color
    hue = row if hue is None else hue
    with sns.axes_style("white", rc={"axes.facecolor": (0, 0, 0, 0)}):
        g = sns.FacetGrid(data, row=row, hue=hue,
                          palette=palette,
                          row_order=row_order, **facet_kws)
        # Draw the densities in a few steps
        g.map(sns.kdeplot, x, clip_on=False, shade=True, alpha=1, lw=1.5,
              bw=.2, **kdeplot_kws)
        g.map(sns.kdeplot, x, clip_on=False, color="grey", lw=1, bw=.2,
              **kdeplot_kws)
        g.map(plt.axhline, y=0, lw=1, clip_on=False, **hline_kws)


        if label_n_per_group:
            g.map(show_size, x)



        g.map(label, x)

        g.set_xlabels('{x} {xlabel_suffix}'.format(
            x=x, xlabel_suffix=xlabel_suffix))

        # Set the subplots to overlap
        g.fig.subplots_adjust(hspace=-.25)

        # Remove axes details that don't play will with overlap
        g.set_titles("")
        g.set(yticks=[])
        g.despine(bottom=True, left=True)

        return g