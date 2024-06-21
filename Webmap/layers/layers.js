var wms_layers = [];


        var lyr_GoogleSatellite_0 = new ol.layer.Tile({
            'title': 'Google Satellite',
            //'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' ',
                url: 'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
            })
        });
var format_Subcuencasreas_1 = new ol.format.GeoJSON();
var features_Subcuencasreas_1 = format_Subcuencasreas_1.readFeatures(json_Subcuencasreas_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_Subcuencasreas_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_Subcuencasreas_1.addFeatures(features_Subcuencasreas_1);
var lyr_Subcuencasreas_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_Subcuencasreas_1,
maxResolution:280.0446615226196,
 minResolution:0.00028004466152261963,

                style: style_Subcuencasreas_1,
                popuplayertitle: "Subcuencas áreas",
                interactive: true,
    title: 'Subcuencas áreas<br />\
    <img src="styles/legend/Subcuencasreas_1_0.png" /> 0 - 3,8<br />\
    <img src="styles/legend/Subcuencasreas_1_1.png" /> 3,8 - 7,6<br />\
    <img src="styles/legend/Subcuencasreas_1_2.png" /> 7,6 - 11,4<br />\
    <img src="styles/legend/Subcuencasreas_1_3.png" /> 11,4 - 15,2<br />\
    <img src="styles/legend/Subcuencasreas_1_4.png" /> 15,2 - 19<br />\
    <img src="styles/legend/Subcuencasreas_1_5.png" /> 19 - 22,7<br />\
    <img src="styles/legend/Subcuencasreas_1_6.png" /> 22,7 - 26,5<br />\
    <img src="styles/legend/Subcuencasreas_1_7.png" /> 26,5 - 30,3<br />\
    <img src="styles/legend/Subcuencasreas_1_8.png" /> 30,3 - 34,1<br />\
    <img src="styles/legend/Subcuencasreas_1_9.png" /> 34,1 - 37,9<br />'
        });
var format_RedesdeDrenaje_2 = new ol.format.GeoJSON();
var features_RedesdeDrenaje_2 = format_RedesdeDrenaje_2.readFeatures(json_RedesdeDrenaje_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_RedesdeDrenaje_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_RedesdeDrenaje_2.addFeatures(features_RedesdeDrenaje_2);
var lyr_RedesdeDrenaje_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_RedesdeDrenaje_2, 
                style: style_RedesdeDrenaje_2,
                popuplayertitle: "Redes de Drenaje",
                interactive: false,
                    title: '<img src="styles/legend/RedesdeDrenaje_2.png" /> Redes de Drenaje'
                });

lyr_GoogleSatellite_0.setVisible(true);lyr_Subcuencasreas_1.setVisible(true);lyr_RedesdeDrenaje_2.setVisible(true);
var layersList = [lyr_GoogleSatellite_0,lyr_Subcuencasreas_1,lyr_RedesdeDrenaje_2];
lyr_Subcuencasreas_1.set('fieldAliases', {'fid': 'fid', 'DN': 'DN', 'Altura_mea': 'Altitud promedio (m)', 'Altura_min': 'Altitud mínima (m)', 'Altura_max': 'Altitud máxima (m)', 'Pendiente_': 'Pendiente promedio', 'Area': 'Área (km2)', 'Perimetro': 'Perímetro (km)', 'Relief': 'Relieve (m)', 'Compactnes': 'Factor de Compactación', 'Circularit': 'Circularidad', 'Meltons_ru': 'N° de Melton\'s', 'LENGTH': 'LENGTH', 'COUNT': 'COUNT', 'Total_leng': 'Longitud Total de Canales (km)', 'Drainage_d': 'Densidad de Drenaje', });
lyr_RedesdeDrenaje_2.set('fieldAliases', {'fid': 'fid', 'DN': 'DN', });
lyr_Subcuencasreas_1.set('fieldImages', {'fid': 'Hidden', 'DN': 'Hidden', 'Altura_mea': 'TextEdit', 'Altura_min': 'TextEdit', 'Altura_max': 'TextEdit', 'Pendiente_': 'TextEdit', 'Area': 'TextEdit', 'Perimetro': 'TextEdit', 'Relief': 'TextEdit', 'Compactnes': 'TextEdit', 'Circularit': 'Hidden', 'Meltons_ru': 'TextEdit', 'LENGTH': 'Hidden', 'COUNT': 'Hidden', 'Total_leng': 'TextEdit', 'Drainage_d': 'TextEdit', });
lyr_RedesdeDrenaje_2.set('fieldImages', {'fid': 'TextEdit', 'DN': 'Range', });
lyr_Subcuencasreas_1.set('fieldLabels', {'Altura_mea': 'header label - always visible', 'Altura_min': 'header label - always visible', 'Altura_max': 'header label - always visible', 'Pendiente_': 'header label - always visible', 'Area': 'header label - always visible', 'Perimetro': 'header label - always visible', 'Relief': 'header label - always visible', 'Compactnes': 'header label - always visible', 'Meltons_ru': 'header label - always visible', 'Total_leng': 'header label - always visible', 'Drainage_d': 'header label - always visible', });
lyr_RedesdeDrenaje_2.set('fieldLabels', {'fid': 'no label', 'DN': 'no label', });
lyr_RedesdeDrenaje_2.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});