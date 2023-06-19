package main


func findInterval(function func(float64) float64, window [2]float64) []map[string]float64 {

	initial := window[0]
	length := window[1] - initial
	step := 0.0
	delta := float64(length) / step
	interval := []map[string]float64{}
	x := initial
	check := 0.0

	for delta > 1 {

		step += 1
		delta = float64(length) / float64(step)

	}

	for (x < window[1]) {

		x += delta
		check = function(initial)*function(x)

		if (check < 0) {

			interval = append(interval, map[string]float64{ "lower": initial,
															"upper": x })
			initial = x

		}

	}

	return interval

}
