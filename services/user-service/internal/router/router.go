package router

import (
	"os"

	"user-service/internal/controller"
	"user-service/internal/middleware"

	"github.com/gin-gonic/gin"
)

func Setup(userCtrl *controller.UserController) *gin.Engine {
	if os.Getenv("NODE_ENV") == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	r := gin.Default()

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status":    "ok",
			"service":   "user-service",
			"timestamp": gin.H{},
		})
	})

	users := r.Group("/users", middleware.Authenticate())
	{
		users.GET("", middleware.AdminOnly(), userCtrl.GetAll)
		users.GET("/:id", userCtrl.GetByID)
		users.PUT("/:id", userCtrl.Update)
		users.PATCH("/:id/role", middleware.AdminOnly(), userCtrl.UpdateRole)
		users.DELETE("/:id", middleware.AdminOnly(), userCtrl.Delete)
	}

	return r
}
