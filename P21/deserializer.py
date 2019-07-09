# JSON files deserializer (we can adapt it for other problems so we always use the same library)
import json

def load_data():
	with open('P21.json') as data_file:    
	    data = json.load(data_file)

	v_max = data["vehicle_v_max"]
	obstacles = []
	starts = data["start_positions"]
	goals = data["goal_positions"]
	b_polygon = data["bounding_polygon"]
	for i in range(1, 100):
		try:
			obstacles.append(data["obstacle_" + str(i)])
		except:
			break
	return v_max, obstacles, starts, goals, b_polygon