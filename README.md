# Course_Grouping
We are trying to fix the course grouping code


## How to use:

1. There's some useful stuff in the ipynb about cleaning up the responses and generating a filtered response list. It may be useful, may not be useful. Often this might end up needing custom code each time.
2. First run the forming_course_data.py (with the right filepaths and stuff). This will spit output in the terminal. copy the output, and save it in a file called course_interrelations.txt This text file should not contain any curly braces or commas, so make sure to remove those after you copy
3. Run the finding_new_groups.py It's going to spit out a first draft grouping.
4. This grouping can then be put into the testing_manual_grups.py, where you can manually move groups to different spots, and check how the grouping will be affected.