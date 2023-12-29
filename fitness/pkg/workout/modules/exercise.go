package workout

import (
	"context"
	"fmt"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

type Exercise struct{
	Id int64
	Name string
}



func (e *Exercise) String() string {
    return fmt.Sprintf("Exercise (id: %d, name: %q)", e.Id, e.Name)
}

func insertExercise(ctx context.Context, driver neo4j.DriverWithContext) (*Exercise, error) {
    result, err := neo4j.ExecuteQuery(ctx, driver,
        "CREATE (n:Exercise { id: $id, name: $name }) RETURN n",
        map[string]any{
            "id":   1,
            "name": "Item 1",
        }, neo4j.EagerResultTransformer)
    if err != nil {
        return nil, err
    }
    itemNode, _, err := neo4j.GetRecordValue[neo4j.Node](result.Records[0], "n")
    if err != nil {
        return nil, fmt.Errorf("could not find node n")
    }
    id, err := neo4j.GetProperty[int64](itemNode, "id")
    if err != nil {
        return nil, err
    }
    name, err := neo4j.GetProperty[string](itemNode, "name")
    if err != nil {
        return nil, err
    }
    return &Exercise{Id: id, Name: name}, nil
}
