use actix_web::{get, post, web, App, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
struct MyObject {
    name: String,
    value: i32,
}

#[get("/json")]
async fn get_json() -> impl Responder {
    web::Json(MyObject { name: "Actix".to_string(), value: 123 })
}

#[post("/json")]
async fn post_json(item: web::Json<MyObject>) -> impl Responder {
    web::Json(MyObject { name: format!("Received: {}", item.name), value: item.value * 2 })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(get_json)
            .service(post_json)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
