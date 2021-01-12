package model

import (
	"gorm.io/gorm"
)

type Data struct {
	gorm.Model
	DeviceID uint    `gorm:"not null"`
	CO2_PPM  float32 `gorm:"not null"`
	NO2_PPM  float32 `gorm:"not null"`
	CH2O_PPM float32 `gorm:"not null"`
	Temp_C   float32 `gorm:"not null"`
	Hum_100  float32 `gorm:"not null"`
}
