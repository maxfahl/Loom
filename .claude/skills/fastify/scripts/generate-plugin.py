import argparse
import os
import sys
from datetime import datetime

# --- Helper Functions ---
def log_info(message):
    print(f"\033[0;34m[INFO]\033[0m {message}")

def log_success(message):
    print(f"\033[0;32m[SUCCESS]\033[0m {message}")

def log_error(message):
    print(f"\033[0;31m[ERROR]\033[0m {message}")
    sys.exit(1)

def get_input(prompt, default=None):
    while True:
        user_input = input(f"\033[0;36m[INPUT]\033[0m {prompt} ").strip()
        if user_input:
            return user_input
        elif default is not None:
            return default
        else:
            log_error("Input cannot be empty.")

def main():
    parser = argparse.ArgumentParser(
        description="Scaffolds a new Fastify plugin file, ensuring it's correctly wrapped with fastify-plugin."
    )
    parser.add_argument(
        "--name",
        help="Name of the plugin (e.g., auth, database). Will be used for filename and plugin name."
    )
    parser.add_argument(
        "--output-dir",
        default="src/plugins",
        help="Output directory for the generated plugin file (default: src/plugins)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    plugin_name = args.name or get_input("Enter plugin name (e.g., auth, database)")
    plugin_description = get_input("Enter a brief description for the plugin", default=f"A Fastify plugin for {plugin_name} functionality.")

    camel_case_plugin_name = ''.join(word.capitalize() for word in plugin_name.split('-'))

    file_content = f"""import {{ FastifyInstance, FastifyPluginOptions }} from 'fastify';
import fastifyPlugin from 'fastify-plugin';

// Optionally extend FastifyInstance, FastifyRequest, or FastifyReply types
// declare module 'fastify' {{
//   interface FastifyInstance {{
//     someUtility: (message: string) => void;
//   }}
//   interface FastifyRequest {{
//     user: {{ id: string }};
//   }}
// }}

/**
 * {plugin_description}
 *
 * @param fastify The Fastify instance
 * @param opts Plugin options
 */
async function {camel_case_plugin_name}Plugin(fastify: FastifyInstance, opts: FastifyPluginOptions) {{
  // Example: Decorate the Fastify instance with a utility method
  // fastify.decorate('someUtility', (message: string) => {{
  //   fastify.log.info(`[{{camel_case_plugin_name}}Plugin] Utility called with: ${{message}}`);
  // }});

  // Example: Add a hook
  // fastify.addHook('onRequest', (request, reply, done) => {{
  //   request.log.info(`[{{camel_case_plugin_name}}Plugin] Incoming request: ${{request.method}} ${{request.url}}`);
  //   done();
  // }});

  // Example: Register routes within the plugin
  // fastify.get('/{plugin_name}-status', async (request, reply) => {{
  //   return {{ status: 'ok', plugin: '{plugin_name}' }};
  // }});

  fastify.log.info(`{{camel_case_plugin_name}}Plugin loaded.`);
}}

// Wrap the plugin with fastify-plugin to ensure proper encapsulation and avoid scope issues.
// This makes the plugin available to the entire Fastify application instance.
export default fastifyPlugin({camel_case_plugin_name}Plugin, {{ name: '{plugin_name}-plugin' }});

// Example of how to register this plugin in your main application file:
/*
import Fastify from 'fastify';
import {{camel_case_plugin_name}}Plugin from './plugins/{plugin_name}-plugin';

const app = Fastify({{ logger: true }});

app.register({camel_case_plugin_name}Plugin, {{ /* options here */ }});

const start = async () => {{
  try {{
    await app.listen({{ port: 3000 }});
    app.log.info(`Server listening on ${{app.server.address()}}`);
  }} catch (err) {{
    app.log.error(err);
    process.exit(1);
  }}
}};

start();
*/
"""

    if args.dry_run:
        log_info("Dry run: Generated content:")
        print(file_content)
    else:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{plugin_name.lower()}-plugin.ts")

        with open(file_path, "w") as f:
            f.write(file_content)
        log_success(f"Plugin file created: {file_path}")
        log_info(f"Remember to register this plugin in your main Fastify application:\n  fastify.register({camel_case_plugin_name}Plugin, {{ /* options */ }});")

if __name__ == "__main__":
    main()
