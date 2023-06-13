package main
import "fmt"


func main() {

	binary := "111001"
	fmt.Println(binaryToDecimal(binary))
	decimal := 101
	fmt.Println(decimalToBinary(decimal))
	hex := "0x109D"
	fmt.Println(hexToDecimal(hex))
	number := 387
	fmt.Println(decimalToHex(number))
	bits := "0110111"
	fmt.Println(binaryToHex(bits))
	digit := "0xE31A7"
	fmt.Println(hexToBinary(digit))

	mock := "0x1101"
	fmt.Println(binaryToHex(mock))
	test := "0xE31A7h"
	fmt.Println(hexToBinary(test))

}
