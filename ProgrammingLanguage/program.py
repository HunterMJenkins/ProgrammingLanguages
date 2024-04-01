import javalang
import json

def print_ast(node, indent=""):
    """Recursively prints the AST in a structured format."""
    if node is None:
        return

    if isinstance(node, javalang.tree.Node):
        print(f"{indent}type: {node.__class__.__name__}")
        for field_name in node.attrs:
            field_value = getattr(node, field_name)
            print(f"{indent}  {field_name}:")
            print_ast(field_value, indent + "    ")
    elif isinstance(node, list):
        for index, item in enumerate(node):
            print(f"{indent}  - index: {index}")
            print_ast(item, indent + "    ")
    else:
        print(f"{indent}{node}")

def node_to_dict(node):
    """Converts a javalang.tree.Node to a dictionary, handling set objects."""
    if isinstance(node, javalang.tree.Node):
        node_dict = {'type': node.__class__.__name__}
        for attr in node.attrs:
            value = getattr(node, attr)
            if isinstance(value, set):
                # Convert set to list for JSON serialization
                node_dict[attr] = list(value)
            else:
                node_dict[attr] = node_to_dict(value)
        return node_dict
    elif isinstance(node, list):
        return [node_to_dict(item) for item in node]
    elif isinstance(node, set):
        # Convert set to list for JSON serialization
        return list(node)
    else:
        return node


def parse_java_file(file_path):
    """Parses a Java file and returns the AST."""
    with open(file_path, 'r') as file:
        content = file.read()
    tree = javalang.parse.parse(content)
    return tree

def main(java_file_path, json_file_path):
    """Main function to parse the Java file, print and output the AST to a JSON file."""
    tree = parse_java_file(java_file_path)
    
    print("Printing AST to console:")
    print_ast(tree)
    
    ast_dict = node_to_dict(tree)
    with open(json_file_path, 'w') as json_file:
        print("\nSaving AST to JSON file...")
        json.dump(ast_dict, json_file, indent=4)
    print("AST saved to JSON file successfully.")

# Replace 'path/to/your/Example.java' with the actual path to your Java file
java_file_path = 'DefaultTexParserTest.java'
# Specify the path where you want to save the JSON file
json_file_path = 'ast4.json'
main(java_file_path, json_file_path)
