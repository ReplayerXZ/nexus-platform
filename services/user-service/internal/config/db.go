package config

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/lib/pq"
)

var DB *sql.DB

func ConnectDB() {
	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		os.Getenv("POSTGRES_HOST"),
		os.Getenv("POSTGRES_PORT"),
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("POSTGRES_DB"),
	)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatalf("❌ Gagal koneksi ke PostgreSQL: %v", err)
	}

	if err := db.Ping(); err != nil {
		log.Fatalf("❌ PostgreSQL tidak merespon: %v", err)
	}

	DB = db
	log.Println("✅ PostgreSQL connected")
}