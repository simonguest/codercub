import sys
import nbformat

def main():
    # Read the notebook from standard input
    nb_content = sys.stdin.read()
    nb = nbformat.reads(nb_content, as_version=4)
    
    # Iterate through all cells - omit the cfu cells
    nb.cells = [
        cell for cell in nb.cells
        if not (cell.cell_type == 'raw' and 'cfu' in
    cell.get('metadata', {}).get('tags', []))
    ]
      
    # Write the modified notebook to standard output
    sys.stdout.write(nbformat.writes(nb))

if __name__ == '__main__':
    main()
    