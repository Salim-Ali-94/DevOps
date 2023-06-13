package main
import "fmt"


func main() {

	value := "111001"
	fmt.Println(binaryToDecimal(value))
	number := 57
	fmt.Println(decimalToBinary(number))
	hex := "57"
	fmt.Println(hexToDecimal(hex))
	hex = "0x57"
	fmt.Println(hexToDecimal(hex))

}