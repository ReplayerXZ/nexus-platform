.PHONY: help up down build logs ps clean restart

help: ## Tampilkan semua perintah
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Jalankan semua service
	docker compose up -d

up-build: ## Build ulang dan jalankan semua service
	docker compose up -d --build

down: ## Stop semua service
	docker compose down

down-clean: ## Stop semua service dan hapus volume
	docker compose down -v

build: ## Build semua image
	docker compose build

logs: ## Lihat logs semua service
	docker compose logs -f

logs-auth: ## Lihat logs auth service
	docker compose logs -f auth-service

logs-user: ## Lihat logs user service
	docker compose logs -f user-service

logs-notif: ## Lihat logs notification service
	docker compose logs -f notification-service

ps: ## Lihat status semua service
	docker compose ps

restart: ## Restart semua service
	docker compose restart

clean: ## Hapus semua container, image, volume yang tidak dipakai
	docker system prune -af --volumes