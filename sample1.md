# Sample Markdown File 1

This is a sample markdown file with indented code blocks.

## Python Code Example

Here's a Python function:

```
def hello_world(name="World"):
    """
    A simple greeting function
    """
    message = f"Hello, {name}!"
    print(message)
    return message

# Call the function
result = hello_world("Python")
```

## JavaScript Example

Some JavaScript code:

```
function calculateSum(a, b) {
    // Add two numbers
    const sum = a + b;
    console.log(`The sum is: ${sum}`);
    return sum;
}

const result = calculateSum(5, 3);
```

## Mixed Content

Regular text here.

```
# This is a bash script
#!/bin/bash
echo "Starting process..."

for i in {1..5}; do
    echo "Processing item $i"
done

echo "Process complete!"
```

More regular text after the code block.

## Already Fenced

This code block is already properly fenced:

```python
def already_good():
    return "This should not be changed"
```

End of file.