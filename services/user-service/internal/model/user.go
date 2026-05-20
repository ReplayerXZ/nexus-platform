package model

import "time"

type User struct {
	ID        string    `json:"id"`
	Nama      string    `json:"nama"`
	Email     string    `json:"email"`
	Role      string    `json:"role"`
	IsActive  bool      `json:"is_active"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type UpdateUserRequest struct {
	Nama string `json:"nama" binding:"required,min=2"`
}

type UpdateRoleRequest struct {
	Role string `json:"role" binding:"required,oneof=user admin"`
}

type Claims struct {
	ID    string `json:"id"`
	Email string `json:"email"`
	Role  string `json:"role"`
}
