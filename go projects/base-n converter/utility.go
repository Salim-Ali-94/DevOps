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

func convertToBinary(number int) string {

	decimal := float64(number)
	length := math.Log2(decimal)
	width := math.Ceil(length)
	remainder := number
	binary := ""

	for index := width; index > 0; index-- {

		exponent := float64(index)
		position := math.Pow(2, exponent - 1)
		check := int(position)

		if (remainder >= check) {

			remainder -= check
			binary += "1"

		} else {

			binary += "0"

		}

	}

	return binary

}

func binaryTest(number string) bool {

	for _, value := range number {

		if ((string(value) != "0") && (string(value) != "1")) {

			return false

		}

	}

	return true

}