import os

def split_timing_files(folder_path):
    print("Current working directory:", folder_path)
    
    # Dictionary to store lines for each trial-type
    trial_type_lines_dict = {}

    for sub_folder in os.listdir(folder_path):
        # Identify folders relevant to this analysis
        if sub_folder.startswith("WML"):
            sub_folder_path = os.path.join(folder_path, sub_folder)
            print("Processing sub-folder:", sub_folder_path)
            for ses_folder in os.listdir(sub_folder_path):
                # Identify session folders
                if ses_folder.startswith("ses-"):
                    ses_folder_path = os.path.join(sub_folder_path, ses_folder)
                    print("Processing ses-folder:", ses_folder_path)
                    for file_name in os.listdir(ses_folder_path):
                        # Identifier based on timing file name construction in BIDS
                        if file_name.startswith("sub-"):
                            file_path = os.path.join(ses_folder_path, file_name)
                            print("Processing file:", file_path)
                            run_number = None
                            # Extracting run number from file name--assuming timing file is BIDS compliant
                            for part in file_name.split("_"):
                                if part.startswith("run-"):
                                    run_number = part.split("-")[1].split(".")[0]
                            with open(file_path, 'r') as file:
                                lines = file.readlines()
                                trial_type_lines_dict.clear() # Clear out previous file's trial_type data
                                for line in lines:
                                    words = line.split() 
                                    parts = words[2].split("-") # Isolate target vs distractor label regardless of handwritten vs typed
                                    if "trial" not in parts[0]: # Screen out trial_type column heading line
                                        trial_type = parts[1] # To do specific trial types, words[2]
                                        if trial_type not in trial_type_lines_dict:
                                            trial_type_lines_dict[trial_type] = []
                                        trial_type_lines_dict[trial_type].append(line.strip())
                                for trial_type, lines in trial_type_lines_dict.items():                
                                    if run_number is not None:
                                        new_file_name = f"{trial_type}_run-{run_number}.txt"
                                        print(f"Writing to {new_file_name}")
                                        if os.path.exists(os.path.join(ses_folder_path, new_file_name)):
                                            os.remove(os.path.join(ses_folder_path, new_file_name))
                                        with open(os.path.join(ses_folder_path, new_file_name), 'w') as new_file:
                                            for line in lines: 
                                                parts = line.split("\t")                                               
                                                new_file.write(f"{parts[0]} {parts[1]} 1\n") # This pulls the onset and duration columns from a BIDS-compliant timing file and appends a 1 to make it FSL compliant
                                                print(f"{parts[0]} {parts[1]} 1\n")
				
            print("Processing completed.")


folder_path = os.getcwd() 
split_timing_files(folder_path)
