package main


type Todo struct {

	ID string `json:"id,omitempty" bson:"_id,omitempty"`
	Item string `json:"item,omitempty" bson:"item,omitempty"`
	// Completed bool `json:"completed,omitempty" bson:"completed,omitempty"`
	Completed bool `json:"completed" bson:"completed"`

}
