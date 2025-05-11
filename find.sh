# find files ending in out
find . -type f -name "*.out" -print0 | while IFS= read -r -d '' file; do
    # Check if the file is empty
    if [ ! -s "$file" ]; then
        echo "Empty file: $file"
    else
        echo "Non-empty file: $file"
    fi
done