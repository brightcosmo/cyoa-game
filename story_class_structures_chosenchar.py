# import statement
from story_class_structures_bestchar import *

####
#### TASK 5
####

class StoryChosen(StoryBest):
    """
    StoryBest class inherits from the StoryBest class (which inherits from the Story class), and has the same attributes.

    Each character in the story is now represented by their name rather than a character code.
    Additionally, the object contructor, select_character_for_check and select_option methods have been revised as follows:

    __init__:
    Now replaces character codes within each scenes description and option text with the character names supplied from characters_in_story.

    select_character_for_check:
    The character used to perform the check will be set to the character object in option_char, if none are supplied, the method will determine the best character to make the check
    within the list of scene_chars. If scene_chars is empty, the method will determine the best character from all characters in the story object.

    select_option:
    The select_option method now iterates over each scene description and scene option to determine what characters are present in the scene and the first character mentioned in the option's text.
    It then supplies this information in the form of 2 lists as parameters for select_character_for_check.
    
    """

    def __init__(self, scene_string_data: list, characters_in_story: list) -> None:
        """
         This function instantiates the instance variables for the Story class.
         It has been slightly modified to replace the character codes in each scenes description and option text with the character names from characters_in_story

        Parameters:
            scene_string_data: A list of strings separated by a delimiter which represent scene ID, description, and options.
            characters_in_story: A list of characters' data separated by a delimiter representing name, attribute scores, and skill proficiency. 
        """

        # initializes scenes and characters using the superclass
        super().__init__(scene_string_data,characters_in_story)
        
        # creates a string to be used as the argument for string formatting
        format_str = ""

        # adds formatting for every character to convert the character code to its name
        for index in range(len(self.characters)):
            item_to_format = "C" + str(index+1)
            name = self.characters[index].name
            format_str += " , " + item_to_format + " = \"" + name + "\""

        # removes the first three characters (" , ")
        format_str = format_str[3:]
        
        # character codes will be converted to name in all scene and option descriptions
        format_scene_description = "scene.description = scene.description.format(" + format_str + ")"
        format_option_description = "option.description = option.description.format(" + format_str + ")"

        # formats every scene's description
        for scene in self.scenes.values():
            exec(format_scene_description) # exec() can run strings as code so we modify the .format string each time in the code above the run it.

            # formats every option's description within that scene
            for option in scene.options.values():
                exec(format_option_description)

 

    def select_character_for_check(self, skill_or_attribute_name: str, scene_chars: list, option_char) -> Character:
        """
        Returns the the character specified in option_char, or, if option_char is empty,
        checks every character's value in scene_chars for the skill/attribute, including proficiency but excluding
        the random element, and returns the name of the character with the highest value.
        If there are multiple characters with the highest value, return the first one found.

        Attributes:
            skill_or_attribute_name: The attribute or skill being checked.
            scene_chars : The characters present within a scene.
            option_char : The first character to appear in the option's text

        Returns:
            The name attribute of the first character with the highest value of the skill/attribute or the character specified in option_char.
        """
        # if options_char is an empty list have the best character within the scene make the check
        if option_char == []:

            # if scene_chars is empty set the list of possible_chars to all the characters within the story object
            if scene_chars == []:
                possible_chars = self.characters
            
            # if not, set the list of possible_chars to scene_chars
            else:
                possible_chars = scene_chars 

            # use super() to run the method from the parent class and supply it the optional parameter possible_chars
            return super().select_character_for_check(skill_or_attribute_name,possible_chars) 

        # if a character has been specified in the option text, return that character
        else:
            return option_char[0] 


    def select_option(self, option_number: int, override: int) -> None:
        """
        Allows the user to select an option to progress the story, and updates current_scene based on the outcome.
        Also responsible for iterating over each scenes description and option text to determine which characters are available in each scene and option.

        Parameters:
            option_number: An integer representing the option chosen, shown at the end of the scene.
            override: Optional variable used to override the random element in make_check of the character instances.
            character: An optional instance of Character, which is None by default.
                       This is used for the StoryChosen class which inherits from StoryBest.

        """
        # checks if the game is over raises StopIteration with human readable text
        if "E" in self.current_scene.ID:
            raise StopIteration("the game is over")

        # if the chosen option is in the current scenes options
        if option_number in self.current_scene.options:
            
            #set the variables sceme_chars and option_char to empty lists
            scene_chars = list()
            option_char = list()
             
            # for each character in the story
            for char in self.characters:

                if char.name in self.current_scene.description: # if the characters name is in the current scenes description
                    scene_chars.append(char) # append it to scene_chars 

                # if the characters name is in the currently select option of the currently select scene, append it to option_char. This is only done once per option.
                if char.name in self.current_scene.options[option_number].description and option_char == []:
                    option_char.append(char)

            # obtains the chosen option using the list with the option number as the index
            chosen_option = self.current_scene.options[option_number]
            
            # if the option exists, obtain the option object's attribute and difficulty
            if chosen_option.attribute != None:
                skill_or_attribute_name = chosen_option.attribute
                difficulty = chosen_option.difficulty

            # if not, default value for skill/attribute is None and default difficulty is 0
            else:
                skill_or_attribute_name = None
                difficulty = 0
            
            # if override is not an integer, set it to none
            if type(override) != int:
                override = None
            
            # if skill_or_attribute_name is not none, set the character_used to the best character to make the check
            if skill_or_attribute_name != None:
                character_used = self.select_character_for_check(skill_or_attribute_name,scene_chars,option_char)
            
            # else set it to the first character in the story object
            else:
                character_used = self.characters[0]

            # call the method from the parent class and supply it with the optional parameter character_used
            super().select_option(option_number,override,character_used) 
