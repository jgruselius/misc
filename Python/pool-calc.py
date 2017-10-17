# Define a test data set:
samples = [
	{ "conc": 10, "vol": 30.9 },
	{ "conc": 10, "vol": 40.4 },
	{ "conc": 10, "vol": 46.3 },
	{ "conc": 10, "vol": 33.7 },
	{ "conc": 10, "vol": 20.6 },
	{ "conc": 10, "vol": 46.9 },
	{ "conc": 10, "vol": 24 },
	{ "conc": 10, "vol": 34.7 },
	{ "conc": 10, "vol": 18.3 },
	{ "conc": 10, "vol": 19.9 },
	{ "conc": 10, "vol": 35.4 },
	{ "conc": 10, "vol": 44 },
	{ "conc": 10, "vol": 28.9 },
	{ "conc": 10, "vol": 36.7 },
	{ "conc": 10, "vol": 25.1 },
	{ "conc": 10, "vol": 30.4 },
	{ "conc": 10, "vol": 21.1 },
	{ "conc": 10, "vol": 38.2 },
	{ "conc": 10, "vol": 39 },
	{ "conc": 10, "vol": 38.8 },
	{ "conc": 10, "vol": 49.5 },
	{ "conc": 10, "vol": 25.6 },
	{ "conc": 10, "vol": 29.3 },
	{ "conc": 10, "vol": 11.8 },
	{ "conc": 10, "vol": 13.2 },
	{ "conc": 10, "vol": 31.6 },
	{ "conc": 10, "vol": 33.7 },
	{ "conc": 10, "vol": 27.7 },
	{ "conc": 10, "vol": 28.8 },
	{ "conc": 10, "vol": 16.6 },
	{ "conc": 10, "vol": 45.8 },
	{ "conc": 10, "vol": 43.4 },
	{ "conc": 10, "vol": 15.5 },
	{ "conc": 10, "vol": 35.8 },
	{ "conc": 10, "vol": 39.8 },
	{ "conc": 10, "vol": 18.4 },
	{ "conc": 10, "vol": 23.1 },
	{ "conc": 10, "vol": 20.1 },
	{ "conc": 10, "vol": 26.5 },
	{ "conc": 10, "vol": 10.4 },
	{ "conc": 10, "vol": 40.1 },
	{ "conc": 10, "vol": 48 },
	{ "conc": 10, "vol": 29.1 },
	{ "conc": 10, "vol": 12.4 },
	{ "conc": 10, "vol": 15.5 },
	{ "conc": 10, "vol": 24.3 },
	{ "conc": 10, "vol": 36.9 },
	{ "conc": 10, "vol": 74.6 },
	{ "conc": 10, "vol": 22.4 },
	{ "conc": 10, "vol": 11.3 },
	{ "conc": 10, "vol": 17.6 },
	{ "conc": 10, "vol": 29.8 },
	{ "conc": 10, "vol": 21.5 },
	{ "conc": 10, "vol": 57.6 },
	{ "conc": 10, "vol": 16.2 },
	{ "conc": 10, "vol": 21.2 },
	{ "conc": 10, "vol": 14 },
	{ "conc": 10, "vol": 31.7 },
	{ "conc": 10, "vol": 24.3 },
	{ "conc": 10, "vol": 24.5 },
	{ "conc": 10, "vol": 26.4 },
	{ "conc": 10, "vol": 14.7 },
	{ "conc": 10, "vol": 43.1 },
	{ "conc": 10, "vol": 29.7 },
	{ "conc": 10, "vol": 24.8 },
	{ "conc": 10, "vol": 38 },
	{ "conc": 10, "vol": 21 },
	{ "conc": 10, "vol": 31.8 },
	{ "conc": 10, "vol": 61.5 }
]
# Another test data set:
samples = [
	{ "conc": 10, "vol": 32 },
	{ "conc": 10, "vol": 40.4 },
	{ "conc": 4, "vol": 46.3 },
	{ "conc": 10, "vol": 33.7 },
	{ "conc": 10, "vol": 20.6 },
	{ "conc": 4, "vol": 46.9 },
	{ "conc": 4, "vol": 24 },
	{ "conc": 10, "vol": 34.7 },
	{ "conc": 10, "vol": 18.3 },
	{ "conc": 10, "vol": 19.9 },
	{ "conc": 10, "vol": 35.4 },
	{ "conc": 6, "vol": 44 },
	{ "conc": 10, "vol": 28.9 },
	{ "conc": 6, "vol": 36.7 },
	{ "conc": 6, "vol": 25.1 },
	{ "conc": 10, "vol": 30.4 },
	{ "conc": 10, "vol": 21.1 },
	{ "conc": 10, "vol": 38.2 },
	{ "conc": 6, "vol": 39 },
	{ "conc": 10, "vol": 38.8 },
	{ "conc": 4, "vol": 49.5 },
	{ "conc": 10, "vol": 25.6 },
	{ "conc": 4, "vol": 29.3 },
	{ "conc": 10, "vol": 11.8 },
	{ "conc": 4, "vol": 13.2 },
	{ "conc": 4, "vol": 31.6 },
	{ "conc": 4, "vol": 33.7 },
	{ "conc": 4, "vol": 27.7 },
	{ "conc": 10, "vol": 28.8 },
	{ "conc": 10, "vol": 16.6 },
	{ "conc": 4, "vol": 45.8 },
	{ "conc": 10, "vol": 43.4 },
	{ "conc": 10, "vol": 15.5 },
	{ "conc": 4, "vol": 35.8 },
	{ "conc": 10, "vol": 39.8 },
	{ "conc": 8, "vol": 18.4 },
	{ "conc": 8, "vol": 23.1 },
	{ "conc": 10, "vol": 20.1 },
	{ "conc": 4, "vol": 26.5 },
	{ "conc": 10, "vol": 10.4 },
	{ "conc": 8, "vol": 40.1 },
	{ "conc": 8, "vol": 48 },
	{ "conc": 6, "vol": 29.1 },
	{ "conc": 10, "vol": 12.4 },
	{ "conc": 6, "vol": 15.5 },
	{ "conc": 4, "vol": 24.3 },
	{ "conc": 4, "vol": 36.9 },
	{ "conc": 4, "vol": 74.6 },
	{ "conc": 10, "vol": 22.4 },
	{ "conc": 10, "vol": 11.3 },
	{ "conc": 4, "vol": 17.6 },
	{ "conc": 4, "vol": 29.8 },
	{ "conc": 4, "vol": 21.5 },
	{ "conc": 4, "vol": 57.6 },
	{ "conc": 10, "vol": 16.2 },
	{ "conc": 10, "vol": 21.2 },
	{ "conc": 4, "vol": 14 },
	{ "conc": 6, "vol": 31.7 },
	{ "conc": 10, "vol": 24.3 },
	{ "conc": 10, "vol": 24.5 },
	{ "conc": 6, "vol": 26.4 },
	{ "conc": 10, "vol": 14.7 },
	{ "conc": 10, "vol": 43.1 },
	{ "conc": 8, "vol": 29.7 },
	{ "conc": 8, "vol": 24.8 },
	{ "conc": 4, "vol": 38 },
	{ "conc": 6, "vol": 21 },
	{ "conc": 6, "vol": 31.8 },
	{ "conc": 6, "vol": 61.5 }
]

#samples = samples[:10]

######### LAZY WAY ###############################
# Just divide the total with the number of samples, it is implied that the final
# conc and the conc of every input is the same:
def lazy(samples, final_vol):
	# Return list rather than generator since size of samples will not be so large:
	return [final_vol / len(samples) for s in samples]
	# return [(final_vol / len(samples) * final_conc / s["conc"]) for s in samples]

######### OTHER WAY ##############################
# Iteratively reduce the smallest input volume until we are close to the desired
# total volume. This works when the inputs have different concentrations, the
# final pool concentration will then end up somewhere between the conc of the
# highest and the lowest input concentration:
def complex(samples, final_vol, limit_vol=2):
	# Create a list we can sort to get the minimas:
	l = [(s["conc"]*s["vol"],s["conc"],s["vol"]) for s in samples]
	# Find the minimas by sorting this list on the different values:
	min_conc = sorted(l, key=lambda x: x[1])[0][1]
	max_conc = sorted(l, key=lambda x: x[1])[-1][1]
	min_vol = sorted(l, key=lambda x: x[2])[0][2]
	# The volume of the input with lowest amount:
	min_amount = sorted(l)[0][2]

	def minimize_vol(vol, final_vol=final_vol, limit_vol=limit_vol, reduce=0.9):
		# Keep track of the number of iterations (you may want to break at some point):
		global counter
		counter += 1
		try_vol = reduce * vol
		# The lowest volume to take would then be (sample(s) w highest conc):
		low_vol = min(try_vol * max_conc / s["conc"] for s in samples)
		# Total pool volume if we were to take this amount of all samples:
		tot_vol = sum(try_vol * max_conc / s["conc"] for s in samples)
		# We don't want to pipette less than limit_vol
		# while keeping total volume above final_vol:
		if low_vol >= limit_vol and tot_vol >= final_vol and try_vol >= limit_vol:
			return minimize_vol(try_vol)
		else:
			# We can't improve anymore within the given limits... 
			return vol

	# Start from whichever is the smallest volume:
	use_vol = minimize_vol(min(min_amount, min_vol))
	# Calculate the volume to take of each input:
	# Return list rather than generator since size of samples will not be so large:
	return [(use_vol * max_conc / s["conc"]) for s in samples]

def main():
	# Desired volume and final conc of pool:
	final_vol = 100
	# We don't want to pipette less than:
	limit_vol = 2 
	# ... or print("not all samples have a conc above {}".format(final_conc))
	# Check that all samples have the amount req:
	# all(final_vol * final_conc / len(samples) < s["conc"] * s["vol"] for s in samples)
	# ... or print("not all samples have the req amount")
	global counter
	counter = 0
	# Only use complex calculation when sample concentrations are different:
	if len(set(s["conc"] for s in samples)) < 2:
		print("\n####### Simple way:")
		vols = lazy(samples, final_vol)
	else:
		print("\n####### Complex way:")
		vols = complex(samples, final_vol)
		print("Iterations to arrive at solution: {}".format(counter))

	print([round(v,4) for v in vols])


	print("\nTotal pool volume: {}".format(round(sum(vols),4)))
	z = zip([s["conc"] for s in samples], vols)
	v = (sum(x[0]*x[1] for x in z) / sum(vols))
	print("Theoretical final conc: {}".format(round(v,4)))

if __name__ == "__main__":
	main()

