package main
import ( "fmt"
		 "math"
		 "strings"
		 "strconv" )


func binaryToDecimal(number string) int {

	flag := binaryTest(number)

	if flag {

		accumulator := 0.0

		for index, binary := range number {

			digit := string(binary)
			bit, _ := strconv.ParseFloat(digit, 64)
			exponent := float64(len(number) - index)
			accumulator += bit*math.Pow(2, exponent - 1)

		}

		decimal := int(accumulator)
		return decimal

	}

	return -1

}

func decimalToBinary(number int) string {

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

func hexToDecimal(number string) int {

	if ((number[:2] == "0x") ||
		(number[:2] == "0X")) {

		flag := hexTest(number[2:])

		if flag {

			accumulator := 0.0

			for index, digit := range number[2:] {

				key := string(digit)
				value := format[key]
				hex, _ := strconv.ParseFloat(value, 64)
				exponent := float64(len(number[2:]) - index)
				accumulator += hex*math.Pow(16, exponent - 1)

			}

			decimal := int(accumulator)
			return decimal

		}

		return -1

	}

	return -1

}

func decimalToHex(number int) string {

	result := number / 16
	remainder := number % 16
	key := strconv.FormatInt(int64(remainder), 10)
	hex := format[key]

	for result >= 1 {

		remainder = result % 16
		result /= 16
		key = strconv.FormatInt(int64(remainder), 10)
		hex = fmt.Sprintf("%v%v", format[key], hex)

	}

	hex = fmt.Sprintf("0x%v", hex)
	return hex

}

func hexToBinary(number string) string {

	decimal := hexToDecimal(number)

	if (decimal == -1) {

		return fmt.Sprintf("%q is not a hex value", number)

	}

	binary := decimalToBinary(decimal)
	return binary

}

func binaryToHex(number string) string {

	decimal := binaryToDecimal(number)

	if (decimal == -1) {

		return fmt.Sprintf("%q is not a binary number", number)

	}

	hex := decimalToHex(decimal)
	return hex

}


func binaryTest(number string) bool {

	for _, value := range number {

		if ((string(value) != "0") &&
			(string(value) != "1")) {

			return false

		}

	}

	return true

}

func hexTest(number string) bool {

	valid := true

	for _, value := range strings.ToLower(number) {

		valid = false
		allowed := array()

		for _, key := range allowed {


			if (string(value) == string(key)) {

				valid = true
				break
			
			}

		}

		if !valid {

			return valid

		}

	}

	return valid

}

func array() []string {

	keys := make([]string, 0, 16)

	for index := 0; index < 16; index++ {

		value := strconv.FormatInt(int64(index), 10)
		keys = append(keys, format[value])

	}

	return keys

}
