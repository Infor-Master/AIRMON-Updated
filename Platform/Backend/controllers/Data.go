package controllers

import (
	"airmon/model"
	"airmon/services"
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func AddData(c *gin.Context) {
	var data model.Data

	if err := c.ShouldBindJSON(&data); err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid structure"})
		return
	}

	services.Db.Create(&data)
	c.JSON(http.StatusCreated, gin.H{"status": http.StatusCreated, "message": "data created sucessfully"})
}

func GetData(c *gin.Context) {
	var data []model.Data

	id := c.Param("id")
	limit, err := strconv.Atoi(c.Param("limit"))

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid request"})
		return
	}

	offset, err := strconv.Atoi(c.Param("offset"))

	if err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"status": http.StatusBadRequest, "message": "Invalid request"})
		return
	}

	services.Db.Where("device_id = ?", id).Limit(limit).Offset(offset).Find(&data)

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": data})
}
