package main
import ( "github.com/joho/godotenv"
		 "fmt"
		 "os" )


// var dbHost string = "mongodb://localhost:27017"
// var dbHost string = "mongodb://mongo_db:27017"
var dbHost string

func initializeDotEnv() {

	error := godotenv.Load()

	if error != nil {

		fmt.Println("FAILED TO LOAD .env FILE:", error)

	}

	dbHost = os.Getenv("MONGODB_ENDPOINT")

}
