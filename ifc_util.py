# author: Jia-Rui Lin@Tsinghua
# date: Jan 08, 2014
# site: https://linjiarui.net

import numpy as np
import ifcopenshell as ios
import ifcopenshell.geom as igm

#==========Util Functions for Geometric Properties============
# @Shilpa what's shown in your screenshot is not the coordinates of a vertex. It is the coordinates of the object placement. This can be done with one line of code using ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement). This will give you a matrix which includes that location in absolute coordinates.
# Note that these are global engineering coordinates. If your file contains georeferencing map conversions, you may want to then further apply the map conversion to get map grid coordinates. You can use ifcopenshell.util.geolocation.local2global or ifcopenshell.util.geolocation.xyz2enh for this.
# Then, should you wish to find the absolute coordinate of a local coordinate of a particular vertex within the shape, you may multiply the coordinate by the matrix.
def get_location(ifc_obj):
    if hasattr(ifc_obj,'ObjectPlacement'):
        from ifcopenshell.util.placement import get_local_placement
        local_matrix=get_local_placement(ifc_obj.ObjectPlacement)
        return local_matrix[0:3,3]
    return None

def distance(pos1,pos2):
    return np.linalg.norm(pos2-pos1)

def max_distance(positions):
    count=len(positions)
    max_dist=float('-inf')
    for i in range(count):
        p1=positions[i]
        for j in range(i+1,count):
            p2=positions[j]
            dist=distance(p1,p2)
            if dist>max_dist:max_dist=dist
    return max_dist

def min_distance(positions):
    count=len(positions)
    min_dist=float('inf')
    for i in range(count):
        p1=positions[i]
        for j in range(i+1,count):
            p2=positions[j]
            dist=distance(p1,p2)
            if dist<min_dist:min_dist=dist
    return min_dist
#===============================

def get_attr(ifc_obj,name):
    if name.lower()=='position' or name.lower()=='objectplacement':#hack object position
        return get_location(ifc_obj)
    if name.lower()=='type' and ifc_obj is not None:#hack object type
        return ifc_obj.is_a()
    
    if hasattr(ifc_obj,name):
        return getattr(ifc_obj,name)
    return None

# one can retrieve a data attribute via obj.AttrA.AttrC
def get_chained_attr(ifc_obj,name):
    import itertools
    from collections.abc import Iterable
    
    attrs=name.split('.')
    attrs.reverse()
    
        
    results=[]
    results.append(ifc_obj)
    while len(attrs)>0:
        attr=attrs.pop()
        if len(attr.strip())==0:break
        
        temp=[]
        temp=[get_attr(obj,attr) for obj in results]
        
        temp=[item for item in temp if item is not None]
        
        results=list(itertools.chain.from_iterable(temp)) if isinstance(temp[0],Iterable) and not isinstance(temp[0],str) else temp
        if len(results)==0: return None #this means no attribute is found or no value is returned
    
    #print(results)
    return results[0] if len(results)==1 else results

def get_single_prop(ifc_obj,name):
    prop_sets=[]
    for rel in ifc_obj.IsDefinedBy:
        if rel.is_a('IfcRelDefinesByProperties'):
            prop_def=rel.RelatingPropertyDefinition
            prop_sets.append(prop_def)
        elif rel.is_a('IfcRelDefinesByType'):
            obj_type=rel.RelatingType
            psets=obj_type.HasPropertySets
            if psets is not None: prop_sets.extend(psets)
        else:
            continue
    
    for prop_def in prop_sets:
        if prop_def.is_a('IfcElementQuantity'):
            for quantity in prop_def.Quantities:
                if quantity.is_a('IfcQuantityLength'):
                    if quantity.Name==name: return quantity.LengthValue
                elif quantity.is_a('IfcQuantityArea'):
                    if quantity.Name==name: return quantity.AreaValue
                elif quantity.is_a('IfcQuantityVolume'):
                    if quantity.Name==name: return quantity.VolumeValue
                elif quantity.is_a('IfcQuantityCount'):
                    if quantity.Name==name: return quantity.CountValue
                elif quantity.is_a('IfcQuantityWeight'):
                    if quantity.Name==name: return quantity.WeightValue
                elif quantity.is_a('IfcQuantityTime'):
                    if quantity.Name==name: return quantity.TimeValue
                else:continue #there are more complex quantity types
        elif prop_def.is_a('IfcPropertySet'):
            for property in prop_def.HasProperties:
                if property.is_a('IfcPropertySingleValue'):
                    if property.Name==name: return property.NominalValue.wrappedValue if property.NominalValue else None
                else:continue #there are more types
        else:continue #there are more types

    return None

def get_prop(ifc_obj,name):
    val=get_chained_attr(ifc_obj,name) if '.' in name else get_attr(ifc_obj,name)
    return val if val is not None else get_single_prop(ifc_obj,name)

def get_psets(ifc_obj):
    return ios.util.element.get_psets(ifc_obj)

def get_elements_in_spatial(ifc_spatial):
    elements=[]
    if ifc_spatial.ContainsElements and len(ifc_spatial.ContainsElements)>0:
        for relContain in ifc_spatial.ContainsElements:
            if not (relContain.RelatedElements and len(relContain.RelatedElements)>0): continue
            elements.extend(relContain.RelatedElements)
    
    if ifc_spatial.IsDecomposedBy and len(ifc_spatial.IsDecomposedBy)>0:
        for relAgg in ifc_spatial.IsDecomposedBy:
            if not (relAgg.RelatedObjects and len(relAgg.RelatedObjects)>0): continue
            for relObj in relAgg.RelatedObjects:
                elems=get_elements_in_spatial(relObj)
                elements.extend(elems)
    
    return elements

def open_ifc(file_path):
    #print('ifc_util called')
    return ios.open(file_path)