# import statements
from story_class_structures import *
from choose_your_own_adventure import read_file

####
#### TASK 4
####

class StoryBest(Story):
    """
    StoryBest class inherits from the Story class, and has the same attributes.
    One new method has been added, select_character_for_check, and select_option has been modified:

    select_character_for_check:
        The first name of the character with the highest value of a skill/attribute will be returned.

    select_option:
        This method has been modified to always use the character returned from this select_character_for_check.
    """
    
    def select_character_for_check(self, skill_or_attribute_name, available_chars: list = None) -> str:
        """
        Checks every character's value for the skill/attribute, including proficiency but excluding
        the random element, and returns the name of the character with the highest value.
        If there are multiple characters with the highest value, return the first one found.

        Attributes:
            skill_or_attribute_name: The attribute or skill being checked.
            available_chars: An optional list of character instances, set to None by default (all characters are checked).
                             This is used for the StoryChosen class which inherits from StoryBest.
        
        Returns:
            The name attribute of the first character with the highest value of the skill/attribute.
        """

        # if no list of characters were input, use all characters in this story class
        if available_chars == None or available_chars == []:
            available_chars = self.characters

        # print("available_chars:",available_chars)
        # instantiates a list for the score values
        score_list = []
        
        # for every character in the list
        for chara in available_chars:
            
            # the character's score for a choice using a given skill or attribute is calculated
            score = chara.calculate_score(skill_or_attribute_name)

            # adds the score to the score list
            score_list.append(score)

        # finds the highest score
        best_score = max(score_list)

        # checks every score in the list
        for score in score_list:
            
            # finds the first score matching the highest score, and returns it
            if score == best_score:

                # the index of the best score is the index used for the character returned
                score_index = score_list.index(score)
                return available_chars[score_index]

    ##
    ##


    def select_option(self, option_number: int, override: int, character: Character = None) -> None:
        """
        Allows the user to select an option to progress the story, and updates current_scene based on the outcome.
        Parameters:
            option_number: An integer representing the option chosen, shown at the end of the scene.
            override: Optional variable used to override the random element in make_check of the character instances.
            character: An optional instance of Character, which is None by default.
                       This is used for the StoryChosen class which inherits from StoryBest.
        """

        # sets the option number if the it is in the list of options from the scene
        if option_number in self.current_scene.options:
            chosen_option = self.current_scene.options[option_number]
            
            # if the chosen option requires a skill/attribute and difficulty
            if chosen_option.attribute != None:
                skill_or_attribute_name = chosen_option.attribute
                difficulty = chosen_option.difficulty

            # if not, default value for skill/attribute is None and default difficulty is 0
            else:
                skill_or_attribute_name = None
                difficulty = 0

        # otherwise, raises an error as the option was not in the list
        else:
            raise ValueError("Invalid option.")

        # if no character was input
        if character == None:

            # and no skill/attribute was input, check for the best character to perform the action
            if skill_or_attribute_name != None:
                character_used = self.select_character_for_check(skill_or_attribute_name)

            # otherwise, use the first character in the list
            else:
                character_used = self.characters[0]

        # otherwise, use the character input
        else:
            character_used = character

        # runs select_option from the main Story class using the option number, random override, and character used
        super().select_option(option_number,override,character_used)
