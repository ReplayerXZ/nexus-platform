package repository

import (
	"database/sql"
	"user-service/internal/model"
)

type UserRepository struct {
	db *sql.DB
}

func NewUserRepository(db *sql.DB) *UserRepository {
	return &UserRepository{db: db}
}

func (r *UserRepository) FindAll() ([]model.User, error) {
	rows, err := r.db.Query(`
		SELECT id, nama, email, role, is_active, created_at, updated_at
		FROM users ORDER BY created_at DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var users []model.User
	for rows.Next() {
		var u model.User
		if err := rows.Scan(&u.ID, &u.Nama, &u.Email, &u.Role,
			&u.IsActive, &u.CreatedAt, &u.UpdatedAt); err != nil {
			return nil, err
		}
		users = append(users, u)
	}
	return users, nil
}

func (r *UserRepository) FindByID(id string) (*model.User, error) {
	var u model.User
	err := r.db.QueryRow(`
		SELECT id, nama, email, role, is_active, created_at, updated_at
		FROM users WHERE id = $1
	`, id).Scan(&u.ID, &u.Nama, &u.Email, &u.Role,
		&u.IsActive, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, err
	}
	return &u, nil
}

func (r *UserRepository) Update(id string, nama string) (*model.User, error) {
	var u model.User
	err := r.db.QueryRow(`
		UPDATE users SET nama = $1, updated_at = NOW()
		WHERE id = $2
		RETURNING id, nama, email, role, is_active, created_at, updated_at
	`, nama, id).Scan(&u.ID, &u.Nama, &u.Email, &u.Role,
		&u.IsActive, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, err
	}
	return &u, nil
}

func (r *UserRepository) UpdateRole(id string, role string) (*model.User, error) {
	var u model.User
	err := r.db.QueryRow(`
		UPDATE users SET role = $1, updated_at = NOW()
		WHERE id = $2
		RETURNING id, nama, email, role, is_active, created_at, updated_at
	`, role, id).Scan(&u.ID, &u.Nama, &u.Email, &u.Role,
		&u.IsActive, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, err
	}
	return &u, nil
}

func (r *UserRepository) Delete(id string) error {
	_, err := r.db.Exec(`
		UPDATE users SET is_active = false, updated_at = NOW()
		WHERE id = $1
	`, id)
	return err
}
