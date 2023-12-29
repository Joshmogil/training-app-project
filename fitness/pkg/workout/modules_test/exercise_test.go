package modules_test

import (
    "testing"
	"fitness/pkg/workout/modules"
)


func TestExercise_Insert(t *testing.T) {
    u := &modules.Exercise{Name: "Susy Queue"}
    ok(t, u.Save())
}