# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 11:25:04 2018

@author: XGE-PC
"""

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import pandas as pd
import os
import math
import numpy as np
from scipy.spatial import Delaunay
import scipy as sp
from shapely import wkt, geometry
import shapely
from shapely.ops import cascaded_union

import matplotlib as mpl
import matplotlib.pyplot as plt 
from mpl_toolkits.basemap import Basemap 
from scipy.special import binom
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase


class flow_shape_generator:
    def __init__(self):
        
        self.curve_sampling_length = 10000
        self.self_directed_sampling_size = 100
        self.self_directed_size = 80000
        
        self.flow_volume_minmum = 10
        self.flow_volume_percentage = 0.9
        self.flow_show_max_count = 30
        
    # =============================================================================
    # 
    # =============================================================================
    def set_curve_parameter(self, curve_sampling, self_directed_sampling, self_directed_size):
        self.curve_sampling_length = curve_sampling
        self.self_directed_sampling_size = self_directed_sampling
        self.self_directed_size = self_directed_size
    
    # =============================================================================
    # 
    # =============================================================================
    def set_flow_statistic_parameter(self, flow_volume_min_threshold, flow_volume_percentage_threshold, flow_show_maximum_count_threshold):
        self.flow_volume_minmum = flow_volume_min_threshold
        self.flow_volume_percentage = flow_volume_percentage_threshold
        self.flow_show_max_count = flow_show_maximum_count_threshold
    
    # =============================================================================
    # 
    # =============================================================================
    def mkdir(self, path):
        path=path.strip()
        path=path.rstrip("\\")
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False
    
    # =============================================================================
    # 
    # =============================================================================
    def get_curve(self, x1,y1,x2,y2):
        tempX1 = -(y1 - y2)/3 + (x1+x2)/2
        tempY1 = (x1 - x2)/3 + (y1+y2)/2
        
        line_len = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
        P=(x1,y1),(tempX1,tempY1),(x2,y2)
        n = len(P)-1
        
        Num_t=int(line_len/self.curve_sampling_length)
        px, py = [None]*(Num_t+1),[None]*(Num_t+1)
        
        for j in range(Num_t+1):
            t = j / float(Num_t)
            px[j],py[j]=0.0,0.0
            for i in range(len(P)):
                px[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][0]
                py[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][1]
        
        px1, py1 = [None]*(Num_t-1),[None]*(Num_t-1)
        for j in range(Num_t-1):
            px1[j] = px[j+1]
            py1[j] = py[j+1]
        return px1, py1

    # =============================================================================
    # 
    # =============================================================================
    def get_curve_close(self, x1,y1,x2,y2):
        size = self.self_directed_size
        tempX1 = size/1.2 + (x1+x2)/2
        tempY1 = size + (y1+y2)/2
        
        tempX2 = (x1+x2)/2
        tempY2 = size + (y1+y2)/2
        
        tempX3 = -size/1.2 + (x1+x2)/2
        tempY3 = size + (y1+y2)/2
        
        P=(x1,y1),(tempX1,tempY1),(tempX2,tempY2),(tempX3,tempY3),(x2,y2)
        n = len(P)-1
        
        Num_t=self.self_directed_sampling_size
        px, py = [None]*(Num_t+1),[None]*(Num_t+1)
        
        for j in range(Num_t+1):
            t = j / float(Num_t)
            px[j],py[j]=0.0,0.0
            for i in range(len(P)):
                px[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][0]
                py[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][1]
        return px, py

    
    # =============================================================================
    # get coordinates of an arrow
    # =============================================================================
    def get_arrow_xy_list(self, x,y,arrow_angle,arrow_size):
        last_lon1 = x[len(x)-2]
        last_lat1 = y[len(y)-2]
        last_lon2 = x[len(x)-1]
        last_lat2 = y[len(y)-1]
     
        #########################Left arrow line############################
        cs = math.cos(math.radians(arrow_angle))
        sn = math.sin(math.radians(arrow_angle))
        
        tempX = last_lon1 - last_lon2;
        tempY = last_lat1 - last_lat2;
        
        tempX = tempX*cs - tempY*sn;
        tempY = tempX*sn + tempY*cs;
        		
        tempX1 = tempX*arrow_size + last_lon2;
        tempY1 = tempY*arrow_size + last_lat2;
        
        #########################right arrow line############################
        cs = math.cos(math.radians(-arrow_angle))
        sn = math.sin(math.radians(-arrow_angle))
        
        tempX = last_lon1 - last_lon2;
        tempY = last_lat1 - last_lat2;
        
        tempX = tempX*cs - tempY*sn;
        tempY = tempX*sn + tempY*cs;
        		
        tempX2 = tempX*arrow_size + last_lon2;
        tempY2 = tempY*arrow_size + last_lat2;
        
        #########################combine two arrow lines############################
        arrow_x = [tempX1, last_lon2, tempX2]
        arrow_y = [tempY1, last_lat2, tempY2]
        return arrow_x, arrow_y
    

    # =============================================================================
    # load flow data from flow_matrix data and cluster center data
    # =============================================================================
    def load_flow_data(self, flow_matrix_file,cluster_info_file):
        # *************************************************************************
        frequncy_num_list = []
        frequncy_source_list = []
        frequncy_sink_list = []
        
        file_reader=open(flow_matrix_file, "r", encoding='UTF-8')
        line = file_reader.readline()
        cluster_count = len(line.replace('\n', '').split(','))
        line = file_reader.readline()
        while (line != ""):
            line = line.replace('\n', '')    
            temp_line_array = line.split(',')
            
            sink_cluster_id = int(temp_line_array[0])
            for i in range(1,cluster_count):
                source_cluster_id = i
                if temp_line_array[i]!='0.0':
                    frequncy_source_list.append(source_cluster_id)
                    frequncy_sink_list.append(sink_cluster_id)
                    frequncy_num_list.append(float(temp_line_array[i]))
            
            line = file_reader.readline()
        file_reader.close()  
        
        # *************************************************************************
        cluster_dict = {}
        file_reader=open(cluster_info_file, "r", encoding='UTF-8')
        line = file_reader.readline()
        line = file_reader.readline()
        while (line != ""):
            line = line.replace('\n', '')    
            temp_line_array = line.split(',')
            
            cluster_id = int(temp_line_array[0])+1
            center_x = float(temp_line_array[1])
            center_y = float(temp_line_array[2])
            weight = float(temp_line_array[3])
            
            cluster_dict[cluster_id] = [center_x,center_y,weight]
            
            line = file_reader.readline()
        file_reader.close()
        
        source_cluster_x_list=[]
        source_cluster_y_list=[]
        sink_cluster_x_list=[]
        sink_cluster_y_list=[]
        for i in range(0,len(frequncy_source_list)):
            source_id = frequncy_source_list[i]
            sink_id = frequncy_sink_list[i]
            source_cluster_x_list.append(cluster_dict[source_id][0])
            source_cluster_y_list.append(cluster_dict[source_id][1])
            sink_cluster_x_list.append(cluster_dict[sink_id][0])
            sink_cluster_y_list.append(cluster_dict[sink_id][1])
    
        # *************************************************************************
        data_tuples = list(zip(frequncy_source_list,frequncy_sink_list, \
                               source_cluster_x_list,source_cluster_y_list, \
                               sink_cluster_x_list,sink_cluster_y_list, frequncy_num_list))
        data = pd.DataFrame(data_tuples, columns=['Source','Sink','Source_X','Source_Y','Sink_X','Sink_Y','Frequncy'])
        return data
     
    # =============================================================================
    # 
    # =============================================================================
    def gen_flowmap_shp(self, flow_matrix_file, cluster_info_file, out_flow_map_file):
        # *************************************************************************  
        path_tuple = os.path.split(out_flow_map_file)
        shpdir = path_tuple[0]
        shpName = path_tuple[1].split('.')[0]
        if os.path.exists(out_flow_map_file) == False:
            if os.path.exists(shpdir) == False: self.mkdir(shpdir)
        else:
            dbfPath = shpdir + '/' + shpName + ".dbf"
            prjPath = shpdir + '/' + shpName + ".prj"
            sbnPath = shpdir + '/' + shpName + ".sbn"
            shxPath = shpdir + '/' + shpName + ".shx"
            if os.path.exists(dbfPath): os.remove(dbfPath)
            if os.path.exists(prjPath): os.remove(prjPath)
            if os.path.exists(sbnPath): os.remove(sbnPath)
            if os.path.exists(shxPath): os.remove(shxPath)
        
        # *************************************************************************
        data = self.load_flow_data(flow_matrix_file,cluster_info_file)    
        data = data.sort_values('Frequncy', ascending=False)
        
        # *************************************************************************
        f_array = np.sort(data['Frequncy'])
        quantile_val = np.sum(f_array)*self.flow_volume_percentage #0.9 #*0.75
        max_flow_count = self.flow_show_max_count #30 #len(data) * 0.1
        flow_count = 0
        temp_acc_val = 0
        for index, row in data.iterrows():
            temp_source = row['Source']
            temp_sink = row['Sink']
            temp_frequency = row['Frequncy']
            
            temp_acc_val = temp_acc_val + temp_frequency
            if flow_count==0:
                max_val = temp_frequency
            #if temp_source != temp_sink:
            flow_count = flow_count + 1
            if flow_count >= max_flow_count or temp_acc_val >= quantile_val or temp_frequency < self.flow_volume_minmum:
                min_val = temp_frequency
                break
        data = data.sort_values('Frequncy')
        
        # *************************************************************************
        m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
        node_dict = {}
        poDS = None
        try:
            gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
            gdal.SetConfigOption("SHAPE_ENCODING", "")
    
            pszDriverName = "ESRI Shapefile"
            ogr.RegisterAll()
            poDriver = ogr.GetDriverByName(pszDriverName)
            poDS = poDriver.CreateDataSource(out_flow_map_file)
            
            geomType = ogr.wkbLineString
            srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
            srs = osr.SpatialReference(srs_str)
            poLayer = poDS.CreateLayer(shpName, srs, geomType)
            
            oField1 = ogr.FieldDefn("count", ogr.OFTInteger)
            oField2 = ogr.FieldDefn("percentage", ogr.OFTReal)
            oField3 = ogr.FieldDefn("sink_id", ogr.OFTInteger)
            oField4 = ogr.FieldDefn("source_id", ogr.OFTInteger)
            poLayer.CreateField(oField1, 1)
            poLayer.CreateField(oField2, 1)
            poLayer.CreateField(oField3, 1)
            poLayer.CreateField(oField4, 1)
        
            oDefn = poLayer.GetLayerDefn()
            
            for index, row in data.iterrows():
                temp_source = row['Source']
                temp_sink = row['Sink']
                temp_x1 = row['Source_X']
                temp_y1 = row['Source_Y']
                temp_x2 = row['Sink_X']
                temp_y2 = row['Sink_Y']
                temp_frequency = row['Frequncy']        
                if temp_frequency < min_val: continue
    
                
                x1,y1=m(temp_x1, temp_y1)
                x2,y2=m(temp_x2, temp_y2)
                
                #********************************************************
                if temp_source not in node_dict.keys():
                    node_dict[temp_source]={}
                    node_dict[temp_source]["id"] = int(temp_source)
                    node_dict[temp_source]["x"] = int(x1)
                    node_dict[temp_source]["y"] = int(y1)
                
                if temp_sink not in node_dict.keys():
                    node_dict[temp_sink]={}
                    node_dict[temp_sink]["id"] = int(temp_sink)
                    node_dict[temp_sink]["x"] = int(x2)
                    node_dict[temp_sink]["y"] = int(y2)
                #********************************************************
                
                if temp_source == temp_sink: 
                    x, y = self.get_curve_close(x1+1000,y1+100,x2-1000,y2+100)
                else:
                    x, y = self.get_curve(x1,y1,x2,y2)
                
                tempGeom = ogr.Geometry(ogr.wkbLineString)
                for temp_idx in range(0,len(x)):
                    temp_x, temp_y=m(x[temp_idx], y[temp_idx], True)
                    tempGeom.SetPoint(temp_idx, temp_x, temp_y, 0)
                tempFeature = ogr.Feature(oDefn)
                tempFeature.SetGeometry(tempGeom)
                tempFeature.SetField(0, temp_frequency)
                tempFeature.SetField(1, temp_frequency/temp_acc_val)
                tempFeature.SetField(2, temp_sink)
                tempFeature.SetField(3, temp_source)
                
                poLayer.CreateFeature(tempFeature)
                del tempFeature
            #end for iteration
        
            poDS.FlushCache()
            del poDS
        except:
            if poDS != None: del poDS
        return node_dict
    
    # =============================================================================
    # 
    # =============================================================================
    def gen_flow_node_shp(self, node_dict, out_flow_node_file):
        #*****************************************************************************
        path_tuple = os.path.split(out_flow_node_file)
        shpdir = path_tuple[0]
        shpName = path_tuple[1].split('.')[0]
        if os.path.exists(out_flow_node_file) == False:
            if os.path.exists(shpdir) == False: self.mkdir(shpdir)
        else:
            dbfPath = shpdir + '/' + shpName + ".dbf"
            prjPath = shpdir + '/' + shpName + ".prj"
            sbnPath = shpdir + '/' + shpName + ".sbn"
            shxPath = shpdir + '/' + shpName + ".shx"
            if os.path.exists(dbfPath): os.remove(dbfPath)
            if os.path.exists(prjPath): os.remove(prjPath)
            if os.path.exists(sbnPath): os.remove(sbnPath)
            if os.path.exists(shxPath): os.remove(shxPath)
        
        m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
        poDS = None
        try:
            gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
            gdal.SetConfigOption("SHAPE_ENCODING", "")
    
            pszDriverName = "ESRI Shapefile"
            ogr.RegisterAll()
            poDriver = ogr.GetDriverByName(pszDriverName)
            poDS = poDriver.CreateDataSource(out_flow_node_file)
        
            geomType = ogr.wkbPolygon
            srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
            srs = osr.SpatialReference(srs_str)
            poLayer = poDS.CreateLayer(shpName, srs, geomType)
            
            oField1 = ogr.FieldDefn("id", ogr.OFTInteger)
            poLayer.CreateField(oField1, 1)
        
            oDefn = poLayer.GetLayerDefn()
            
            for index, item in node_dict.items():
                temp_id = item['id']
                temp_c_x = item['x']
                temp_c_y = item['y']
        
                tempGeom = ogr.Geometry(ogr.wkbLinearRing)
                for temp_idx in range(0,360):
                    temp_x = temp_c_x + 12000*math.cos(math.radians(temp_idx))
                    temp_y = temp_c_y + 12000*math.sin(math.radians(temp_idx))
                    temp_geo_x, temp_geo_y = m(temp_x, temp_y, True)
                    tempGeom.SetPoint(temp_idx, temp_geo_x, temp_geo_y, 0)
                tempGeom.CloseRings()
                tempPolygon = ogr.Geometry(ogr.wkbPolygon)
                tempPolygon.AddGeometry(tempGeom)
                
                tempFeature = ogr.Feature(oDefn)
                tempFeature.SetGeometry(tempPolygon)
                tempFeature.SetField(0, temp_id)
                
                poLayer.CreateFeature(tempFeature)
                del tempFeature
        
            poDS.FlushCache()
            del poDS
        except:
            if poDS != None: del poDS


    # =============================================================================
    # 
    # =============================================================================
    def gen_cluster_region_shp(self, tweet_data, out_region_shpPath):
        ##########################Begin for Shapefile################################
        path_tuple = os.path.split(out_region_shpPath)
        shpdir = path_tuple[0]
        shpName = path_tuple[1].split('.')[0]
        if os.path.exists(out_region_shpPath) == False:
            if os.path.exists(shpdir) == False: self.mkdir(shpdir)
        else:
            dbfPath = shpdir + '/' + shpName + ".dbf"
            prjPath = shpdir + '/' + shpName + ".prj"
            sbnPath = shpdir + '/' + shpName + ".sbn"
            shxPath = shpdir + '/' + shpName + ".shx"
            if os.path.exists(dbfPath): os.remove(dbfPath)
            if os.path.exists(prjPath): os.remove(prjPath)
            if os.path.exists(sbnPath): os.remove(sbnPath)
            if os.path.exists(shxPath): os.remove(shxPath)    
    
        poDS = None
        try:
            gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
            gdal.SetConfigOption("SHAPE_ENCODING", "")
        
            pszDriverName = "ESRI Shapefile"
            ogr.RegisterAll()
            poDriver = ogr.GetDriverByName(pszDriverName)
            poDS = poDriver.CreateDataSource(out_region_shpPath)
            
            geomType = ogr.wkbPolygon
            srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
            srs = osr.SpatialReference(srs_str)
            poLayer = poDS.CreateLayer(shpName, srs, geomType)
        
            oField1 = ogr.FieldDefn("c_id", ogr.OFTInteger)
            oField2 = ogr.FieldDefn("p_count", ogr.OFTInteger)
            poLayer.CreateField(oField1, 1)
            poLayer.CreateField(oField2, 1)
            
            oDefn = poLayer.GetLayerDefn()
            ##########################End for Shapefile################################
            
            ##########################Begin for preparing group################################
            id_points_group_map = {}
            coord_dict = {}
            id_points_count={}
            for index,item in tweet_data.iterrows():
                temp_cluster = item['sink_cluster']
                temp_x = '%.5f' % item['x']
                temp_y = '%.5f' % item['y']
                temp_key = temp_x + '_' + temp_y
                
                if (item['y']>72 or item['y']<-60): continue
                if temp_key in coord_dict.keys():
                    continue
                else:
                    coord_dict[temp_key] = 0
                
                if temp_cluster in id_points_group_map.keys():
                    id_points_group_map[temp_cluster].append(item)
                else:
                    id_points_group_map[temp_cluster]=[]
                    id_points_group_map[temp_cluster].append(item)
                    
                if temp_cluster in id_points_count.keys():
                    id_points_count[temp_cluster]=id_points_count[temp_cluster]+1
                else:
                    id_points_count[temp_cluster]=1
            ##########################End for preparing group################################
            
            ##########################Begin for preparing points################################
            multi_points_list = []
            group_id_sorted_list = sorted(id_points_group_map.keys())
            for group_id in group_id_sorted_list:
                temp_point_count = len(id_points_group_map[group_id])
                allPointsGeom = ogr.Geometry(ogr.wkbMultiPoint)
                for point_idx in range(0,temp_point_count):
                    tempGeom = ogr.Geometry(ogr.wkbPoint)
                    tempGeom.SetPoint(0, id_points_group_map[group_id][point_idx]['x'], id_points_group_map[group_id][point_idx]['y'], 0)
                    allPointsGeom.AddGeometry(tempGeom)
                multi_points_list.append(allPointsGeom)
            ##########################End for preparing points################################
            
            
            buffer_list = []
            buffer_id_list = []
            convex_list = []
            convex_id_list = []
            group_id_sorted_list = sorted(id_points_group_map.keys())
            #*************************************************************
            for group_id in group_id_sorted_list:
                temp_point_count = len(id_points_group_map[group_id])
                if (temp_point_count==2):
                    tempGeom = ogr.Geometry(ogr.wkbLineString)
                    tempGeom.SetPoint(0, id_points_group_map[group_id][0]['x'], id_points_group_map[group_id][0]['y'], 0)
                    tempGeom.SetPoint(1, id_points_group_map[group_id][1]['x'], id_points_group_map[group_id][1]['y'], 0)
                    buffer_area=tempGeom.Buffer(0.1)
                    buffer_list.append(buffer_area)
                    buffer_id_list.append(group_id)
                elif (temp_point_count==1):
                    tempGeom = ogr.Geometry(ogr.wkbPoint)
                    tempGeom.SetPoint(0, id_points_group_map[group_id][0]['x'], id_points_group_map[group_id][0]['y'], 0)
                    buffer_area=tempGeom.Buffer(0.1)
                    buffer_list.append(buffer_area)
                    buffer_id_list.append(group_id)
            
            #*************************************************************
            for group_id in group_id_sorted_list:
                temp_point_count = len(id_points_group_map[group_id])
                if (temp_point_count>2):
                    points = np.zeros((temp_point_count, 2))
                    for point_idx in range(0,temp_point_count):
                        points[point_idx][0] = id_points_group_map[group_id][point_idx]['x']
                        points[point_idx][1] = id_points_group_map[group_id][point_idx]['y']
                    tri = Delaunay(points)
                    triangle_count = len(tri.simplices)
                    multiGeom = ogr.Geometry(ogr.wkbMultiPolygon)
                    for tri_idx in range(0, triangle_count):
                        v_idx1 = tri.simplices[tri_idx][0]
                        v_idx2 = tri.simplices[tri_idx][1]
                        v_idx3 = tri.simplices[tri_idx][2]
                        tempGeom = ogr.Geometry(ogr.wkbLinearRing)
                        tempGeom.SetPoint(0, points[v_idx1][0], points[v_idx1][1], 0)
                        tempGeom.SetPoint(1, points[v_idx2][0], points[v_idx2][1], 0)
                        tempGeom.SetPoint(2, points[v_idx3][0], points[v_idx3][1], 0)
                        tempGeom.CloseRings()
                        tempPolygon = ogr.Geometry(ogr.wkbPolygon)
                        tempPolygon.AddGeometry(tempGeom)
        
                        flag = False
                        for idx in range(0,len(multi_points_list)):
                            group_id_1=group_id_sorted_list[idx]
                            if(group_id_1==group_id): continue
                            if (tempPolygon.Intersects(multi_points_list[idx])):
                                flag=True                     
                        if(flag==False):
                            tempPolygon = ogr.Geometry(ogr.wkbPolygon)
                            tempPolygon.AddGeometry(tempGeom)
                            multiGeom.AddGeometry(tempPolygon)
                    convex_list.append(multiGeom)
                    convex_id_list.append(group_id)
            
            #*************************************************************
            for convex_idx1 in range(0, len(convex_list)-1):
                temp_geom1 = convex_list[convex_idx1]
                temp_count1 = temp_geom1.GetGeometryCount()
                for convex_idx2 in range(convex_idx1+1, len(convex_list)):
                    temp_geom2 = convex_list[convex_idx2]
                    temp_count2 = temp_geom2.GetGeometryCount()
                    if (temp_geom1.Intersects(temp_geom2)):
                        if(temp_geom1.GetArea() > temp_geom2.GetArea()):
                            temp_geom1_copy = ogr.Geometry(ogr.wkbMultiPolygon)
                            for temp_p_idx in range(0, temp_count1):
                                if (temp_geom1.GetGeometryRef(temp_p_idx).Intersects(temp_geom2)==False):
                                    temp_geom1_copy.AddGeometry(temp_geom1.GetGeometryRef(temp_p_idx).Clone())
                            convex_list[convex_idx1]=temp_geom1_copy
                        else:
                            temp_geom2_copy = ogr.Geometry(ogr.wkbMultiPolygon)
                            for temp_p_idx in range(0, temp_count2):
                                if (temp_geom2.GetGeometryRef(temp_p_idx).Intersects(temp_geom1)==False):
                                    temp_geom2_copy.AddGeometry(temp_geom2.GetGeometryRef(temp_p_idx).Clone())
                            convex_list[convex_idx2]=temp_geom2_copy
                
            #*************************************************************
            for convex_idx in range(0, len(convex_list)):
                temp_geom = convex_list[convex_idx]
                temp_count = temp_geom.GetGeometryCount()
                for buffer_idx in range(0, len(buffer_list)):
                    temp_buffer = buffer_list[buffer_idx]
                    if (temp_geom.Intersects(temp_buffer)):
                        temp_geom_copy = ogr.Geometry(ogr.wkbMultiPolygon)
                        for temp_p_idx in range(0, temp_count):
                            if (temp_geom.GetGeometryRef(temp_p_idx).Intersects(temp_buffer)==False):
                                temp_geom_copy.AddGeometry(temp_geom.GetGeometryRef(temp_p_idx).Clone())
                        convex_list[convex_idx]=temp_geom_copy
            
            #*************************************************************
            for convex_idx in range(0, len(convex_list)):
                temp_geom = convex_list[convex_idx]
                temp_geos_geom = shapely.wkt.loads(temp_geom.ExportToWkt())
                dissolved = cascaded_union(temp_geos_geom)
                if (dissolved.geom_type=='MultiPolygon'):
                    temp_count = len(dissolved)
                    max_area = dissolved[0].area
                    max_id = 0
                    for temp_poly_idx in range(1, temp_count):
                        if (dissolved[temp_poly_idx].area > max_area):
                            max_area = dissolved[temp_poly_idx].area
                            max_id = temp_poly_idx
                    temp_p_count = len(dissolved[max_id].exterior.coords)
                    temp_exterior = ogr.Geometry(ogr.wkbLinearRing)
                    for p_idx in range(0, temp_p_count):
                        temp_exterior.SetPoint(p_idx, dissolved[max_id].exterior.coords[p_idx][0], \
                                                      dissolved[max_id].exterior.coords[p_idx][1], \
                                                      dissolved[max_id].exterior.coords[p_idx][2])
                    
                    temp_polygon = ogr.Geometry(ogr.wkbPolygon)
                    temp_polygon.AddGeometry(temp_exterior)
                    convex_list[convex_idx]=temp_polygon
                else:
                    temp_p_count = len(dissolved.exterior.coords)
                    temp_exterior = ogr.Geometry(ogr.wkbLinearRing)
                    for p_idx in range(0, temp_p_count):
                        temp_exterior.SetPoint(p_idx, dissolved.exterior.coords[p_idx][0], \
                                                      dissolved.exterior.coords[p_idx][1], \
                                                      dissolved.exterior.coords[p_idx][2])
                    
                    temp_polygon = ogr.Geometry(ogr.wkbPolygon)
                    temp_polygon.AddGeometry(temp_exterior)
                    convex_list[convex_idx]=temp_polygon
              
            #*************************************************************
            for convex_idx1 in range(0, len(convex_list)-1):
                temp_geom1 = convex_list[convex_idx1]
                for convex_idx2 in range(convex_idx1+1, len(convex_list)):
                    temp_geom2 = convex_list[convex_idx2]
                    if (temp_geom1.Intersects(temp_geom2)):
                        if(temp_geom1.GetArea() > temp_geom2.GetArea()):
                            temp_geom1 = temp_geom1.Difference(temp_geom2)
                            convex_list[convex_idx1]=temp_geom1
                        else:
                            temp_geom2 = temp_geom2.Difference(temp_geom1)
                            convex_list[convex_idx2]=temp_geom2
                            
            #*************************************************************
            for convex_idx in range(0, len(convex_list)):
                group_id = convex_id_list[convex_idx]
                tempFeature = ogr.Feature(oDefn)
                tempFeature.SetGeometry(convex_list[convex_idx])
                tempFeature.SetField(0, group_id)
                tempFeature.SetField(1, id_points_count[group_id])
                poLayer.CreateFeature(tempFeature)
                del tempFeature
                
            for buffer_idx in range(0, len(buffer_list)):
                group_id = buffer_id_list[buffer_idx]
                tempFeature = ogr.Feature(oDefn)
                tempFeature.SetGeometry(buffer_list[buffer_idx])
                tempFeature.SetField(0, group_id)
                tempFeature.SetField(1, id_points_count[group_id])
                poLayer.CreateFeature(tempFeature)
                del tempFeature
            poDS.FlushCache()
            del poDS
            ##########################End Write################################
        except:
            if poDS != None: del poDS

    
    # =============================================================================
    # 
    # =============================================================================
    def gen_points_shp(self,tweet_data,out_point_shpPath,with_compress=True,major_source_list=None):
        path_tuple = os.path.split(out_point_shpPath)
        shpdir = path_tuple[0]
        shpName = path_tuple[1].split('.')[0]
        if os.path.exists(out_point_shpPath) == False:
            if os.path.exists(shpdir) == False: self.mkdir(shpdir)
        else:
            dbfPath = shpdir + '/' + shpName + ".dbf"
            prjPath = shpdir + '/' + shpName + ".prj"
            sbnPath = shpdir + '/' + shpName + ".sbn"
            shxPath = shpdir + '/' + shpName + ".shx"
            if os.path.exists(dbfPath): os.remove(dbfPath)
            if os.path.exists(prjPath): os.remove(prjPath)
            if os.path.exists(sbnPath): os.remove(sbnPath)
            if os.path.exists(shxPath): os.remove(shxPath)
        
        poDS = None
        try:
            gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
            gdal.SetConfigOption("SHAPE_ENCODING", "")
    
            pszDriverName = "ESRI Shapefile"
            ogr.RegisterAll()
            poDriver = ogr.GetDriverByName(pszDriverName)
            poDS = poDriver.CreateDataSource(out_point_shpPath)
            
            geomType = ogr.wkbPoint
            srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
            srs = osr.SpatialReference(srs_str)
            poLayer = poDS.CreateLayer(shpName, srs, geomType)
            
            oField1 = ogr.FieldDefn("time", ogr.OFTString)
            oField2 = ogr.FieldDefn("tw_id", ogr.OFTString)
            oField3 = ogr.FieldDefn("retw_id", ogr.OFTString)
            oField4 = ogr.FieldDefn("tw_x", ogr.OFTReal)
            oField5 = ogr.FieldDefn("tw_y", ogr.OFTReal)
            oField6 = ogr.FieldDefn("retw_x", ogr.OFTReal)
            oField7 = ogr.FieldDefn("retw_y", ogr.OFTReal)
            oField8 = ogr.FieldDefn("distance", ogr.OFTReal)
            oField9 = ogr.FieldDefn("sink_cluster", ogr.OFTInteger)
            oField10 = ogr.FieldDefn("source_cluster", ogr.OFTInteger)
            oField11 = ogr.FieldDefn("stype", ogr.OFTInteger)
            
            poLayer.CreateField(oField1, 1)
            poLayer.CreateField(oField2, 1)
            poLayer.CreateField(oField3, 1)
            poLayer.CreateField(oField4, 1)
            poLayer.CreateField(oField5, 1)
            poLayer.CreateField(oField6, 1)
            poLayer.CreateField(oField7, 1)
            poLayer.CreateField(oField8, 1)
            poLayer.CreateField(oField9, 1)
            poLayer.CreateField(oField10, 1)
            poLayer.CreateField(oField11, 1)
        
            oDefn = poLayer.GetLayerDefn()
        
            coord_dict = {} #For removing points in same coordinate (saving only one), to reduce shapefile's size
            ##########################Begin for iteration################################
            for index,item in tweet_data.iterrows():
                temp_x = '%.5f' % item['x']
                temp_y = '%.5f' % item['y']
                temp_key = temp_x + '_' + temp_y
                
                if (item['y']>72 or item['y']<-60): continue
                if with_compress==True:
                    if temp_key in coord_dict.keys():
                        continue
                    else:
                        coord_dict[temp_key] = 0
                        
                tempGeom = ogr.Geometry(ogr.wkbPoint)
                tempGeom.SetPoint(0, item['x'], item['y'], 0)
                tempFeature = ogr.Feature(oDefn)
                tempFeature.SetGeometry(tempGeom)
                tempFeature.SetField(0, item['T'])
                tempFeature.SetField(1, item['tw_id'])
                tempFeature.SetField(2, item['retweeted_id'])
                tempFeature.SetField(3, item['x'])
                tempFeature.SetField(4, item['y'])
                tempFeature.SetField(5, item['retweeted_x'])
                tempFeature.SetField(6, item['retweeted_y'])
                tempFeature.SetField(7, item['dist'])            
                tempFeature.SetField(8, item['sink_cluster'])
                tempFeature.SetField(9, item['source_cluster'])
                if major_source_list is None:
                    tempFeature.SetField(10, -1)
                else:
                    if item['sink_cluster'] in major_source_list:
                        tempFeature.SetField(10, 1) # 1 indicates major source
                    else:
                        tempFeature.SetField(10, 0) # 0 indicates major sink
            
                poLayer.CreateFeature(tempFeature)
                del tempFeature
             
            ##########################End for iteration################################   
            poDS.FlushCache()
            del poDS
        except:
            if poDS != None: del poDS
    





















# =============================================================================
# 
# =============================================================================
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

# =============================================================================
# 
# =============================================================================
def gen_potential_shp(p_cluster_data,shpPath,with_compress=True,major_source_list=None):
    
    path_tuple = os.path.split(shpPath)
    shpdir = path_tuple[0]
    shpName = path_tuple[1].split('.')[0]
    if os.path.exists(shpPath) == False:
        if os.path.exists(shpdir) == False: mkdir(shpdir)
    else:
        dbfPath = shpdir + '/' + shpName + ".dbf"
        prjPath = shpdir + '/' + shpName + ".prj"
        sbnPath = shpdir + '/' + shpName + ".sbn"
        shxPath = shpdir + '/' + shpName + ".shx"
        if os.path.exists(dbfPath): os.remove(dbfPath)
        if os.path.exists(prjPath): os.remove(prjPath)
        if os.path.exists(sbnPath): os.remove(sbnPath)
        if os.path.exists(shxPath): os.remove(shxPath)
    
    poDS = None
    try:
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        pszDriverName = "ESRI Shapefile"
        ogr.RegisterAll()
        poDriver = ogr.GetDriverByName(pszDriverName)
        poDS = poDriver.CreateDataSource(shpPath)
        
        geomType = ogr.wkbPoint
        srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
        srs = osr.SpatialReference(srs_str)
        poLayer = poDS.CreateLayer(shpName, srs, geomType)
        
        oField1 = ogr.FieldDefn("c_id", ogr.OFTInteger)
        oField2 = ogr.FieldDefn("c_x", ogr.OFTReal)
        oField3 = ogr.FieldDefn("c_y", ogr.OFTReal)
        oField4 = ogr.FieldDefn("c_radius", ogr.OFTReal)
        oField5 = ogr.FieldDefn("c_weight", ogr.OFTReal)
        
        poLayer.CreateField(oField1, 1)
        poLayer.CreateField(oField2, 1)
        poLayer.CreateField(oField3, 1)
        poLayer.CreateField(oField4, 1)
        poLayer.CreateField(oField5, 1)
    
        oDefn = poLayer.GetLayerDefn()
    
        ##########################Begin for iteration################################
        for index,item in p_cluster_data.iterrows():
            tempGeom = ogr.Geometry(ogr.wkbPoint)
            tempGeom.SetPoint(0, item['center_x'], item['center_y'], 0)
            tempFeature = ogr.Feature(oDefn)
            tempFeature.SetGeometry(tempGeom)
            tempFeature.SetField(0, item['cluster_id'])
            tempFeature.SetField(1, item['center_x'])
            tempFeature.SetField(2, item['center_y'])
            tempFeature.SetField(3, item['weight'])
            tempFeature.SetField(4, item['radius'])
            
            poLayer.CreateFeature(tempFeature)
            del tempFeature
         
        ##########################End for iteration################################   
        poDS.FlushCache()
        del poDS
    except:
        if poDS != None: del poDS

# =============================================================================
# 
# =============================================================================
def gen_points_triangle_shp(tweet_data,shpPath):
    ##########################Begin for Shapefile################################
    path_tuple = os.path.split(shpPath)
    shpdir = path_tuple[0]
    shpName = path_tuple[1].split('.')[0]
    if os.path.exists(shpPath) == False:
        if os.path.exists(shpdir) == False: mkdir(shpdir)
    else:
        dbfPath = shpdir + '/' + shpName + ".dbf"
        prjPath = shpdir + '/' + shpName + ".prj"
        sbnPath = shpdir + '/' + shpName + ".sbn"
        shxPath = shpdir + '/' + shpName + ".shx"
        if os.path.exists(dbfPath): os.remove(dbfPath)
        if os.path.exists(prjPath): os.remove(prjPath)
        if os.path.exists(sbnPath): os.remove(sbnPath)
        if os.path.exists(shxPath): os.remove(shxPath)    

    poDS = None
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "")

    pszDriverName = "ESRI Shapefile"
    ogr.RegisterAll()
    poDriver = ogr.GetDriverByName(pszDriverName)
    poDS = poDriver.CreateDataSource(shpPath)
    
    geomType = ogr.wkbPolygon
    srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
    srs = osr.SpatialReference(srs_str)
    poLayer = poDS.CreateLayer(shpName, srs, geomType)

    oField1 = ogr.FieldDefn("c_id", ogr.OFTInteger)
    oField2 = ogr.FieldDefn("p_count", ogr.OFTInteger)
    poLayer.CreateField(oField1, 1)
    poLayer.CreateField(oField2, 1)
    
    oDefn = poLayer.GetLayerDefn()
    ##########################End for Shapefile################################
    
    ##########################Begin for preparing group################################
    id_points_group_map = {}
    coord_dict = {}
    id_points_count={}
    for index,item in tweet_data.iterrows():
        temp_cluster = item['sink_cluster']
        temp_x = '%.5f' % item['x']
        temp_y = '%.5f' % item['y']
        temp_key = temp_x + '_' + temp_y
        
        if (item['y']>72 or item['y']<-60): continue
        if temp_key in coord_dict.keys():
            continue
        else:
            coord_dict[temp_key] = 0
        
        if temp_cluster in id_points_group_map.keys():
            id_points_group_map[temp_cluster].append(item)
        else:
            id_points_group_map[temp_cluster]=[]
            id_points_group_map[temp_cluster].append(item)
            
        if temp_cluster in id_points_count.keys():
            id_points_count[temp_cluster]=id_points_count[temp_cluster]+1
        else:
            id_points_count[temp_cluster]=1
    ##########################End for preparing group################################
    
    ##########################Begin for preparing points################################
    multi_points_list = []
    group_id_sorted_list = sorted(id_points_group_map.keys())
    for group_id in group_id_sorted_list:
        temp_point_count = len(id_points_group_map[group_id])
        allPointsGeom = ogr.Geometry(ogr.wkbMultiPoint)
        for point_idx in range(0,temp_point_count):
            tempGeom = ogr.Geometry(ogr.wkbPoint)
            tempGeom.SetPoint(0, id_points_group_map[group_id][point_idx]['x'], id_points_group_map[group_id][point_idx]['y'], 0)
            allPointsGeom.AddGeometry(tempGeom)
        multi_points_list.append(allPointsGeom)
    ##########################End for preparing points################################
    
    
    buffer_list = []
    buffer_id_list = []
    convex_list = []
    convex_id_list = []
    group_id_sorted_list = sorted(id_points_group_map.keys())
    #*************************************************************
    for group_id in group_id_sorted_list:
        temp_point_count = len(id_points_group_map[group_id])
        if (temp_point_count==2):
            tempGeom = ogr.Geometry(ogr.wkbLineString)
            tempGeom.SetPoint(0, id_points_group_map[group_id][0]['x'], id_points_group_map[group_id][0]['y'], 0)
            tempGeom.SetPoint(1, id_points_group_map[group_id][1]['x'], id_points_group_map[group_id][1]['y'], 0)
            buffer_area=tempGeom.Buffer(0.1)
            buffer_list.append(buffer_area)
            buffer_id_list.append(group_id)
        elif (temp_point_count==1):
            tempGeom = ogr.Geometry(ogr.wkbPoint)
            tempGeom.SetPoint(0, id_points_group_map[group_id][0]['x'], id_points_group_map[group_id][0]['y'], 0)
            buffer_area=tempGeom.Buffer(0.1)
            buffer_list.append(buffer_area)
            buffer_id_list.append(group_id)
    
    #*************************************************************
    for group_id in group_id_sorted_list:
        temp_point_count = len(id_points_group_map[group_id])
        if (temp_point_count>2):
            points = np.zeros((temp_point_count, 2))
            for point_idx in range(0,temp_point_count):
                points[point_idx][0] = id_points_group_map[group_id][point_idx]['x']
                points[point_idx][1] = id_points_group_map[group_id][point_idx]['y']
            tri = Delaunay(points)
            triangle_count = len(tri.simplices)
            multiGeom = ogr.Geometry(ogr.wkbMultiPolygon)
            for tri_idx in range(0, triangle_count):
                v_idx1 = tri.simplices[tri_idx][0]
                v_idx2 = tri.simplices[tri_idx][1]
                v_idx3 = tri.simplices[tri_idx][2]
                tempGeom = ogr.Geometry(ogr.wkbLinearRing)
                tempGeom.SetPoint(0, points[v_idx1][0], points[v_idx1][1], 0)
                tempGeom.SetPoint(1, points[v_idx2][0], points[v_idx2][1], 0)
                tempGeom.SetPoint(2, points[v_idx3][0], points[v_idx3][1], 0)
                tempGeom.CloseRings()
                tempPolygon = ogr.Geometry(ogr.wkbPolygon)
                tempPolygon.AddGeometry(tempGeom)

                flag = False
                for idx in range(0,len(multi_points_list)):
                    group_id_1=group_id_sorted_list[idx]
                    if(group_id_1==group_id): continue
                    if (tempPolygon.Intersects(multi_points_list[idx])):
                        flag=True                     
                if(flag==False):
                    tempPolygon = ogr.Geometry(ogr.wkbPolygon)
                    tempPolygon.AddGeometry(tempGeom)
                    multiGeom.AddGeometry(tempPolygon)
            convex_list.append(multiGeom)
            convex_id_list.append(group_id)
    
    #*************************************************************
    for convex_idx1 in range(0, len(convex_list)-1):
        temp_geom1 = convex_list[convex_idx1]
        temp_count1 = temp_geom1.GetGeometryCount()
        for convex_idx2 in range(convex_idx1+1, len(convex_list)):
            temp_geom2 = convex_list[convex_idx2]
            temp_count2 = temp_geom2.GetGeometryCount()
            if (temp_geom1.Intersects(temp_geom2)):
                if(temp_geom1.GetArea() > temp_geom2.GetArea()):
                    temp_geom1_copy = ogr.Geometry(ogr.wkbMultiPolygon)
                    for temp_p_idx in range(0, temp_count1):
                        if (temp_geom1.GetGeometryRef(temp_p_idx).Intersects(temp_geom2)==False):
                            temp_geom1_copy.AddGeometry(temp_geom1.GetGeometryRef(temp_p_idx).Clone())
                    convex_list[convex_idx1]=temp_geom1_copy
                else:
                    temp_geom2_copy = ogr.Geometry(ogr.wkbMultiPolygon)
                    for temp_p_idx in range(0, temp_count2):
                        if (temp_geom2.GetGeometryRef(temp_p_idx).Intersects(temp_geom1)==False):
                            temp_geom2_copy.AddGeometry(temp_geom2.GetGeometryRef(temp_p_idx).Clone())
                    convex_list[convex_idx2]=temp_geom2_copy
        
    #*************************************************************
    for convex_idx in range(0, len(convex_list)):
        temp_geom = convex_list[convex_idx]
        temp_count = temp_geom.GetGeometryCount()
        for buffer_idx in range(0, len(buffer_list)):
            temp_buffer = buffer_list[buffer_idx]
            if (temp_geom.Intersects(temp_buffer)):
                temp_geom_copy = ogr.Geometry(ogr.wkbMultiPolygon)
                for temp_p_idx in range(0, temp_count):
                    if (temp_geom.GetGeometryRef(temp_p_idx).Intersects(temp_buffer)==False):
                        temp_geom_copy.AddGeometry(temp_geom.GetGeometryRef(temp_p_idx).Clone())
                convex_list[convex_idx]=temp_geom_copy
    
    #*************************************************************
    for convex_idx in range(0, len(convex_list)):
        temp_geom = convex_list[convex_idx]
        temp_geos_geom = shapely.wkt.loads(temp_geom.ExportToWkt())
        dissolved = cascaded_union(temp_geos_geom)
        if (dissolved.geom_type=='MultiPolygon'):
            temp_count = len(dissolved)
            max_area = dissolved[0].area
            max_id = 0
            for temp_poly_idx in range(1, temp_count):
                if (dissolved[temp_poly_idx].area > max_area):
                    max_area = dissolved[temp_poly_idx].area
                    max_id = temp_poly_idx
            temp_p_count = len(dissolved[max_id].exterior.coords)
            temp_exterior = ogr.Geometry(ogr.wkbLinearRing)
            for p_idx in range(0, temp_p_count):
                temp_exterior.SetPoint(p_idx, dissolved[max_id].exterior.coords[p_idx][0], \
                                              dissolved[max_id].exterior.coords[p_idx][1], \
                                              dissolved[max_id].exterior.coords[p_idx][2])
            
            temp_polygon = ogr.Geometry(ogr.wkbPolygon)
            temp_polygon.AddGeometry(temp_exterior)
            convex_list[convex_idx]=temp_polygon
        else:
            temp_p_count = len(dissolved.exterior.coords)
            temp_exterior = ogr.Geometry(ogr.wkbLinearRing)
            for p_idx in range(0, temp_p_count):
                temp_exterior.SetPoint(p_idx, dissolved.exterior.coords[p_idx][0], \
                                              dissolved.exterior.coords[p_idx][1], \
                                              dissolved.exterior.coords[p_idx][2])
            
            temp_polygon = ogr.Geometry(ogr.wkbPolygon)
            temp_polygon.AddGeometry(temp_exterior)
            convex_list[convex_idx]=temp_polygon
      
    #*************************************************************
    for convex_idx1 in range(0, len(convex_list)-1):
        temp_geom1 = convex_list[convex_idx1]
        for convex_idx2 in range(convex_idx1+1, len(convex_list)):
            temp_geom2 = convex_list[convex_idx2]
            if (temp_geom1.Intersects(temp_geom2)):
                if(temp_geom1.GetArea() > temp_geom2.GetArea()):
                    temp_geom1 = temp_geom1.Difference(temp_geom2)
                    convex_list[convex_idx1]=temp_geom1
                else:
                    temp_geom2 = temp_geom2.Difference(temp_geom1)
                    convex_list[convex_idx2]=temp_geom2
                    
    #*************************************************************
    for convex_idx in range(0, len(convex_list)):
        group_id = convex_id_list[convex_idx]
        tempFeature = ogr.Feature(oDefn)
        tempFeature.SetGeometry(convex_list[convex_idx])
        tempFeature.SetField(0, group_id)
        tempFeature.SetField(1, id_points_count[group_id])
        poLayer.CreateFeature(tempFeature)
        del tempFeature
        
    for buffer_idx in range(0, len(buffer_list)):
        group_id = buffer_id_list[buffer_idx]
        tempFeature = ogr.Feature(oDefn)
        tempFeature.SetGeometry(buffer_list[buffer_idx])
        tempFeature.SetField(0, group_id)
        tempFeature.SetField(1, id_points_count[group_id])
        poLayer.CreateFeature(tempFeature)
        del tempFeature
    poDS.FlushCache()
    del poDS
    ##########################End Write################################

# =============================================================================
# 
# =============================================================================
def gen_points_shp(tweet_data,shpPath,with_compress=True,major_source_list=None):

    path_tuple = os.path.split(shpPath)
    shpdir = path_tuple[0]
    shpName = path_tuple[1].split('.')[0]
    if os.path.exists(shpPath) == False:
        if os.path.exists(shpdir) == False: mkdir(shpdir)
    else:
        dbfPath = shpdir + '/' + shpName + ".dbf"
        prjPath = shpdir + '/' + shpName + ".prj"
        sbnPath = shpdir + '/' + shpName + ".sbn"
        shxPath = shpdir + '/' + shpName + ".shx"
        if os.path.exists(dbfPath): os.remove(dbfPath)
        if os.path.exists(prjPath): os.remove(prjPath)
        if os.path.exists(sbnPath): os.remove(sbnPath)
        if os.path.exists(shxPath): os.remove(shxPath)
    
    poDS = None
    try:
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        pszDriverName = "ESRI Shapefile"
        ogr.RegisterAll()
        poDriver = ogr.GetDriverByName(pszDriverName)
        poDS = poDriver.CreateDataSource(shpPath)
        
        geomType = ogr.wkbPoint
        srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
        srs = osr.SpatialReference(srs_str)
        poLayer = poDS.CreateLayer(shpName, srs, geomType)
        
        oField1 = ogr.FieldDefn("time", ogr.OFTString)
        oField2 = ogr.FieldDefn("tw_id", ogr.OFTString)
        oField3 = ogr.FieldDefn("retw_id", ogr.OFTString)
        oField4 = ogr.FieldDefn("tw_x", ogr.OFTReal)
        oField5 = ogr.FieldDefn("tw_y", ogr.OFTReal)
        oField6 = ogr.FieldDefn("retw_x", ogr.OFTReal)
        oField7 = ogr.FieldDefn("retw_y", ogr.OFTReal)
        oField8 = ogr.FieldDefn("distance", ogr.OFTReal)
        oField9 = ogr.FieldDefn("sink_cluster", ogr.OFTInteger)
        oField10 = ogr.FieldDefn("source_cluster", ogr.OFTInteger)
        oField11 = ogr.FieldDefn("stype", ogr.OFTInteger)
        
        poLayer.CreateField(oField1, 1)
        poLayer.CreateField(oField2, 1)
        poLayer.CreateField(oField3, 1)
        poLayer.CreateField(oField4, 1)
        poLayer.CreateField(oField5, 1)
        poLayer.CreateField(oField6, 1)
        poLayer.CreateField(oField7, 1)
        poLayer.CreateField(oField8, 1)
        poLayer.CreateField(oField9, 1)
        poLayer.CreateField(oField10, 1)
        poLayer.CreateField(oField11, 1)
    
        oDefn = poLayer.GetLayerDefn()
    
        coord_dict = {} #For removing points in same coordinate (saving only one), to reduce shapefile's size
        ##########################Begin for iteration################################
        for index,item in tweet_data.iterrows():
            temp_x = '%.5f' % item['x']
            temp_y = '%.5f' % item['y']
            temp_key = temp_x + '_' + temp_y
            
            if (item['y']>72 or item['y']<-60): continue
            if with_compress==True:
                if temp_key in coord_dict.keys():
                    continue
                else:
                    coord_dict[temp_key] = 0
                    
            tempGeom = ogr.Geometry(ogr.wkbPoint)
            tempGeom.SetPoint(0, item['x'], item['y'], 0)
            tempFeature = ogr.Feature(oDefn)
            tempFeature.SetGeometry(tempGeom)
            tempFeature.SetField(0, item['T'])
            tempFeature.SetField(1, item['tw_id'])
            tempFeature.SetField(2, item['retweeted_id'])
            tempFeature.SetField(3, item['x'])
            tempFeature.SetField(4, item['y'])
            tempFeature.SetField(5, item['retweeted_x'])
            tempFeature.SetField(6, item['retweeted_y'])
            tempFeature.SetField(7, item['dist'])            
            tempFeature.SetField(8, item['sink_cluster'])
            tempFeature.SetField(9, item['source_cluster'])
            if major_source_list is None:
                tempFeature.SetField(10, -1)
            else:
                if item['sink_cluster'] in major_source_list:
                    tempFeature.SetField(10, 1) # 1 indicates major source
                else:
                    tempFeature.SetField(10, 0) # 0 indicates major sink
        
            poLayer.CreateFeature(tempFeature)
            del tempFeature
         
        ##########################End for iteration################################   
        poDS.FlushCache()
        del poDS
    except:
        if poDS != None: del poDS


# =============================================================================
# 
# =============================================================================
def get_curve(x1,y1,x2,y2):
    tempX1 = -(y1 - y2)/3 + (x1+x2)/2
    tempY1 = (x1 - x2)/3 + (y1+y2)/2
    
    P=(x1,y1),(tempX1,tempY1),(x2,y2)
    n = len(P)-1
    
    line_len = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
    
    Num_t=int(math.ceil(line_len/10000))
    px, py = [None]*(Num_t+1),[None]*(Num_t+1)
    
    for j in range(Num_t+1):
        t = j / float(Num_t)
        px[j],py[j]=0.0,0.0
        for i in range(len(P)):
            px[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][0]
            py[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][1]
    
    px1, py1 = [None]*(Num_t-1),[None]*(Num_t-1)
    for j in range(Num_t-1):
        px1[j] = px[j+1]
        py1[j] = py[j+1]
    return px1, py1

# =============================================================================
# 
# =============================================================================
def get_curve_close(x1,y1,x2,y2):
    size = 80000 #800000
    tempX1 = size/1.2 + (x1+x2)/2
    tempY1 = size + (y1+y2)/2
    
    tempX2 = (x1+x2)/2
    tempY2 = size + (y1+y2)/2
    
    tempX3 = -size/1.2 + (x1+x2)/2
    tempY3 = size + (y1+y2)/2
    
    P=(x1,y1),(tempX1,tempY1),(tempX2,tempY2),(tempX3,tempY3),(x2,y2)
    n = len(P)-1
    
    Num_t=100
    px, py = [None]*(Num_t+1),[None]*(Num_t+1)
    
    for j in range(Num_t+1):
        t = j / float(Num_t)
        px[j],py[j]=0.0,0.0
        for i in range(len(P)):
            px[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][0]
            py[j] += binom(n,i)*t**i*(1-t)**(n-i)*P[i][1]
    return px, py


# =============================================================================
# load flow data from flow_matrix data and cluster center data
# =============================================================================
def load_flow_data(flow_matrix_file,cluster_info_file):
    # *************************************************************************
    frequncy_num_list = []
    frequncy_source_list = []
    frequncy_sink_list = []
    
    file_reader=open(flow_matrix_file, "r", encoding='UTF-8')
    line = file_reader.readline()
    cluster_count = len(line.replace('\n', '').split(','))
    line = file_reader.readline()
    while (line != ""):
        line = line.replace('\n', '')    
        temp_line_array = line.split(',')
        
        sink_cluster_id = int(temp_line_array[0])
        for i in range(1,cluster_count):
            source_cluster_id = i
            if temp_line_array[i]!='0.0':
                frequncy_source_list.append(source_cluster_id)
                frequncy_sink_list.append(sink_cluster_id)
                frequncy_num_list.append(float(temp_line_array[i]))
        
        line = file_reader.readline()
    file_reader.close()  
    
    # *************************************************************************
    cluster_dict = {}
    file_reader=open(cluster_info_file, "r", encoding='UTF-8')
    line = file_reader.readline()
    line = file_reader.readline()
    while (line != ""):
        line = line.replace('\n', '')    
        temp_line_array = line.split(',')
        
        cluster_id = int(temp_line_array[0])+1
        center_x = float(temp_line_array[1])
        center_y = float(temp_line_array[2])
        weight = float(temp_line_array[3])
        
        cluster_dict[cluster_id] = [center_x,center_y,weight]
        
        line = file_reader.readline()
    file_reader.close()
    
    source_cluster_x_list=[]
    source_cluster_y_list=[]
    sink_cluster_x_list=[]
    sink_cluster_y_list=[]
    for i in range(0,len(frequncy_source_list)):
        source_id = frequncy_source_list[i]
        sink_id = frequncy_sink_list[i]
        source_cluster_x_list.append(cluster_dict[source_id][0])
        source_cluster_y_list.append(cluster_dict[source_id][1])
        sink_cluster_x_list.append(cluster_dict[sink_id][0])
        sink_cluster_y_list.append(cluster_dict[sink_id][1])

    # *************************************************************************
    data_tuples = list(zip(frequncy_source_list,frequncy_sink_list, \
                           source_cluster_x_list,source_cluster_y_list, \
                           sink_cluster_x_list,sink_cluster_y_list, frequncy_num_list))
    data = pd.DataFrame(data_tuples, columns=['Source','Sink','Source_X','Source_Y','Sink_X','Sink_Y','Frequncy'])
    return data
 
# =============================================================================
# 
# =============================================================================
def gen_flowmap_shp(case_name, date_index, flow_matrix_file, cluster_info_file, flow_map_file):
    # *************************************************************************  
    path_tuple = os.path.split(flow_map_file)
    shpdir = path_tuple[0]
    shpName = path_tuple[1].split('.')[0]
    if os.path.exists(flow_map_file) == False:
        if os.path.exists(shpdir) == False: mkdir(shpdir)
    else:
        dbfPath = shpdir + '/' + shpName + ".dbf"
        prjPath = shpdir + '/' + shpName + ".prj"
        sbnPath = shpdir + '/' + shpName + ".sbn"
        shxPath = shpdir + '/' + shpName + ".shx"
        if os.path.exists(dbfPath): os.remove(dbfPath)
        if os.path.exists(prjPath): os.remove(prjPath)
        if os.path.exists(sbnPath): os.remove(sbnPath)
        if os.path.exists(shxPath): os.remove(shxPath)
    
    # *************************************************************************
    data = load_flow_data(flow_matrix_file,cluster_info_file)    
    data = data.sort_values('Frequncy', ascending=False)
    
    # *************************************************************************
    f_array = np.sort(data['Frequncy'])
    quantile_val = np.sum(f_array)*0.9 #*0.75
    max_flow_count = 30 #len(data) * 0.1
    flow_count = 0
    temp_acc_val = 0
    for index, row in data.iterrows():
        temp_source = row['Source']
        temp_sink = row['Sink']
        temp_frequency = row['Frequncy']
        
        temp_acc_val = temp_acc_val + temp_frequency
        if flow_count==0:
            max_val = temp_frequency
        #if temp_source != temp_sink:
        flow_count = flow_count + 1
        if flow_count >= max_flow_count or temp_acc_val >= quantile_val or temp_frequency < 5: 
            min_val = temp_frequency
            break
    data = data.sort_values('Frequncy')
    
    # *************************************************************************
    m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    node_dict = {}
    poDS = None
    try:
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        pszDriverName = "ESRI Shapefile"
        ogr.RegisterAll()
        poDriver = ogr.GetDriverByName(pszDriverName)
        poDS = poDriver.CreateDataSource(flow_map_file)
        
        geomType = ogr.wkbLineString
        srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
        srs = osr.SpatialReference(srs_str)
        poLayer = poDS.CreateLayer(shpName, srs, geomType)
        
        oField1 = ogr.FieldDefn("count", ogr.OFTInteger)
        oField2 = ogr.FieldDefn("percentage", ogr.OFTReal)
        oField3 = ogr.FieldDefn("sink_id", ogr.OFTInteger)
        oField4 = ogr.FieldDefn("source_id", ogr.OFTInteger)
        poLayer.CreateField(oField1, 1)
        poLayer.CreateField(oField2, 1)
        poLayer.CreateField(oField3, 1)
        poLayer.CreateField(oField4, 1)
    
        oDefn = poLayer.GetLayerDefn()
        
        for index, row in data.iterrows():
            temp_source = row['Source']
            temp_sink = row['Sink']
            temp_x1 = row['Source_X']
            temp_y1 = row['Source_Y']
            temp_x2 = row['Sink_X']
            temp_y2 = row['Sink_Y']
            temp_frequency = row['Frequncy']        
            if temp_frequency < min_val: continue

            
            x1,y1=m(temp_x1, temp_y1)
            x2,y2=m(temp_x2, temp_y2)
            
            #********************************************************
            if temp_source not in node_dict.keys():
                node_dict[temp_source]={}
                node_dict[temp_source]["id"] = int(temp_source)
                node_dict[temp_source]["x"] = int(x1)
                node_dict[temp_source]["y"] = int(y1)
            
            if temp_sink not in node_dict.keys():
                node_dict[temp_sink]={}
                node_dict[temp_sink]["id"] = int(temp_sink)
                node_dict[temp_sink]["x"] = int(x2)
                node_dict[temp_sink]["y"] = int(y2)
            #********************************************************
            
            if temp_source == temp_sink: 
                x, y = get_curve_close(x1+1000,y1+100,x2-1000,y2+100)
            else:
                x, y = get_curve(x1,y1,x2,y2)
            
            tempGeom = ogr.Geometry(ogr.wkbLineString)
            for temp_idx in range(0,len(x)):
                temp_x, temp_y=m(x[temp_idx], y[temp_idx], True)
                tempGeom.SetPoint(temp_idx, temp_x, temp_y, 0)
            tempFeature = ogr.Feature(oDefn)
            tempFeature.SetGeometry(tempGeom)
            tempFeature.SetField(0, temp_frequency)
            tempFeature.SetField(1, temp_frequency/temp_acc_val)
            tempFeature.SetField(2, temp_sink)
            tempFeature.SetField(3, temp_source)
            
            poLayer.CreateFeature(tempFeature)
            del tempFeature
        #end for iteration
    
        poDS.FlushCache()
        del poDS
    except:
        if poDS != None: del poDS
    return node_dict

# =============================================================================
# 
# =============================================================================
def gen_flow_node_shp(node_dict, flow_node_file):
    #*****************************************************************************
    path_tuple = os.path.split(flow_node_file)
    shpdir = path_tuple[0]
    shpName = path_tuple[1].split('.')[0]
    if os.path.exists(flow_node_file) == False:
        if os.path.exists(shpdir) == False: mkdir(shpdir)
    else:
        dbfPath = shpdir + '/' + shpName + ".dbf"
        prjPath = shpdir + '/' + shpName + ".prj"
        sbnPath = shpdir + '/' + shpName + ".sbn"
        shxPath = shpdir + '/' + shpName + ".shx"
        if os.path.exists(dbfPath): os.remove(dbfPath)
        if os.path.exists(prjPath): os.remove(prjPath)
        if os.path.exists(sbnPath): os.remove(sbnPath)
        if os.path.exists(shxPath): os.remove(shxPath)
    
    m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    poDS = None
    try:
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        pszDriverName = "ESRI Shapefile"
        ogr.RegisterAll()
        poDriver = ogr.GetDriverByName(pszDriverName)
        poDS = poDriver.CreateDataSource(flow_node_file)
    
        geomType = ogr.wkbPolygon
        srs_str = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
        srs = osr.SpatialReference(srs_str)
        poLayer = poDS.CreateLayer(shpName, srs, geomType)
        
        oField1 = ogr.FieldDefn("id", ogr.OFTInteger)
        poLayer.CreateField(oField1, 1)
    
        oDefn = poLayer.GetLayerDefn()
        
        for index, item in node_dict.items():
            temp_id = item['id']
            temp_c_x = item['x']
            temp_c_y = item['y']
    
            tempGeom = ogr.Geometry(ogr.wkbLinearRing)
            for temp_idx in range(0,360):
                temp_x = temp_c_x + 12000*math.cos(math.radians(temp_idx))
                temp_y = temp_c_y + 12000*math.sin(math.radians(temp_idx))
                temp_geo_x, temp_geo_y = m(temp_x, temp_y, True)
                tempGeom.SetPoint(temp_idx, temp_geo_x, temp_geo_y, 0)
            tempGeom.CloseRings()
            tempPolygon = ogr.Geometry(ogr.wkbPolygon)
            tempPolygon.AddGeometry(tempGeom)
            
            tempFeature = ogr.Feature(oDefn)
            tempFeature.SetGeometry(tempPolygon)
            tempFeature.SetField(0, temp_id)
            
            poLayer.CreateFeature(tempFeature)
            del tempFeature
    
        poDS.FlushCache()
        del poDS
    except:
        if poDS != None: del poDS

# =============================================================================
# 
# =============================================================================
for number in range(1,21):        
    base_dir = 'C:/manqi/'
    case_name = 'Sandy_weather/'
    case_type = 'clusterdata_e_3.0_tp_Median/'
    interval_name = 'GeoDenStream_PotentialClusterInfo'+str(number)
    shapefile_name = 'PotentialCluster'+str(number)
    tweet_data = pd.read_csv(base_dir+case_name+case_type+'clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    
    shpPath = base_dir + case_name+case_type + 'potential_cluster_shp/' + shapefile_name + '.shp'
    
    gen_potential_shp(tweet_data, shpPath)
    print([case_name, number])

# =============================================================================
# 
# =============================================================================
for number in range(1,21):        
    base_dir = 'C:/manqi/'
    case_name = 'Sandy_weather/'
    case_type = 'clusterdata_e_3.0_tp_Median/'
    interval_name = 'GeoDenStream_Cluster'+str(number)
    shapefile_name = 'DenStream'+str(number)
    tweet_data = pd.read_csv(base_dir+case_name+case_type+'clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    
    shpPath = base_dir + case_name+case_type + 'cluster_shp_compress/' + shapefile_name + '.shp'
    
    gen_points_shp(tweet_data, shpPath)
    print([case_name, number])

# =============================================================================
# 
# =============================================================================
for number in range(1,21):
    date_index = str(number)
    case_name = 'Sandy_weather'
    den_type = 'clusterdata_e_3.0_tp_Median'
    flow_matrix_file = 'C:/manqi/'+case_name+'/'+den_type+'/flow_matrix/flowprob_matrix'+str(date_index)+'.csv'
    cluster_info_file = 'C:/manqi/'+case_name+'/'+den_type+'/clusters_den_stream/GeoDenStream_ClusterInfo'+str(date_index)+'.csv'
    flow_map_file = 'C:/manqi/'+case_name+'/'+den_type+'/cluster_flowmap_shp/'+case_name+'_flowmap'+str(date_index) + '.shp'

    node_dict = gen_flowmap_shp(case_name,date_index,flow_matrix_file,cluster_info_file,flow_map_file)
    
    flow_node_file = 'C:/manqi/'+case_name+'/'+den_type+'/cluster_flownode_shp/'+case_name+'_flownode'+str(date_index) + '.shp'
    gen_flow_node_shp(node_dict,flow_node_file)
    print(date_index)


# =============================================================================
# 
# =============================================================================
for number in range(1,21):        
    base_dir = 'C:/manqi/'
    case_name = 'Sandy_weather/'
    case_type = 'clusterdata_e_3.0_tp_Median/'
    interval_name = 'GeoDenStream_Cluster'+str(number)
    shapefile_name = 'Region'+str(number)
    tweet_data = pd.read_csv(base_dir+case_name+case_type+'clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    
    shpPath = base_dir + case_name+case_type + 'cluster_region_shp/' + shapefile_name + '.shp'
    
    gen_points_triangle_shp(tweet_data, shpPath)
    print([case_name, number])


# =============================================================================
# 
# =============================================================================
# =============================================================================
# 
# =============================================================================
for number in range(1,18):        
    base_dir = 'C:/manqi/'
    case_name = 'Ebola/'
    case_type = 'clusterdata_e_3.0_week_tp_Median/'
    interval_name = 'GeoDenStream_PotentialClusterInfo'+str(number)
    shapefile_name = 'PotentialCluster'+str(number)
    tweet_data = pd.read_csv(base_dir+case_name+case_type+'clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    
    shpPath = base_dir + case_name+case_type + 'potential_cluster_shp/' + shapefile_name + '.shp'
    
    gen_potential_shp(tweet_data, shpPath)
    print([case_name, number])

# =============================================================================
# 
# =============================================================================
for number in range(1,18):        
    base_dir = 'C:/manqi/'
    case_name = 'Ebola/'
    case_type = 'clusterdata_e_3.0_week_tp_Median/'
    interval_name = 'GeoDenStream_Cluster'+str(number)
    shapefile_name = 'DenStream'+str(number)
    tweet_data = pd.read_csv(base_dir+case_name+case_type+'clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    
    shpPath = base_dir + case_name+case_type + 'cluster_shp_compress/' + shapefile_name + '.shp'
    
    gen_points_shp(tweet_data, shpPath)
    print([case_name, number])

# =============================================================================
# 
# =============================================================================
for item in range(1,18):
    date_index = str(item)
    case_name = 'Ebola'
    den_type = 'clusterdata_e_3.0_week_tp_Median'
    flow_matrix_file = 'C:/manqi/'+case_name+'/'+den_type+'/flow_matrix/flowprob_matrix'+str(date_index)+'.csv'
    cluster_info_file = 'C:/manqi/'+case_name+'/'+den_type+'/clusters_den_stream/GeoDenStream_ClusterInfo'+str(date_index)+'.csv'
    flow_map_file = 'C:/manqi/'+case_name+'/'+den_type+'/cluster_flowmap_shp/'+case_name+'_flowmap'+str(date_index) + '.shp'

    gen_flowmap_shp(case_name,date_index,flow_matrix_file,cluster_info_file,flow_map_file)
    print(date_index)


# =============================================================================
# 
# =============================================================================
for number in range(1,18):        
    base_dir = 'C:/manqi/'
    case_name = 'Ebola/'
    case_type = 'clusterdata_e_3.0_week_tp_Median/'
    interval_name = 'GeoDenStream_Cluster'+str(number)
    shapefile_name = 'Region'+str(number)
    tweet_data = pd.read_csv(base_dir+case_name+case_type+'clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    
    shpPath = base_dir + case_name+case_type + 'cluster_region_shp/' + shapefile_name + '.shp'
    
    gen_points_triangle_shp(tweet_data, shpPath)
    print([case_name, number])
    
    

# =============================================================================
# For Sandy_weather all day
# =============================================================================
for number in range(1,21):
    date_index = str(number)
    case_name = 'Sandy_weather'
    case_type = 'clusterdata_e_3.0_tp_Median'
    interval_name = 'GeoDenStream_Cluster'+str(number)
    
    tweet_data = pd.read_csv('C:/manqi/'+case_name+'/'+case_type+'/clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    flow_matrix_file = 'C:/manqi/'+case_name+'/'+case_type+'/flow_matrix/flowprob_matrix'+str(date_index)+'.csv'
    cluster_info_file = 'C:/manqi/'+case_name+'/'+case_type+'/clusters_den_stream/GeoDenStream_ClusterInfo'+str(date_index)+'.csv'
    
    out_flow_map_file = 'C:/manqi/'+case_name+'/'+case_type+'/cluster_flowmap_shp/'+case_name+'_flowmap'+str(date_index) + '.shp'
    out_flow_node_file = 'C:/manqi/'+case_name+'/'+case_type+'/cluster_flownode_shp/'+case_name+'_flownode'+str(date_index) + '.shp'
    out_cluster_region_file = 'C:/manqi/'+case_name+'/'+case_type+'/cluster_region_shp/'+case_name+'_region'+str(date_index) + '.shp'
    out_cluster_point_file = 'C:/manqi/'+case_name+'/'+case_type + '/cluster_shp_compress/'+'DenStream'+str(number) + '.shp'
    
    fsg = flow_shape_generator()
    fsg.set_curve_parameter(10000,100,80000)
    fsg.set_flow_statistic_parameter(5, 0.9, 30)

    node_dict = fsg.gen_flowmap_shp(flow_matrix_file,cluster_info_file,out_flow_map_file)
    fsg.gen_flow_node_shp(node_dict,out_flow_node_file)
    fsg.gen_cluster_region_shp(tweet_data, out_cluster_region_file)
    fsg.gen_points_shp(tweet_data, out_cluster_point_file)
    print(date_index)


# =============================================================================
# For Ebola weekly
# =============================================================================
for number in range(1,18):
    date_index = str(number)
    case_name = 'Ebola'
    case_type = 'clusterdata_e_3.0_week_tp_Median'
    interval_name = 'GeoDenStream_Cluster'+str(number)
    
    tweet_data = pd.read_csv('C:/manqi/'+case_name+'/'+case_type+'/clusters_den_stream/'+interval_name+'.csv', encoding='latin1')
    flow_matrix_file = 'C:/manqi/'+case_name+'/'+case_type+'/flow_matrix/flowprob_matrix'+str(date_index)+'.csv'
    cluster_info_file = 'C:/manqi/'+case_name+'/'+case_type+'/clusters_den_stream/GeoDenStream_ClusterInfo'+str(date_index)+'.csv'
    
    out_flow_map_file = 'C:/manqi/'+case_name+'/'+case_type+'/cluster_flowmap_shp/'+case_name+'_flowmap'+str(date_index) + '.shp'
    out_flow_node_file = 'C:/manqi/'+case_name+'/'+case_type+'/cluster_flownode_shp/'+case_name+'_flownode'+str(date_index) + '.shp'
    out_cluster_region_file = 'C:/manqi/'+case_name+'/'+case_type+'/cluster_region_shp/'+case_name+'_region'+str(date_index) + '.shp'
    out_cluster_point_file = 'C:/manqi/'+case_name+'/'+case_type + '/cluster_shp_compress/'+'DenStream'+str(number) + '.shp'
    
    fsg = flow_shape_generator()
    fsg.set_curve_parameter(10000,100,800000)
    fsg.set_flow_statistic_parameter(100, 0.9, 30)

    node_dict = fsg.gen_flowmap_shp(flow_matrix_file,cluster_info_file,out_flow_map_file)
    fsg.gen_flow_node_shp(node_dict,out_flow_node_file)
    fsg.gen_cluster_region_shp(tweet_data, out_cluster_region_file)
    fsg.gen_points_shp(tweet_data, out_cluster_point_file)
    print(date_index)
    