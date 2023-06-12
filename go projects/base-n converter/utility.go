package main
import ( "fmt"
		 "math"
		 "strconv" )


func convertToDecimal(number string) string {

	flag := binaryTest(number)

	if flag {

		accumulate := 0.0

		for index, binary := range number {

			digit := string(binary)
			bit, _ := strconv.ParseFloat(digit, 64)
			exponent := float64(len(number) - index)
			accumulate += bit*math.Pow(2, exponent - 1)

		}

		decimal := strconv.FormatFloat(accumulate, 'f', -1, 64)
		return decimal

	}

	return fmt.Sprintf("%q is not a binary number", number)

}

func binaryTest(number string) bool {

	for _, value := range number {

		if ((string(value) != "0") && (string(value) != "1")) {

			return false

		}

	}

	return true

}