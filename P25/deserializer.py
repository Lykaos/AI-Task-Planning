# JSON files deserializer (we can adapt it for other problems so we always use the same library)
import json

def load_data():
	with open('P25.json') as data_file:    
	    data = json.load(data_file)

	v_max = data["vehicle_v_max"]
	a_max = data["vehicle_a_max"]
	obstacles = []
	starts = data["start_positions"]
	goals = []#data["goal_positions"]
	form_pos = data["formation_positions"]
	b_polygon = data["bounding_polygon"]
	for i in range(1, 100):
		try:
			obstacles.append(data["obstacle_" + str(i)])
		except:
			break
	return v_max, a_max,starts, form_pos, b_polygon

def load_traj():
	with open('P25_26_traj.json') as data_file:    
	    data = json.load(data_file)

	t = data["t"]
	theta = data["theta"]
	x = data["x"]
	y = data["y"]

	return t,theta,x,y