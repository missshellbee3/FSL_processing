import os

wd = os.getcwd() + "/proj-data"
output_file = "sub-ses.txt"
with open(output_file, 'w') as txt_file:
    for sub_folder in os.listdir(wd):
        # Extract sub/ses from default Brainlife download folder names
        if sub_folder.startswith("sub-"):
            split1 = sub_folder.split(".")
            subnum = split1[0].split("-")
            sesnum = split1[1].split("-")
            sub_folder_path = os.path.join(wd, sub_folder)
            # Write sub/ses to file
            txt_file.write(subnum[1] + "\t" + sesnum[1] + "\n")  
            for data_folder in os.listdir(sub_folder_path):
                # Locate data types and rename appropriately
                if data_folder.startswith("dt-neuro-anat"):
                    os.renames(os.path.join(sub_folder_path, data_folder), os.path.join(sub_folder_path, "t1w")) 
                if data_folder.startswith("dt-neuro-func-task"):
                    namesplit = data_folder.split(".")
                    newname = "func-task_" + namesplit[3]
                    os.renames(os.path.join(sub_folder_path, data_folder), os.path.join(sub_folder_path, newname))