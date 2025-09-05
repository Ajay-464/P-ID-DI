import json
import os
import argparse
from analyzer import analyze_pid
from exporter import save_to_csv, save_to_xml

def main():
    """
    Main function to run the P&ID Digitizer application.
    """
   
    parser = argparse.ArgumentParser(description="Digitize P&ID diagrams using AI.")
    parser.add_argument("filename", type=str, help="The name of the P&ID image file located in the data/input_pids/ folder.")
    
    args = parser.parse_args()
    input_filename = args.filename


    input_path = os.path.join("..", "data", "input_pids", input_filename)
    json_output_dir = os.path.join("..", "data", "output_json")
    csv_output_dir = os.path.join("..", "data", "output_csv") 


    os.makedirs(json_output_dir, exist_ok=True)
    os.makedirs(csv_output_dir, exist_ok=True)
    
  
    if not os.path.exists(input_path):
        print(f"****** Error: Input file not found at {input_path}")
        return


    extracted_data = analyze_pid(input_path)

   
    if extracted_data:
        base_filename = os.path.splitext(input_filename)[0]
        
        # Save as JSON
        json_output_path = os.path.join(json_output_dir, base_filename + ".json")
        with open(json_output_path, "w") as f:
            json.dump(extracted_data, f, indent=2)
        print(f"\n JSON results saved to {json_output_path}")

        save_to_csv(extracted_data, csv_output_dir, base_filename)
        
                # Save as XML
        xml_output_path = os.path.join(xml_output_dir, base_filename + ".xml")
        save_to_xml(extracted_data, xml_output_path)
        print(f"\n XML results saved to {xml_output_path}")

if __name__ == "__main__":
    main()