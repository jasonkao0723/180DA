import parse

pi = {}
seat = {}
#parse.parse_bluetooth_info("bluetooth-info.txt", pi)

#parse.parse_pi_info("pi-info.txt", pi, seat)

parse.parse_seating("bluetooth-info.txt", "pi-info.txt", seat)

print(seat)
