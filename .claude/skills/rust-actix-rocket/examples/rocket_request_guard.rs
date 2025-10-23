#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;

use rocket::request::{Outcome, Request, FromRequest};
use rocket::http::Status;

// A simple API key request guard
pub struct ApiKey(String);

#[rocket::async_trait]
impl<'r> FromRequest<'r> for ApiKey {
    type Error = ApiKeyError;

    async fn from_request(request: &'r Request<'_>) -> Outcome<Self, Self::Error> {
        match request.headers().get_one("x-api-key") {
            Some(key) if key == "valid-api-key" => Outcome::Success(ApiKey(key.to_string())),
            _ => Outcome::Failure((Status::Unauthorized, ApiKeyError::Missing)),
        }
    }
}

pub enum ApiKeyError {
    Missing,
}

#[get("/protected")]
fn protected_route(api_key: ApiKey) -> String {
    format!("Access granted with API Key: {}", api_key.0)
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![protected_route])
}
