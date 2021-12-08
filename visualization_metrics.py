from data_prep import prep_vermont
import plotly.figure_factory as ff
import plotly.graph_objs as go
import numpy as np
import os
import webbrowser


def gen_choropleth(values: list, title: str, legend_title: str, fips: list):

    colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]
    
    fig = ff.create_choropleth(
        fips=fips, values=values, scope=['VT'],
        binning_endpoints=[], colorscale=colorscale,
        county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
        legend_title=legend_title, title=title
    )

    return fig

def figures_to_html(figs, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")


def prep(columns: list):
    df, counties, fips = prep_vermont()
    df_copy = df.copy(deep=True)
    df_copy = df_copy.reset_index(drop=True)
    df_copy.fillna(0)
    condensed_counties = df_copy.groupby('County').mean()

    column_dict = {}
    for _, word in enumerate(columns):
        if 'share' in str(word):
            column_dict[word] = gen_choropleth(condensed_counties[str(word)].round(3).values, f'{word}', 'Percent', fips)
        else:
            column_dict[word] = gen_choropleth(condensed_counties[str(word)].round(3).values, f'{word}', 'Population', fips)

    return column_dict


def visualize(dict_column: dict):
    path = os.path.join('explorable.html')
    figures_to_html(dict_column.values(), path)
    webbrowser.open_new_tab(f'file://{os.path.join(os.getcwd(), path)}')


def main():
    columns = ['lapophalfshare', 'lapop1share', 'lapop10share']
    column_dict = prep(columns)
    visualize(column_dict)

if __name__ == '__main__':
    main()