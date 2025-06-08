from mcp.server.fastmcp import FastMCP

from ifc_util import *

mcp=FastMCP("ifcMCP")

@mcp.tool()
def greet(name:str) -> str:
    return f"Hello, {name}"

@mcp.tool()
def get_entities(file_path:str, entity_type:str):
    """
    Get IFC entities with a specific type in an ifc file, only globalId and name of each entity are returned
    
    Parameters:
        file_path: path to the ifc file
        entity_type: type of IFC entity (e.g., "IfcDoor")
    """
    #print('method called')
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
    #print('ifc file opened')
    entities=ifc_model.by_type(entity_type)
    #print('entities retrieved')
    
    results=[]
    
    for i,entity in enumerate(entities):
        
        globalId=get_prop(entity,'GlobalId')
        name=get_prop(entity,'Name')
        results.append({
            'globalId':globalId,
            'name':name,
            'type':entity_type
        })
     
    return results

@mcp.tool()
def get_named_property_of_entities(file_path:str, globalIds:list[str], prop_name:str):
    """
    Get property with a certain name of all entities
    
    Parameters:
        file_path: path to the ifc file
        globalIds: globalIds of all the entities
        prop_name: name of the property
    """
    #print('method called')
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
        
    results=[]
    
    for globalId in globalIds:
        entity=ifc_model.by_guid(globalId)
        if entity is None: continue
        
        prop=get_prop(entity,prop_name)
        results.append({
            'globalId':globalId,
            prop_name:prop
        })
     
    return results

@mcp.tool()
def get_entity_properties(file_path:str, globalId:str):
    """
    Get all properties of an entity with a certain GlobalId in an ifc file
    
    Parameters:
        file_path: path to the ifc file
        globalId: GlobalId of IFC entity
    """
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
    
    entity=ifc_model.by_guid(globalId)
    if entity is None: return "error, the entity is not found"
    
    prop_data={
        'globalId':get_prop(entity,'GlobalId'),
        'name':get_prop(entity,'Name'),
        'description':get_prop(entity,'Description'),
        'type':entity.is_a(),
        'property_sets':{}
    }
    
    psets=get_psets(entity)
    for ps_name,pset_props in psets.items():
        prop_data['property_sets'][ps_name]=pset_props
    
    return prop_data

@mcp.tool()
def get_entity_location(file_path:str, globalId:str):
    """
    Get location of an entity with a certain GlobalId in an ifc file
    
    Parameters:
        file_path: path to the ifc file
        globalId: GlobalId of IFC entity
    """
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
    
    entity=ifc_model.by_guid(globalId)
    if entity is None: return "error, the entity is not found"
    
    loc=get_location(entity)
    return loc

@mcp.tool()
def get_entities_in_spatial(file_path:str, globalId:str):
    """
    Get globalIds of entities in a spatial structure (IfcSpace, IfcBuildingStorey, IfcBuilding, IfcSite) with globalId in an ifc file
    
    Parameters:
        file_path: path to the ifc file
        globalId: GlobalId of the spatial structure
    """
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
    
    spatial=ifc_model.by_guid(globalId)
    if spatial is None: return "error, the spatial structure is not found"
    
    globalIds=[]
    for ele in get_elements_in_spatial(spatial):
        globalIds.append(ele.GlobalId)
    
    return globalIds


@mcp.tool()
def get_openings_on_wall(file_path:str, globalId:str):
    """
    Get globalId, type, name of openings (IfcWindow, IfcDoor) on a certain wall in an ifc file
    
    Parameters:
        file_path: path to the ifc file
        globalId: GlobalId of the wall
    """
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
    
    wall=ifc_model.by_guid(globalId)
    if wall is None: return "error, the wall is not found"
    
    results=[]
    if wall.HasOpenings and len(wall.HasOpenings)>0:
        for opening in wall.HasOpenings:
            ele=opening.RelatingBuildingElement
            if ele:
                results.append({
                    'globalId':ele.GlobalId,
                    'type':ele.is_a(),
                    'name':ele.Name
                })
    return results

@mcp.tool()
def get_space_boundaries(file_path:str, globalId:str):
    """
    Get globalId, type, name of boundaries (IfcWindow, IfcDoor, IfcWall, etc.) of a certain space in an ifc file
    
    Parameters:
        file_path: path to the ifc file
        globalId: GlobalId of the space
    """
    ifc_model=open_ifc(file_path)
    if ifc_model is None: return "error, the file is not found or broken"
    
    space=ifc_model.by_guid(globalId)
    if space is None: return "error, the space is not found"
    
    results=[]
    if space.BoundedBy and len(space.BoundedBy)>0:
        for boundedBy in space.BoundedBy:
            ele=boundedBy.RelatedBuildingElement
            if ele:
                results.append({
                    'globalId':ele.GlobalId,
                    'type':ele.is_a(),
                    'name':ele.Name
                })
    return results

if __name__ == '__main__':
    #mcp.run(transport="stdio")  # Default, so transport argument is optional
    mcp.run(transport="streamable-http") # default port 8000, access streamable-http mcp server via http://127.0.01:8000/mcp
    #mcp.run(transport="sse")