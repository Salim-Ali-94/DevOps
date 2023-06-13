package main
import "fmt"


func main() {

	binary := "111001"
	fmt.Println(binaryToDecimal(binary))
	number := 57
	fmt.Println(decimalToBinary(number))
	hex := "0x57"
	fmt.Println(hexToDecimal(hex))
	value := 387
	fmt.Println(decimalToHex(value))

}