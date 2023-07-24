#### TASK 3
####


def read_file(filename: str) -> list:
    """
    Reads a file and returns a list of strings from the file, excluding empty strings.
    Parameters:
        filename: The name of the file to be read.
    Returns:
        file_lines: A list of strings where each list element represents one line in the file.
    """
    # reads the file and creates the list for each line
    file_lines = [line.strip() for line in open (filename, "r")]

    # removes any extra whitespace
    file_lines = [line for line in file_lines if line not in ("")]

    # returns the list
    return file_lines

##
##

if __name__ == "__main__":

    # imports everything from story_class_structures_chosenchar
    from story_class_structures_chosenchar import *

    # creates a new StoryChosen object, reading the sample files for the scene and characters
    story = StoryChosen(read_file("sample_story.txt"), read_file("sample_chars.txt"))

    # continues until scene ID has an "E" (the end scene)
    while "E" not in story.get_scene_id():
        
        # displays the current scene
        print(story.show_current_scene())

        # continues until a valid option is chosen
        valid_option = False
        while valid_option == False:
            
            # takes in an input for the option, and validates this input
            try:
                number = int(input("Enter your choice: "))
                assert number in story.current_scene.options
                valid_option = True
            
            # prints error if the input is not an integer
            except ValueError:
                print("ERROR: Input was not an integer.")
                continue
            
            # prints error if the integer was not an option
            except AssertionError:
                print("ERROR: Input was not on the list of options.")
                continue

        # selects the option in the scene, with no random modifier
        story.select_option(number, None)

    # prints the final scene
    print("\n" + story.show_current_scene())
