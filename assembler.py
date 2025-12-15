import os
import sys

def assemble_model():
    # --- CONFIGURATION ---
    # The final name you want for your model
    output_filename = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    
    print(f"--- Model Assembler ---")
    print(f"Target File: {output_filename}")

    # 1. Find all split files in the current folder
    # We look for files that end in a number (like .001, .081)
    # and exclude this script itself.
    files = [f for f in os.listdir('.') 
             if f[-3:].isdigit() 
             and not f.endswith('.py')
             and "Llama" in f] # Filtering for Llama files specifically

    if not files:
        print("\n[ERROR] No split files found!")
        print("Make sure this script is in the same folder as the .001, .002 files.")
        input("Press Enter to exit...")
        sys.exit()

    # 2. Sort the files numerically
    # This ensures .002 comes after .001, and .010 comes after .009
    # We strictly sort by the last 3 digits of the filename.
    try:
        files.sort(key=lambda x: int(x.split('.')[-1]))
    except Exception as e:
        print(f"\n[ERROR] sorting files: {e}")
        input("Press Enter to exit...")
        sys.exit()

    print(f"Found {len(files)} parts.")
    print(f"First part: {files[0]}")
    print(f"Last part:  {files[-1]}")
    
    # 3. Stitch them together
    print("\nStarting assembly... (This may take a minute)")
    
    try:
        with open(output_filename, 'wb') as outfile:
            for index, part in enumerate(files):
                # Print progress every 5 files to keep the user updated
                if (index + 1) % 5 == 0 or index == 0 or index == len(files) - 1:
                    print(f"Processing part {index + 1}/{len(files)}: {part}")
                
                with open(part, 'rb') as infile:
                    # Read the chunk and write it to the main file
                    outfile.write(infile.read())
                    
        print(f"\n[SUCCESS] File created: {output_filename}")
        
        # 4. Verify Size
        final_size_gb = os.path.getsize(output_filename) / (1024 * 1024 * 1024)
        print(f"Final Size: {final_size_gb:.2f} GB")
        print("You can now proceed with 'ollama create'.")
        
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")

    input("\nPress Enter to close...")

if __name__ == "__main__":
    assemble_model()
