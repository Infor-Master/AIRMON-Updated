package main

import (
	"airmon/model"
	"airmon/routes"
	"airmon/services"

	"github.com/gin-gonic/gin"
)

func init() {
	services.OpenDatabase()
	services.Db.AutoMigrate(&model.Device{})
	services.Db.AutoMigrate(&model.Data{})
}

func main() {

	router := gin.New()
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	router.NoRoute(func(c *gin.Context) {
		c.JSON(404, gin.H{"code": "PAGE_NOT_FOUND", "message": "Page not found"})
	})

	device := router.Group("/api/device")
	{
		device.POST("/", routes.AddDevice)
		device.PUT("/", routes.UpdateDevice)
		device.DELETE("/", routes.DeleteDevice)
		device.GET("/", routes.GetDevices)
		device.GET("/:id", routes.GetDevice)
	}

	data := router.Group("/api/data")
	{
		data.POST("/", routes.AddData)
		data.GET("/:id", routes.GetData)
	}

	router.Run(":8081")
}
