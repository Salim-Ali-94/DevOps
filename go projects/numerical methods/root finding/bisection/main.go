package main
import ( "fmt"
		 "math" )


func main() {

	f := func(x float64) float64 {

		return math.Pow(x, 3) - math.Pow(x, 2) - 2*x + 1
	}

	d := [2]float64{-2, 2}
	brackets := findInterval(f, d)
	fmt.Println(brackets)
}
