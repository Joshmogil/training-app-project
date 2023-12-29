package modules_test

import (
    "testing"
	"fitness/pkg/workout"    
	"github.com/Joshmogil/training-app-project/tree/main/fitness"
)


func TestUser_Save(t *testing.T) {
    u := &Exercise{Name: "Susy Queue"}
    ok(t, u.Save())
}