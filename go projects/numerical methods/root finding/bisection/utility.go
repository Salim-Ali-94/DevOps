package main
import "math"


func findInterval(function func(float64) float64, window [2]float64) []map[string]float64 {

	var interval []map[string]float64
	initial := window[0]
	length := math.Abs(window[1] - initial)
	step := 1.0
	delta := float64(length) / step
	x := initial

	for (delta > 1) {

		step += 1
		delta = float64(length) / float64(step)

	}

	for (x < window[1]) {

		x += delta

		if (function(initial)*function(x) < 0) {

			interval = append(interval, map[string]float64{ "lower": initial,
															"upper": x })

		}

		initial = x

	}

	return interval

}

func bisection(function func(float64) float64, window [2]float64, precision float64) ([]float64, float64, int) {

	var roots []float64
	var left float64
	var right float64
	var center float64
	var residual float64
	var previous float64
	iteration := 0
	interval := findInterval(function, window)

	for _, bracket := range interval {

		left = bracket["lower"]
		right = bracket["upper"]
		center = (left + right) / 2
		residual = math.Abs(2.0*precision)
		previous = center

		for (residual > precision) {

			if ((function(left)*function(center) == 0) ||
				(function(right)*function(center) == 0)) {

				roots = append(roots, center)
				iteration += 1
				break

			} else if (function(left)*function(center) < 0) {

				right = center

			} else {

				left = center

			}

			center = (left + right) / 2
			residual = math.Abs((center - previous) / center)
			previous = center
			iteration += 1

			if (residual < precision) {

				roots = append(roots, center)

			}

		}

	}

	return roots, residual, iteration

}
