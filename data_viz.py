from data_prep import prep_vermont
import plotly.figure_factory as ff
import plotly.graph_objs as go


df, counties, fips = prep_vermont()


colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]


mean_poverty = df.groupby('County').mean()['PovertyRate']


values = mean_poverty.round(3).values

fig = ff.create_choropleth(
    fips=fips, values=values, scope=['VT'],
    binning_endpoints=[], colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
    legend_title='Poverty Rate by County', title='Vermont'
)


fig.add_trace(go.Scattergeo(
            lon = [44.467500],
            lat = [-73.175630],
            text = ['test McDonalds'],
            name = 'fast food',
            mode = 'markers',
            marker = dict(
                size = 20,
                color = '#08306b',
                line_width = 0,
                sizeref = 9,
                sizemode = "area",
                reversescale = True
            )))


fig.update_geos(fitbounds="locations")


fig.show()
