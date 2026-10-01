from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "EcoLogística API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ecologistica"

    co2_factor: float = 0.254

    allowed_districts: list[str] = ["EL TAMBO", "HUANCAYO", "CHILCA"]

    geo_lat_min: float = -12.2000
    geo_lat_max: float = -11.9000
    geo_lng_min: float = -75.4000
    geo_lng_max: float = -75.1000

    cors_origins: list[str] = ["http://localhost:5173"]

    @property
    def allowed_district_set(self) -> set[str]:
        return {d.strip().upper() for d in self.allowed_districts}

    def normalize_district(self, distrito: str) -> str:
        return distrito.strip().upper()

    def is_district_allowed(self, distrito: str) -> bool:
        return self.normalize_district(distrito) in self.allowed_district_set

    def is_in_scope(self, latitud: float, longitud: float) -> bool:
        return (
            self.geo_lat_min <= latitud <= self.geo_lat_max
            and self.geo_lng_min <= longitud <= self.geo_lng_max
        )


settings = Settings()
