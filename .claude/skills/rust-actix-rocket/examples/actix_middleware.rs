use actix_web::{web, App, HttpServer, Responder};
use actix_web::middleware::Logger;
use actix_web::dev::{ServiceRequest, ServiceResponse};
use futures::future::Ready;
use actix_web::{Error, HttpResponse};

// Simple middleware that logs the request path
pub struct MyMiddleware;

impl<S, B>
    actix_web::dev::Transform<S, ServiceRequest>
    for MyMiddleware
where
    S: actix_web::dev::Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error>,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = MyMiddlewareService<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        futures::future::ok(MyMiddlewareService { service })
    }
}

pub struct MyMiddlewareService<S> {
    service: S,
}

impl<S, B>
    actix_web::dev::Service<ServiceRequest>
    for MyMiddlewareService<S>
where
    S: actix_web::dev::Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error>,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = S::Future;

    actix_web::dev::forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        println!("Hi from start. Request path: {}", req.path());
        self.service.call(req)
    }
}

#[get("/")]
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello from Actix Web with Middleware!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "actix_web=info");
    env_logger::init();

    HttpServer::new(|| {
        App::new()
            .wrap(Logger::default())
            .wrap(MyMiddleware)
            .service(index)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
