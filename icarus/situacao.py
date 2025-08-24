import geopandas as gpd

class Situacao:
    def __init__(self, shape_path):
        self.gdf = gpd.read_file(shape_path)
        if self.gdf.crs.to_epsg() != 4326:
            self.gdf = self.gdf.to_crs(epsg=4326)

    def obter_mapa_base(self, px):
        fig = px.choropleth_mapbox(
            geojson={},
            locations=[],
            mapbox_style="carto-positron",
            center={"lat": -25.429, "lon": -49.271},
            zoom=11,
        )
        fig.update_layout(autosize=True, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def obter_regioes_afetadas(self, fig, px):
        fig.add_trace(px.choropleth_mapbox(
            self.gdf,
            geojson=self.gdf.geometry,
            locations=self.gdf.index,
            hover_name="nome_area",
            center={"lat": -25.429, "lon": -49.271},
            zoom=11,
            mapbox_style="carto-positron"
        ).data[0])
        return fig
