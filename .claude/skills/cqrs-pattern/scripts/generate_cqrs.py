import argparse
import os
import sys
from datetime import datetime

def to_kebab_case(name):
    return name.replace(' ', '-').lower()

def to_pascal_case(name):
    return ''.join(word.capitalize() for word in name.split('-'))

def generate_command(name_kebab, name_pascal, output_dir):
    content = f"""// {output_dir}/commands/{name_kebab}.command.ts
export interface {name_pascal}Command {{
  // TODO: Define command payload properties
  readonly id: string;
  readonly payload?: any;
}}
"""
    return f"commands/{name_kebab}.command.ts", content

def generate_command_handler(name_kebab, name_pascal, output_dir):
    content = f"""// {output_dir}/handlers/{name_kebab}.handler.ts
import {{ {name_pascal}Command }} from '../commands/{name_kebab}.command';
import {{ ICommandHandler }} from './interfaces'; // Assuming an interface for handlers

export class {name_pascal}CommandHandler implements ICommandHandler<{name_pascal}Command> {{
  constructor(
    // TODO: Inject dependencies (e.g., repository, event publisher)
  ) {{}}

  async execute(command: {name_pascal}Command): Promise<void> {{
    console.log(`Handling {name_pascal}Command for ID: ${{command.id}}`);
    // TODO:
    // 1. Validate command
    // 2. Load aggregate from repository
    // 3. Apply business logic to aggregate
    // 4. Persist aggregate changes / publish domain events
    // Example:
    // const aggregate = await this.repository.findById(command.id);
    // aggregate.doSomething(command.payload);
    // await this.repository.save(aggregate);
    // await this.eventPublisher.publish(new SomeDomainEvent(command.id, ...));
  }}
}}
"""
    return f"handlers/{name_kebab}.handler.ts", content

def generate_query(name_kebab, name_pascal, output_dir):
    content = f"""// {output_dir}/queries/{name_kebab}.query.ts
export interface {name_pascal}Query {{
  // TODO: Define query parameters
  readonly id: string;
}}

export interface {name_pascal}QueryResult {{
  // TODO: Define query result structure
  readonly data: any;
}}
"""
    return f"queries/{name_kebab}.query.ts", content

def generate_query_handler(name_kebab, name_pascal, output_dir):
    content = f"""// {output_dir}/handlers/{name_kebab}.query-handler.ts
import {{ {name_pascal}Query, {name_pascal}QueryResult }} from '../queries/{name_kebab}.query';
import {{ IQueryHandler }} from './interfaces'; // Assuming an interface for handlers

export class {name_pascal}QueryHandler implements IQueryHandler<{name_pascal}Query, {name_pascal}QueryResult> {{
  constructor(
    // TODO: Inject dependencies (e.g., read model repository)
  ) {{}}

  async execute(query: {name_pascal}Query): Promise<{name_pascal}QueryResult> {{
    console.log(`Handling {name_pascal}Query for ID: ${{query.id}}`);
    // TODO:
    // 1. Retrieve data from the read model (e.g., a denormalized database)
    // 2. Map data to {name_pascal}QueryResult
    // Example:
    // const data = await this.readModelRepository.findById(query.id);
    // if (!data) {{
    //   throw new Error('Resource not found');
    // }}
    // return {{ data }};
    return {{ data: {{}} as any }}; // Placeholder
  }}
}}
"""
    return f"handlers/{name_kebab}.query-handler.ts", content

def generate_event(name_kebab, name_pascal, output_dir):
    content = f"""// {output_dir}/events/{name_kebab}.event.ts
export interface {name_pascal}Event {{
  readonly type: '{name_pascal}'; // Unique event type identifier
  readonly aggregateId: string;
  readonly timestamp: Date;
  // TODO: Define event payload properties (facts about what happened)
  readonly payload?: any;
}}
"""
    return f"events/{name_kebab}.event.ts", content

def generate_handler_interfaces(output_dir):
    content = f"""// {output_dir}/handlers/interfaces.ts
export interface ICommand<T = any> {{
  readonly id: string;
  readonly payload?: T;
}}

export interface IQuery<T = any> {{
  readonly id: string;
  readonly params?: T;
}}

export interface IEvent<T = any> {{
  readonly type: string;
  readonly aggregateId: string;
  readonly timestamp: Date;
  readonly payload?: T;
}}

export interface ICommandHandler<TCommand extends ICommand> {{
  execute(command: TCommand): Promise<void>;
}}

export interface IQueryHandler<TQuery extends IQuery, TResult> {{
  execute(query: TQuery): Promise<TResult>;
}}

export interface IEventHandler<TEvent extends IEvent> {{
  handle(event: TEvent): Promise<void>;
}}
"""
    return f"handlers/interfaces.ts", content

def create_file(filepath, content, dry_run):
    if dry_run:
        print(f"Would create file: {filepath}")
        print("-" * 20)
        print(content)
        print("-" * 20)
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        print(f"File already exists: {filepath}. Skipping.", file=sys.stderr)
        return
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created file: {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate CQRS boilerplate files (Command, Query, Event, Handlers).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "name",
        help="Base name for the CQRS components (e.g., 'CreateUser', 'GetUserById')."
    )
    parser.add_argument(
        "--type",
        choices=["command", "query", "event", "all"],
        default="all",
        help="Type of CQRS component to generate:
"
             "  command: Generates Command and Command Handler.
"
             "  query: Generates Query and Query Handler.
"
             "  event: Generates Event.
"
             "  all: Generates Command, Command Handler, Query, Query Handler, and Event (default)."
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Base output directory for generated files (e.g., 'src/application').
"
             "Files will be placed in subdirectories like 'commands', 'queries', 'events', 'handlers'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without actually creating files."
    )
    parser.add_argument(
        "--force-interfaces",
        action="store_true",
        help="Force creation of handlers/interfaces.ts even if it exists."
    )

    args = parser.parse_args()

    name_kebab = to_kebab_case(args.name)
    name_pascal = to_pascal_case(name_kebab)
    
    base_output_dir = os.path.abspath(args.output_dir)
    
    # Ensure the handlers directory exists for interfaces.ts
    handlers_dir = os.path.join(base_output_dir, "handlers")
    os.makedirs(handlers_dir, exist_ok=True)

    # Always generate interfaces.ts if it doesn't exist or --force-interfaces is used
    interfaces_filepath_relative, interfaces_content = generate_handler_interfaces(base_output_dir)
    interfaces_filepath_absolute = os.path.join(base_output_dir, interfaces_filepath_relative)
    if args.force_interfaces or not os.path.exists(interfaces_filepath_absolute):
        create_file(interfaces_filepath_absolute, interfaces_content, args.dry_run)
    elif not args.dry_run:
        print(f"File already exists: {interfaces_filepath_absolute}. Skipping interfaces.ts creation. Use --force-interfaces to overwrite.", file=sys.stderr)


    files_to_generate = []

    if args.type == "command" or args.type == "all":
        files_to_generate.append(generate_command(name_kebab, name_pascal, base_output_dir))
        files_to_generate.append(generate_command_handler(name_kebab, name_pascal, base_output_dir))
    if args.type == "query" or args.type == "all":
        files_to_generate.append(generate_query(name_kebab, name_pascal, base_output_dir))
        files_to_generate.append(generate_query_handler(name_kebab, name_pascal, base_output_dir))
    if args.type == "event" or args.type == "all":
        files_to_generate.append(generate_event(name_kebab, name_pascal, base_output_dir))

    for relative_path, content in files_to_generate:
        absolute_path = os.path.join(base_output_dir, relative_path)
        create_file(absolute_path, content, args.dry_run)

if __name__ == "__main__":
    main()
