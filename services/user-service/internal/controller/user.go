package controller

import (
	"database/sql"
	"net/http"

	"user-service/internal/model"
	"user-service/internal/repository"

	"github.com/gin-gonic/gin"
)

type UserController struct {
	repo *repository.UserRepository
}

func NewUserController(repo *repository.UserRepository) *UserController {
	return &UserController{repo: repo}
}

// GET /users — admin only
func (uc *UserController) GetAll(c *gin.Context) {
	users, err := uc.repo.FindAll()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Gagal mengambil data users"})
		return
	}
	if users == nil {
		users = []model.User{}
	}
	c.JSON(http.StatusOK, gin.H{"users": users, "total": len(users)})
}

// GET /users/:id
func (uc *UserController) GetByID(c *gin.Context) {
	id := c.Param("id")
	user := c.MustGet("user").(model.Claims)

	// User biasa hanya bisa lihat profil sendiri
	if user.Role != "admin" && user.ID != id {
		c.JSON(http.StatusForbidden, gin.H{"error": "Akses ditolak"})
		return
	}

	u, err := uc.repo.FindByID(id)
	if err == sql.ErrNoRows {
		c.JSON(http.StatusNotFound, gin.H{"error": "User tidak ditemukan"})
		return
	}
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Gagal mengambil data user"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"user": u})
}

// PUT /users/:id
func (uc *UserController) Update(c *gin.Context) {
	id := c.Param("id")
	user := c.MustGet("user").(model.Claims)

	if user.Role != "admin" && user.ID != id {
		c.JSON(http.StatusForbidden, gin.H{"error": "Akses ditolak"})
		return
	}

	var req model.UpdateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	u, err := uc.repo.Update(id, req.Nama)
	if err == sql.ErrNoRows {
		c.JSON(http.StatusNotFound, gin.H{"error": "User tidak ditemukan"})
		return
	}
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Gagal update user"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "User berhasil diupdate", "user": u})
}

// PATCH /users/:id/role — admin only
func (uc *UserController) UpdateRole(c *gin.Context) {
	id := c.Param("id")

	var req model.UpdateRoleRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	u, err := uc.repo.UpdateRole(id, req.Role)
	if err == sql.ErrNoRows {
		c.JSON(http.StatusNotFound, gin.H{"error": "User tidak ditemukan"})
		return
	}
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Gagal update role"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "Role berhasil diupdate", "user": u})
}

// DELETE /users/:id — admin only (soft delete)
func (uc *UserController) Delete(c *gin.Context) {
	id := c.Param("id")

	if err := uc.repo.Delete(id); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Gagal menghapus user"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "User berhasil dinonaktifkan"})
}
