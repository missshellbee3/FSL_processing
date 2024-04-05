!/bin/bash

BASE_DIR=$(pwd)
echo "$BASE_DIR"

while IFS=$'\t' read -r id session; do
    subj="sub-$id.ses-$session"
    ses="ses-$session"
    echo "===> Starting processing of $subj"
    echo

    SUBJ_DIR="${BASE_DIR}/proj-data/${subj}"

    if [ -d "$SUBJ_DIR" ]; then

        cd "$SUBJ_DIR"
            # Check if the brain mask doesn’t exist, create it
            if [ ! -f "$SUBJ_DIR/t1w/t1_brain.nii.gz" ]; then
                echo "Skull-stripped brain not found, using bet with a fractional intensity threshold of 0.2"
                bet2 $SUBJ_DIR/t1w/t1.nii.gz \
                $SUBJ_DIR/t1w/t1_brain.nii.gz -f 0.2
            fi
             
            # Loop through your FSF templates
            for run in 1 2; do
                    # Assuming your functional data is stored in a standard path/format
                FMRI_FILE="${SUBJ_DIR}/func-task_run-${run}/bold.nii.gz" # Adjust as needed

                if [ -f "$FMRI_FILE" ]; then
                    # Extract the number of time points
                    npts=$(fslval "$FMRI_FILE" dim4)
                    echo "Run ${run} has ${npts} volumes"
                else
                    echo "FMRI data file not found for $subj, skipping..."
                fi

                fsf_template="design_run${run}.fsf"
                cp "${BASE_DIR}/${fsf_template}" "${SUBJ_DIR}/${fsf_template}"
                
                # Update the new FSF file with the correct subject, session, and ntpts
                sed -i '' "s|set fmri(npts) .*|set fmri(npts) $npts|g" "${SUBJ_DIR}/${fsf_template}"
                sed -i '' "s|sub-WML041.ses-1|${subj}|g" "${SUBJ_DIR}/${fsf_template}"
                sed -i '' "s|/WML041|/${id}|g" "${SUBJ_DIR}/${fsf_template}"
                sed -i '' "s|/ses-1|/${ses}|g" "${SUBJ_DIR}/${fsf_template}"

                if [ -d "${SUBJ_DIR}/run${run}.feat" ]; then
                    rm -r "${SUBJ_DIR}/run${run}.feat"
                fi
                
                # Now, you can run feat on the updated FSF file
                echo "===> Starting feat for ${SUBJ_DIR}/${fsf_template}"
                feat "${SUBJ_DIR}/${fsf_template}"
            done
                
        echo
    else
        echo "Directory $SUBJ_DIR does not exist. Skipping..."
    fi

    # Ensure you return to the BASE_DIR after each subject
    cd "$BASE_DIR"
done < sub-ses.txt

echo
