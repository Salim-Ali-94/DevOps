package main
import ( "net/http"
		 "log"
		 "fmt"
		 "context"
		 "encoding/json"
		 "go.mongodb.org/mongo-driver/mongo/options"
		 "go.mongodb.org/mongo-driver/mongo" )


func main() {

	// checklist := initializeDB()
	// checklist, storeItemClosure := initializeDB()
	storeItemClosure := initializeDB()
	http.HandleFunc("/", entryPoint)
	// http.HandleFunc("/todo-app/store", storeItem)
	http.HandleFunc("/todo-app/store", storeItemClosure)
	log.Fatal(http.ListenAndServe(":8081", nil))

}

// func initializeDB() *mongo.Collection {
func initializeDB() func(http.ResponseWriter, *http.Request) {

	clientOptions := options.Client().ApplyURI(dbHost)
	client, error := mongo.Connect(context.Background(), clientOptions)

	if (error != nil) {

		log.Fatal(error)

	}

	// error := client.Ping(context.Background(), nil)
	error = client.Ping(context.Background(), nil)

	if (error != nil) {

		log.Fatal(error)

	}

	database := client.Database("todo-app")
	collection := database.Collection("checklist")
	// return collection

	// func storeItemClosure(writer http.ResponseWriter, request *http.Request) {
	closure := func(writer http.ResponseWriter, request *http.Request) {

		storeItem(writer, request, collection)

	}

	return closure

}

func entryPoint(writer http.ResponseWriter, request *http.Request) {

	writer.Write([]byte("Todo list API server\n"))

}

// func storeItem(writer http.ResponseWriter, request *http.Request) {
func storeItem(writer http.ResponseWriter, request *http.Request, collection *mongo.Collection) {

	if (request.Method == "POST") {

		var todo Todo
		error := json.NewDecoder(request.Body).Decode(&todo)

		if (error != nil) {

			log.Fatal(error)

		}

		// response, error := collection.InsertOne(context.Background(), todo)
		// _, error := collection.InsertOne(context.Background(), todo)
		// _, error = collection.InsertOne(context.Background(), todo)
		// response, error = collection.InsertOne(context.Background(), todo)
		response, error := collection.InsertOne(context.Background(), todo)

		if (error != nil) {

			log.Fatal(error)

		}

		// writer.Write(response)
		fmt.Fprint(writer, response)
		fmt.Fprint(writer, todo)

	}

}

// func storeItemClosure(writer http.ResponseWriter, request *http.Request) {

// 	storeItem(writer, response, collection)

// }
