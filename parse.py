def parse_bluetooth_info(filename, pi_local):
	file = open(filename, 'r+')
	for line in file:
		pi_local[line[0]] = line[2:19]

	file.close()

def parse_pi_info(filename, pi_local, seating):
	file = open(filename, 'r+')
	for line in file:
		seating[line[0]] = pi_local[line[2]]


def parse_seating(bt, pi, seating):
	pi_local = {}
	bt_info = open(bt, 'r+')
	pi_info = open(pi, 'r+')
	for line in bt_info:
		pi_local[line[0]] = line[2:19]
	for line in pi_info:
		seating[line[0]] = pi_local[line[2]]
	pi_info.close()
	bt_info.close()
