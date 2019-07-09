# JSON files deserializer (we can adapt it for other problems so we always use the same library)
import json

def load_data_P2():
	with open('../json_files/P22.json') as data_file:    
	    data = json.load(data_file)

	v_max = data["vehicle_v_max"]
	points = data["points_of_interest"]
	obstacles = []
	starts = data["start_positions"]
	goals = data["goal_positions"]
	b_polygon = data["bounding_polygon"]
	for i in range(1, 100):
		try:
			obstacles.append(data["obstacle_" + str(i)])
		except:
			break
	return v_max, points, obstacles, starts, goals, b_polygon

def load_data_P3():
	with open('json_files/P23.json') as data_file:    
	    data = json.load(data_file)

	v_max = data["vehicle_v_max"]
	points = data["points_of_interest"]
	obstacles = []
	starts = data["start_positions"]
	goals = data["goal_positions"]
	b_polygon = data["bounding_polygon"]
	for i in range(1, 100):
		try:
			obstacles.append(data["obstacle_" + str(i)])
		except:
			break
	s_range = data["sensor_range"]
	return v_max, points, obstacles, starts, goals, b_polygon, s_range