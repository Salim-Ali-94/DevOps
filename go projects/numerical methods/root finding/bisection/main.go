package main
import ( "fmt"
		 "math" )


func main() {

	f := func(x float64) float64 {

		return math.Pow(x, 3) - math.Pow(x, 2) - 2*x + 1
	}

	domain := [2]float64{-10, 10}
	intervals := findInterval(f, domain)
	tolerance := 1e-3
	solutions, epsilon, iterations := bisection(f, intervals, tolerance)
	fmt.Printf("\nFound %v root(s) with a precision of %v in %v iterations inside the window; from x = %v to x = %v for the given function\n", len(solutions), epsilon, iterations, domain[0], domain[1])

	for _, root := range solutions {

		fmt.Printf("\nf(%v) = %v", root, f(root))

	}

}
