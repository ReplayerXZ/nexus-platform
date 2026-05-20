package main

import (
	"log"
	"os"

	"user-service/internal/config"
	"user-service/internal/controller"
	"user-service/internal/repository"
	"user-service/internal/router"
)

func main() {
	config.ConnectDB()

	userRepo := repository.NewUserRepository(config.DB)
	userCtrl := controller.NewUserController(userRepo)

	r := router.Setup(userCtrl)

	port := os.Getenv("USER_PORT")
	if port == "" {
		port = "8001"
	}

	log.Printf("🚀 User service berjalan di port %s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatalf("❌ Gagal menjalankan server: %v", err)
	}
}
