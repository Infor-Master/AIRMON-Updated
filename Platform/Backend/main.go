package main

import (
	"airmon/model"
	"airmon/services"
	"log"
)

func init() {
	services.OpenDatabase()
	services.Db.AutoMigrate(&model.Device{})
	services.Db.AutoMigrate(&model.Data{})
}

func main() {
	log.Printf("ola")
}
