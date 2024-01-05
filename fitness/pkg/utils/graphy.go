package utils

type Graphable interface {
	GetNodeType() string
	GetCypherFormatString() string
	GetStructValuesAsKeyValue() map[string]any
}