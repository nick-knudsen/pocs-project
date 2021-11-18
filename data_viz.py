from data_prep import prep_vermont
import plotly.figure_factory as ff
import plotly.graph_objs as go


colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]

def gen_choropleth(values: list, title: str, legend_title: str, fips: list, colorscale=colorscale):

    fig = ff.create_choropleth(
        fips=fips, values=values, scope=['VT'],
        binning_endpoints=[], colorscale=colorscale,
        county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
        legend_title=legend_title, title=title
    )

    return fig


df, counties, fips = prep_vermont()


condensed_counties = df.groupby('County').mean()


mean_poverty = condensed_counties['PovertyRate']
mean_pop = condensed_counties['Pop2010']

poverty_map = gen_choropleth(mean_poverty, 'Mean Poverty', 'Mean Poverty Levels', fips)
pop_map = gen_choropleth(mean_pop, 'Mean Pop', 'Mean Population Levels', fips)
