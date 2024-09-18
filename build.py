from jinja2 import Environment, FileSystemLoader
import os
import shutil

def generate_static_site():
    # Set up Jinja2 environment
    print("Setting up Jinja2 environment...")
    env = Environment(loader=FileSystemLoader('templates'))

    # Load templates
    try:
        index_template = env.get_template('index.html')
        create_genesis_block_template = env.get_template('create_genesis_block.html')
        blockchain_warning_template = env.get_template('blockchain_warning.html')
        add_accidents_template = env.get_template('add_accidents.html')
    except Exception as e:
        print(f"Error loading templates: {e}")
        return

    # Create output directory if it doesn't exist
    output_dir = 'static_site'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Create subdirectory for static files
    static_output_dir = os.path.join(output_dir, 'static')
    if not os.path.exists(static_output_dir):
        os.makedirs(static_output_dir)
        print(f"Created static output directory: {static_output_dir}")

    # Copy static files to output directory
    static_dir = 'static'
    if os.path.exists(static_dir):
        for item in os.listdir(static_dir):
            s = os.path.join(static_dir, item)
            d = os.path.join(static_output_dir, item)
            try:
                if os.path.isdir(s):
                    shutil.copytree(s, d, False, None)
                else:
                    shutil.copy2(s, d)
                print(f"Copied {s} to {d}")
            except Exception as e:
                print(f"Error copying file {s}: {e}")
    else:
        print(f"Static directory '{static_dir}' does not exist.")

    # Render templates
    try:
        index_html = index_template.render()
        create_genesis_block_html = create_genesis_block_template.render()
        blockchain_warning_html = blockchain_warning_template.render()
        add_accidents_html = add_accidents_template.render(next_year=2024, next_month=1)  # Adjust initial values if needed

        # Print rendered HTML content for debugging
        print("Index HTML content:")
        print(index_html[:500])  # Print only the first 500 characters for brevity
        
        print("Create Genesis Block HTML content:")
        print(create_genesis_block_html[:500])
        
        print("Blockchain Warning HTML content:")
        print(blockchain_warning_html[:500])
        
        print("Add Accidents HTML content:")
        print(add_accidents_html[:500])

        # Save rendered HTML to static site directory
        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(index_html)
        
        with open(os.path.join(output_dir, 'create_genesis_block.html'), 'w') as f:
            f.write(create_genesis_block_html)
        
        with open(os.path.join(output_dir, 'blockchain_warning.html'), 'w') as f:
            f.write(blockchain_warning_html)
        
        with open(os.path.join(output_dir, 'add_accidents.html'), 'w') as f:
            f.write(add_accidents_html)

        print("HTML files generated successfully.")
    
    except Exception as e:
        print(f"An error occurred while rendering templates: {e}")

if __name__ == '__main__':
    generate_static_site()
