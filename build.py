from jinja2 import Environment, FileSystemLoader
import os
import shutil

def generate_static_site():
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Load templates
    index_template = env.get_template('index.html')
    create_genesis_block_template = env.get_template('create_genesis_block.html')
    blockchain_warning_template = env.get_template('blockchain_warning.html')
    add_accidents_template = env.get_template('add_accidents.html')

    # Create output directory if it doesn't exist
    if not os.path.exists('static_site'):
        os.makedirs('static_site')

    # Create subdirectories for static files
    static_dir = 'static'
    if os.path.exists(static_dir):
        if not os.path.exists('static_site/static'):
            os.makedirs('static_site/static')
        # Copy static files to output directory
        for item in os.listdir(static_dir):
            s = os.path.join(static_dir, item)
            d = os.path.join('static_site/static', item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)
    
    # Render templates
    index_html = index_template.render()
    create_genesis_block_html = create_genesis_block_template.render()
    blockchain_warning_html = blockchain_warning_template.render()
    add_accidents_html = add_accidents_template.render(next_year=2024, next_month=1)  # Adjust initial values if needed

    # Save rendered HTML to static site directory
    with open('static_site/index.html', 'w') as f:
        f.write(index_html)
    
    with open('static_site/create_genesis_block.html', 'w') as f:
        f.write(create_genesis_block_html)
    
    with open('static_site/blockchain_warning.html', 'w') as f:
        f.write(blockchain_warning_html)
    
    with open('static_site/add_accidents.html', 'w') as f:
        f.write(add_accidents_html)

if __name__ == '__main__':
    generate_static_site()
