import argparse
import csv
import math

def linear_least_squares(x_values, y_values):
	m = len(y_values)
	n = len(x_values)
	# Demand x_values[] and y_values[] of equal size:
	if m != n:
		raise ValueError("Lists of different length")
	# Calculate a linear least squares regression function on the form y = a + bx:
	sum_x = 0
	sum_y = 0
	sum_xy = 0
	sum_x2 = 0
	sum_y2 = 0
	for i in xrange(n):
		x = x_values[i]
		y = y_values[i]
		# Test x & y
		sum_x += x
		sum_y += y
		sum_xy += x * y
		sum_x2 += x * x
		sum_y2 += y * y
	a = (sum_y * sum_x2 - sum_x * sum_xy) / (n * sum_x2 - sum_x * sum_x)
	b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
	r2 = math.pow((n * sum_xy - sum_x * sum_y) / math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)), 2)
	return [a, b, r2]

def main(args):
	print linear_least_squares([1,2,3,4,5],[1.02,1.99,3.03,3.987,5.08])

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="...")
	p.add_argument("file", metavar="<file>", help="Result file to parse")
	args = p.parse_args()
	main(args)