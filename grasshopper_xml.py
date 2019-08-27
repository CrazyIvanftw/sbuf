from lxml import etree
import datetime

def make_numeric_parameter(param_name, unit_string, datatype_string, value_string):
    parameter = etree.Element("Input", name=param_name, unit=unit_string, value_datatype=datatype_string, value=value_string)
    return parameter

def make_string_parameter(param_name, value_string):
    parameter = etree.Element("Input", name=param_name, value_datatype="string", value=value_string)
    return parameter

def make_spacial_parameter(param_name, unit_string, datatype_string, x_value_string, y_value_string, z_value_string):
    parameter = etree.Element("Input", name=param_name, unit=unit_string, value_datatype=datatype_string, x=x_value_string, y=y_value_string, z=z_value_string)
    return parameter

def make_pair_parameter(param_name, name1, unit1, datatype1, value1, name2, unit2, datatype2, value2):
    param1 = make_numeric_parameter(name1, unit1, datatype1, value1)
    param2 = make_numeric_parameter(name2, unit2, datatype2, value2)
    parameter = make_parameter_pair(param_name, param1, param2)
    return parameter

def make_parameter_group(param_string, *params):
    group = etree.Element("Group", name=param_string)
    index = 0
    for param in list(params):
        param.set("index", str(index))
        group.append(param)
        index = index + 1
    return group

def make_parameter_pair(param_string, param1, param2):
    pair = etree.Element("Pair", name=param_string)
    param1.set("index", "0")
    param2.set("index", "1")
    pair.append(param1)
    pair.append(param2)
    return pair

def make_4x4matrix(v):
    r1c1 = make_numeric_parameter("Cell", "value", "double", v[0])
    r1c2 = make_numeric_parameter("Cell", "value", "double", v[1])
    r1c3 = make_numeric_parameter("Cell", "value", "double", v[2])
    r1c4 = make_numeric_parameter("Cell", "value", "double", v[3])
    r2c1 = make_numeric_parameter("Cell", "value", "double", v[4])
    r2c2 = make_numeric_parameter("Cell", "value", "double", v[5])
    r2c3 = make_numeric_parameter("Cell", "value", "double", v[6])
    r2c4 = make_numeric_parameter("Cell", "value", "double", v[7])
    r3c1 = make_numeric_parameter("Cell", "value", "double", v[8])
    r3c2 = make_numeric_parameter("Cell", "value", "double", v[9])
    r3c3 = make_numeric_parameter("Cell", "value", "double", v[10])
    r3c4 = make_numeric_parameter("Cell", "value", "double", v[11])
    r4c1 = make_numeric_parameter("Cell", "value", "double", v[12])
    r4c2 = make_numeric_parameter("Cell", "value", "double", v[13])
    r4c3 = make_numeric_parameter("Cell", "value", "double", v[14])
    r4c4 = make_numeric_parameter("Cell", "value", "double", v[15])
    r1 = make_parameter_group("Row", r1c1, r1c2, r1c3, r1c4)
    r2 = make_parameter_group("Row", r2c1, r2c2, r2c3, r2c4)
    r3 = make_parameter_group("Row", r3c1, r3c2, r3c3, r3c4)
    r4 = make_parameter_group("Row", r4c1, r4c2, r4c3, r4c4)
    m = make_parameter_group("Matrix", r1, r2, r3, r4)
    return m


#setup_vals = ["10", "60", "300", "LTH-IRB2400", "230.0", "110.0", "55.0", "1000.0", "2.0", "2000.0", "2.0", "350.0", "1.0", "50", "2", "0", "0.6", "0.4", "20.0", "5.0", "6.5"]
def make_setup(v):
    drop_distance = make_numeric_parameter("Drop Distance", "mm", "int", v[0])
    vertical_margin = make_numeric_parameter("Vertical Margin", "mm", "int", v[1])
    podium_height = make_numeric_parameter("Podium Height", "mm", "int", v[2])
    robot = make_string_parameter("Robot", v[3])
    brick_size = make_spacial_parameter("Brick Size", "mm", "double", v[4], v[5], v[6])

    speed0 = make_pair_parameter("Speed", "LinearSpeed", "mm/s", "double", v[7], "AngularSpeed", "rad/s", "double", v[8])
    speed1 = make_pair_parameter("Speed", "LinearSpeed", "mm/s", "double", v[9], "AngularSpeed", "rad/s", "double", v[10])
    speed2 = make_pair_parameter("Speed", "LinearSpeed", "mm/s", "double", v[11], "AngularSpeed", "rad/s", "double", v[12])
    speeds = make_parameter_group("Speeds", speed0, speed1, speed2)

    zone0 = make_numeric_parameter("Zone", "mm", "int", v[13])
    zone1 = make_numeric_parameter("Zone", "mm", "int", v[14])
    zone2 = make_numeric_parameter("Zone", "mm", "int", v[15])
    zones = make_parameter_group("Zones", zone0, zone1, zone2)

    wait_time = make_numeric_parameter("Wait Time", "s", "double", v[16])
    gripper_close_time = make_numeric_parameter("Gripper Close Time", "s", "double", v[17])

    grip_margin = make_numeric_parameter("Grip Margin", "mm", "double", v[18])
    tool_weight_unloaded = make_numeric_parameter("Tool Weight Unloaded", "kg", "double", v[19])
    tool_weight_loaded = make_numeric_parameter("Tool Weight Loaded", "kg", "double", v[20])
    tool = make_parameter_group("Tool", grip_margin, tool_weight_unloaded, tool_weight_loaded)

    setup = make_parameter_group("Setup", drop_distance, vertical_margin, podium_height, robot, brick_size, speeds, zones, wait_time, gripper_close_time, tool)
    return setup


#pick_geometry_vals = ["10.0", "3", "3", "600.0", "-760.0", "385.0","127.0.0.1", "3333", "999", "10", "120", "10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","516.8", "35.3"]
def make_pick_geometry(v):
    #Simple Stack
    distance_between_bricks = make_numeric_parameter("Distance Between Bricks", "mm", "double", v[0])
    ss_number_of_bricks = make_pair_parameter("Number Of Bricks", "x", "count", "int", v[1], "y", "count", "int", v[2])
    ss_reference_point = make_spacial_parameter("Reference Point", "mm", "double", v[3], v[4], v[5])
    simple_stack = make_parameter_group("Simple Stack", distance_between_bricks, ss_number_of_bricks, ss_reference_point)

    #Pick By Vision
    ip = make_string_parameter("IP Address", v[6])
    port = make_string_parameter("Port", v[7])
    pattern = make_string_parameter("Pattern", v[8])
    upper_limit_id = make_numeric_parameter("Upper Limit ID", "id", "int", v[9])
    lower_limit_id = make_numeric_parameter("Lower Limit ID", "id", "int", v[10])
    matrix = make_4x4matrix(v[11:27])
    z_brick_height = make_numeric_parameter("Z Brick Height", "mm", "double", v[27])
    angle = make_numeric_parameter("Angle", "degrees", "double", v[28])
    pick_by_vision = make_parameter_group("Pick By Vision", ip, port, pattern, upper_limit_id, lower_limit_id, matrix, z_brick_height, angle)

    #Pick Geometry
    pick_geometry = make_parameter_group("Pick Geometry", simple_stack, pick_by_vision)
    return pick_geometry

#place_geometry_vals = ["10.0", "0.0", "0.0", "0.25", "3", "3", "595.24", "727.44", "385.00", "5.0", "0.546", "0", "595.24", "727.44", "385.00", "0"]
def make_place_geometry(v):
    #Förband = Simple Wall
    seam0 = make_numeric_parameter("Seam", "mm", "double", v[0])
    seam1 = make_numeric_parameter("Seam", "mm", "double", v[1])
    seam2 = make_numeric_parameter("Seam", "mm", "double", v[2])
    seam_size = make_parameter_group("Seam Size", seam0, seam1, seam2)
    part_size_of_one_brick_moved = make_numeric_parameter("Part Size Of One Brick Moved", "mm", "double", v[3])
    sw_number_of_bricks = make_pair_parameter("Number Of Bricks", "x", "count", "int", v[4], "y", "count", "int", v[5])
    sw_reference_point = make_spacial_parameter("Reference Point", "mm", "double", v[6], v[7], v[8])
    simple_wall = make_parameter_group("Simple Wall", seam_size, part_size_of_one_brick_moved, sw_number_of_bricks, sw_reference_point)

    #Qirui
    z_margin = make_numeric_parameter("Z Margin", "mm", "double", v[9])
    angle_to_rotate = make_numeric_parameter("Angle To Rotate", "degrees", "double", v[10])
    number_of_bricks_to_move_upwards = make_numeric_parameter("Number Of Bricks To Move Upwards", "count", "int", v[11])
    q_reference_point = make_spacial_parameter("Reference Point", "mm", "double", v[12], v[13], v[14])
    number_of_bricks_already_layed = make_numeric_parameter("Number Of Bricks Already Layed", "count", "int", v[15])
    qirui_wall = make_parameter_group("Qirui Wall", z_margin, angle_to_rotate, number_of_bricks_to_move_upwards, q_reference_point, number_of_bricks_already_layed)
    #Place Geometry
    place_geometry = make_parameter_group("Place Geometry", simple_wall, qirui_wall)
    return place_geometry

def make_save_xml(save_name, setup_vals, pick_vals, place_vals):
    datetime_object = datetime.datetime.now()
    setup = make_setup(setup_vals)
    pick_geometry = make_pick_geometry(pick_vals)
    place_geometry = make_place_geometry(place_vals)
    save_xml = make_parameter_group(save_name, setup, pick_geometry, place_geometry)
    save_xml.set("Created",str(datetime_object))
    return save_xml

#This isn't working, I'll have to get it working tomorrow 
def parse_file(xml_file):
    root = etree.XML(xml_file)
    tree = etree.ElementTree(root)
    print(etree.tostring(tree))

def main():
    setup_vals = ["10", "60", "300", "LTH-IRB2400", "230.0", "110.0", "55.0", "1000.0", "2.0", "2000.0", "2.0", "350.0", "1.0", "50", "2", "0", "0.6", "0.4", "20.0", "5.0", "6.5"]
    pick_geometry_vals = ["10.0", "3", "3", "600.0", "-760.0", "385.0","127.0.0.1", "3333", "999", "10", "120", "10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","10.0","516.8", "35.3"]
    place_geometry_vals = ["10.0", "0.0", "0.0", "0.25", "3", "3", "595.24", "727.44", "385.00", "5.0", "0.546", "0", "595.24", "727.44", "385.00", "0"]
    xml = make_save_xml("Grasshopper Input", setup_vals, pick_geometry_vals, place_geometry_vals)
    file = etree.Element("File", file_name="Default.xml")
    file.append(xml)
    print(etree.tostring(file, pretty_print=True, xml_declaration=True).decode('UTF-8'))

if __name__ == '__main__':
    main()
