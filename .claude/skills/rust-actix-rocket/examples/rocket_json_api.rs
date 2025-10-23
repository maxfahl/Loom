#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;
#[macro_use] extern crate serde;

use rocket::serde::json::Json;

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(crate = "rocket::serde")]
struct MyObject {
    name: String,
    value: i32,
}

#[get("/json")]
fn get_json() -> Json<MyObject> {
    Json(MyObject { name: "Rocket".to_string(), value: 456 })
}

#[post("/json", data = "<item>")]
fn post_json(item: Json<MyObject>) -> Json<MyObject> {
    Json(MyObject { name: format!("Received: {}", item.name), value: item.value * 2 })
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![get_json, post_json])
}
