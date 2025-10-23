---
name: ruby-on-rails-development
version: 0.1.0
category: Web Development / Backend
tags: Ruby, Rails, Web, Backend, MVC, Hotwire, Database, API
description: Guides Claude in developing robust, scalable, and secure Ruby on Rails applications following modern best practices.
---

# Ruby on Rails Development Skill

## 1. Skill Purpose

This skill enables Claude to assist in the development of Ruby on Rails applications, focusing on modern best practices, performance optimization, security, and maintainability. Claude can help with architectural decisions, code implementation, refactoring, testing strategies, and identifying common pitfalls.

## 2. When to Activate This Skill

Activate this skill when the task involves:
- Building new features in a Rails application.
- Refactoring existing Rails code.
- Optimizing performance (e.g., N+1 queries, caching).
- Implementing or reviewing security measures in Rails.
- Setting up testing for Rails components (models, controllers, views).
- Integrating frontend with Hotwire (Turbo, Stimulus).
- Troubleshooting Rails-specific issues.
- Generating boilerplate code for Rails components.

## 3. Core Knowledge

Claude should be proficient in:

- **Rails MVC Architecture**: Models (Active Record), Views (ERB, Haml, Slim, ViewComponents), Controllers (Action Controller), Routes (Action Dispatch).
- **Hotwire Stack**: Turbo (Drive, Frames, Streams), Stimulus.
- **Database Interactions**: Active Record queries, migrations, associations, indexes.
- **Testing Frameworks**: RSpec, Minitest, FactoryBot.
- **Background Jobs**: Active Job, Sidekiq, Solid Queue.
- **Caching**: Fragment, low-level, Russian Doll caching.
- **Security**: CSRF, XSS, SQL injection prevention, encrypted credentials.
- **Performance**: N+1 query prevention, eager loading, asset optimization.
- **Code Quality**: Service Objects, Form Objects, Decorators/Presenters, POROs, RuboCop.
- **API Development**: RESTful principles, JSON API.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Embrace Hotwire**: For rich, interactive UIs with minimal JavaScript, leverage Turbo and Stimulus. Prioritize server-rendered HTML over heavy client-side frameworks where appropriate.
- ✅ **Service Objects for Business Logic**: Encapsulate complex business logic in Service Objects (POROs) to keep models and controllers focused.
- ✅ **Form Objects for Complex Forms**: Use Form Objects to handle intricate form submissions, validations, and data persistence across multiple models.
- ✅ **ViewComponents for Reusable UI**: Create reusable, testable UI components using ViewComponents.
- ✅ **Prevent N+1 Queries**: Always use eager loading (`includes`, `preload`, `eager_load`) when querying associations to avoid N+1 query issues.
- ✅ **Implement Caching Strategically**: Utilize fragment, low-level, and Russian Doll caching to improve application performance.
- ✅ **Offload Long-Running Tasks**: Use Active Job with a suitable adapter (e.g., Sidekiq, Solid Queue) for background processing of emails, image processing, etc.
- ✅ **Write Comprehensive Tests**: Maintain high test coverage using RSpec/Minitest for unit, integration, and feature tests. Use FactoryBot for test data.
- ✅ **Leverage Rails Security Features**: Ensure CSRF protection is enabled, use strong authentication/authorization, and store secrets in encrypted credentials.
- ✅ **Follow Rails Conventions**: Adhere to "convention over configuration" to promote consistency and reduce boilerplate.
- ✅ **Use RuboCop**: Enforce code style and best practices with RuboCop.
- ✅ **Optimize Database Queries**: Add appropriate database indexes and review ActiveRecord usage for efficiency.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Fat Controllers**: Avoid placing extensive business logic directly in controllers. Delegate to Service Objects, Form Objects, or models.
- ❌ **N+1 Queries**: Never fetch associated records in a loop without eager loading. This leads to severe performance degradation.
- ❌ **Storing Secrets in Code**: Do not hardcode API keys, database credentials, or other sensitive information directly in the codebase. Use Rails encrypted credentials or environment variables.
- ❌ **Ignoring Security Updates**: Do not neglect to update Rails, Ruby, and gems. Security vulnerabilities are frequently patched.
- ❌ **Skipping Tests**: Avoid writing features without corresponding tests. This leads to brittle code and regressions.
- ❌ **Direct SQL in Controllers/Views**: Avoid embedding raw SQL queries directly in controllers or views; use ActiveRecord's query interface.
- ❌ **Excessive Gem Usage**: Only include gems that are truly necessary and well-maintained. Evaluate their impact on performance and security.

### Common Questions & Responses

- **Q: How do I handle complex business logic in Rails?**
  - A: Encapsulate it within Service Objects (POROs). These are plain Ruby classes that take inputs, perform an action, and return a result, keeping your models and controllers clean.

- **Q: My page is loading slowly, what should I check first?**
  - A: Check for N+1 queries using tools like Bullet or Rack Mini Profiler. Implement eager loading (`includes`, `preload`) for associations. Also, consider adding database indexes and caching.

- **Q: What's the best way to build interactive features without heavy JavaScript frameworks?**
  - A: Use Hotwire (Turbo and Stimulus). Turbo handles fast page navigation and partial page updates, while Stimulus adds light JavaScript behavior to HTML.

- **Q: How do I secure sensitive data like API keys?**
  - A: Use Rails encrypted credentials. This allows you to store sensitive data securely in your repository, encrypted with a key that is kept out of version control.

- **Q: Should I use RSpec or Minitest for testing?**
  - A: Both are excellent. RSpec is a popular choice for its expressive DSL and BDD style. Minitest is Ruby's default testing framework, lightweight and fast. Choose based on team preference and existing project conventions.

## 5. Anti-Patterns to Flag

### Anti-Pattern: N+1 Query

**BAD:**
```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def index
    @posts = Post.all
  end
end

# app/views/posts/index.html.erb
<% @posts.each do |post| %>
  <h2><%= post.title %></h2>
  <p>Author: <%= post.user.name %></p> <%# N+1 query here %>
<% end %>
```

**GOOD:**
```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def index
    @posts = Post.includes(:user).all # Eager load the user association
  end
end

# app/views/posts/index.html.erb
<% @posts.each do |post| %>
  <h2><%= post.title %></h2>
  <p>Author: <%= post.user.name %></p> <%# No N+1 query %>
<% end %>
```

### Anti-Pattern: Fat Controller

**BAD:**
```ruby
# app/controllers/orders_controller.rb
class OrdersController < ApplicationController
  def create
    @order = Order.new(order_params)
    if @order.save
      # Complex logic for inventory update, email notification, payment processing
      @order.product.update!(stock: @order.product.stock - @order.quantity)
      OrderMailer.confirmation_email(@order).deliver_now
      PaymentGateway.process_payment(@order.total, @order.user.credit_card_token)
      redirect_to @order, notice: 'Order was successfully created.'
    else
      render :new
    end
  end

  private

  def order_params
    params.require(:order).permit(:product_id, :quantity, :user_id)
  end
end
```

**GOOD (using a Service Object):**
```ruby
# app/services/create_order_service.rb
class CreateOrderService
  def initialize(order_params, user)
    @order_params = order_params
    @user = user
  end

  def call
    @order = Order.new(@order_params.merge(user: @user))
    if @order.save
      update_inventory
      send_confirmation_email
      process_payment
      OpenStruct.new(success?: true, order: @order)
    else
      OpenStruct.new(success?: false, order: @order)
    end
  rescue StandardError => e
    OpenStruct.new(success?: false, error: e.message, order: @order)
  end

  private

  def update_inventory
    @order.product.update!(stock: @order.product.stock - @order.quantity)
  end

  def send_confirmation_email
    OrderMailer.confirmation_email(@order).deliver_now
  end

  def process_payment
    PaymentGateway.process_payment(@order.total, @order.user.credit_card_token)
  end
end

# app/controllers/orders_controller.rb
class OrdersController < ApplicationController
  def create
    result = CreateOrderService.new(order_params, current_user).call
    if result.success?
      redirect_to result.order, notice: 'Order was successfully created.'
    else
      @order = result.order # For rendering errors on the form
      flash.now[:alert] = result.error if result.error
      render :new
    end
  end

  private

  def order_params
    params.require(:order).permit(:product_id, :quantity)
  end
end
```

## 6. Code Review Checklist

- [ ] **N+1 Queries**: Are all associations eager loaded where appropriate (e.g., in index actions, nested views)? (Use `Bullet` gem for detection during development).
- [ ] **Business Logic Location**: Is complex business logic encapsulated in Service Objects, Form Objects, or models, rather than controllers or views?
- [ ] **Test Coverage**: Are there adequate tests (unit, integration, feature) for new or modified code?
- [ ] **Security**:
    - [ ] Are sensitive data (API keys, credentials) stored securely (encrypted credentials, environment variables)?
    - [ ] Is input validated and sanitized to prevent XSS/SQL injection?
    - [ ] Is CSRF protection enabled for forms?
- [ ] **Performance**:
    - [ ] Are database queries optimized (indexes, efficient ActiveRecord methods)?
    - [ ] Is caching implemented for expensive operations or view fragments?
    - [ ] Are long-running tasks offloaded to background jobs?
- [ ] **Readability & Maintainability**:
    - [ ] Does the code adhere to Ruby/Rails style guides (e.g., RuboCop)?
    - [ ] Are methods and classes adhering to the Single Responsibility Principle?
    - [ ] Is the code DRY (Don't Repeat Yourself)?
    - [ ] Are variable and method names descriptive?
- [ ] **Hotwire Usage**: If applicable, is Hotwire used effectively for interactivity, avoiding unnecessary JavaScript?
- [ ] **Migrations**: Are database migrations reversible and well-defined?
- [ ] **Error Handling**: Is error handling robust and user-friendly?

## 7. Related Skills

- `typescript-strict-mode`: For frontend TypeScript development if not using Hotwire exclusively.
- `jest-unit-tests`: For JavaScript unit testing if using Stimulus or other JS.
- `ci-cd-pipelines-github-actions`: For automating Rails application testing and deployment.
- `postgres-advanced`: For advanced database optimization and management.
- `docker-compose-services`: For containerizing Rails applications and their dependencies.

## 8. Examples Directory Structure

```
ruby-on-rails-development/
├── examples/
│   ├── hotwire_chat_app/
│   │   ├── app/
│   │   │   ├── controllers/
│   │   │   │   └── messages_controller.rb
│   │   │   ├── models/
│   │   │   │   └── message.rb
│   │   │   └── views/
│   │   │       └── messages/
│   │   │           └── index.html.erb
│   │   └── test/
│   │       └── system/
│   │           └── messages_test.rb
│   ├── service_object_example/
│   │   ├── app/
│   │   │   └── services/
│   │   │       └── create_order_service.rb
│   │   └── test/
│   │       └── unit/
│   │           └── create_order_service_test.rb
│   └── view_component_example/
│       ├── app/
│       │   ├── components/
│       │   │   └── alert_component.rb
│       │   │   └── alert_component.html.erb
│       │   └── views/
│       │       └── layouts/
│       │           └── application.html.erb
│       └── test/
│           └── components/
│               └── alert_component_test.rb
├── patterns/
│   ├── service_object_pattern.md
│   ├── form_object_pattern.md
│   └── hotwire_best_practices.md
├── scripts/
│   ├── generate_service_object.sh
│   ├── check_n_plus_1_queries.py
│   ├── create_migration_with_index.sh
│   └── setup_rspec.sh
└── README.md
```
