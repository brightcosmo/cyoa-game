# import statement
import random

####
#### TASK 1 , TASK 2
####

class Character:
    """
    The Character class is used to represent characters as objects and manipulate their data.
    Attributes
        name (str): name of the character
        acumen (int): ability score for acumen stat
        body (int): ability score for body stat
        charm (int): ability score for charm stat
        proficiency (str): the proficiency of the character
    """

    # a class variable containing the three stats of a character
    AttributeList = ["acumen","body","charm"]

    # a class variable with the 6 proficiencies as keys
    # and the values being their corresponding stat
    SkillDict = {
                "diplomacy" : "charm" ,
                "investigation" : "acumen" , 
                "medicine" : "acumen" , 
                "language" : "charm" , 
                "acrobatics" : "body", 
                "craft" : "body"
                }


    def __init__(self, string_input: list) -> None:
        """
        This function instantiates the instance variables for the Character class.
        Parameters:
            string_input: a list of three strings representing a character
        """
        # string input example : ['Marian Croak', 'A4 B1 C2', 'Di In* Me La Ac Cr']
        
        # the method process_character_string returns a list with 5 values
        # the list is in the format [name, acumen, body, charm, proficiency]
        string_stats = self.process_character_string(string_input)
        #['Marian Croak', 4, 1, 2, 'investigation']
        
        # character name 
        self.name = string_stats[0]

        # attributes
        self.acumen = string_stats[1]
        self.body = string_stats[2]
        self.charm = string_stats[3]

        # proficiency
        self.proficiency = string_stats[4]

    ##
    ##

    def process_character_string(self, string_input: list) -> list:
        """
        This function takes a list of strings representing a character, 
        and returns a list with five values which represent the five instance variables.
        Parameters:
            string_input: a list of three strings representing a character
        Returns:
            return_list: a list containing the name, acumen score, body score, charm score and proficiency of a character
        """
        # string input example : ['Marian Croak', 'A4 B1 C2', 'Di In* Me La Ac Cr']

        # takes the string representing attributes in string_input and removes "A", "B" and "C"
        attributes = string_input[1].translate({65:None,66:None,67:None})

        # splits attributes into a list with three values
        stats = attributes.split()
        
        # converts the 3 elements of stats into integers
        stats = [int(x) for x in stats]
       
        
        # checks that each score in stats is between 1 and 4 inclusive 
        # raises ValueError if they aren't 
        if stats[0] < 1 or stats[0] > 4: 
            raise ValueError(f"invalid value for acumen; {stats[0]} is not in the range 1 to 4")
        if stats[1] < 1 or stats[1] > 4: 
            raise ValueError(f"invalid value for body; {stats[1]} is not in the range 1 to 4")
        if stats[2] < 1 or stats[2] > 4:
            raise ValueError(f"invalid value for charm; {stats[2]} is not in the range 1 to 4")
        
        # checks if the sum of the three ability scores is 7
        # if it isn't, ValueError is raised
        if sum(stats) != 7:
            raise ValueError(f"A{stats[0]} B{stats[1]} C{stats[2]} is invalid, sum of attributes does not equal 7")

        
        # the line representing proficiencies is split into a list using space as a delimiter
        # the list is stored in proficiency_line
        proficiency_line = string_input[2].split(" ")

        # prof_count will keep track of the number of proficiencies (signified by asterisks) detected
        prof_count = 0
        
        # checks each skill in the line to see if:
        # 1) it is a valid skill
        # 2) it contains an asterisk
        
        for skill in proficiency_line:
            
            if self.proficiency_converter(skill.strip("*")) in self.SkillDict:
                if "*" in skill:
                    # when a proficiency is detected
                    # proficiency is set to the full word represented by skill
                    # prof_count is incremented by 1
                    proficiency = self.proficiency_converter(skill.strip("*"))
                    prof_count += 1

            else:
                # if a skill that doesn't exist is detected, ValueError is raised
                raise ValueError(f"{string_input[2]} is invalid; unexpected skill name given")
                
        # if the amount of proficiencies detected is not 1, a ValueError is raised
        if prof_count != 1:
            raise ValueError(f"{string_input[2]} is invalid; exactly one proficiency asterisk expected")
        
        # if the proficiency is invalid, a ValueError is raised
        if proficiency == "invalid":
            raise ValueError(f"{string_input[2]} is invalid; unexpected skill name given")
        
        # return_list = [name , acumen , body , charm , proficiency]
        return_list = [string_input[0],stats[0],stats[1],stats[2],proficiency]

        return return_list

    ##
    ##

    def proficiency_converter(self, proficiency_short: str) -> str:
        # print("proficiency_short:",proficiency_short)
        """
        Converts the abbreviated proficiency from the string_input.
        Parameters:
            proficiency_short: a two character string representing the proficiency
        Returns:
            proficiency: a string representing the full name of the proficiency
        """
        # uses match case to return the full name of the proficiency
        match proficiency_short:
            case "Di":
                proficiency = "diplomacy"
            case "In":
                proficiency = "investigation"
            case "Me":
                proficiency = "medicine"
            case "La":
                proficiency = "language"
            case "Ac":
                proficiency = "acrobatics"
            case "Cr":
                proficiency = "craft"
            case default: 
                proficiency = "invalid"
        return proficiency

    ##
    ##

    def get_name(self) -> str:
        """
        Returns the name attribute of the class.
        """
        return self.name
    
    ##
    ##

    def get_acumen(self) -> int:
        """
        Returns the acumen attribute of the class.
        """
        return self.acumen

    ##
    ##

    def get_body(self) -> int:
        """
        Returns the body attribute of the class.
        """
        return self.body

    ##
    ##

    def get_charm(self) -> int:
        """
        Returns the charm attribute of the class.
        """
        return self.charm

    ##
    ##

    def get_proficient(self) -> str:
        """
        Returns the proficiency attribute of the class.
        """
        return self.proficiency

    ##
    ##

    def make_check(self, skill_or_attribute_name: str, difficulty: int, override_random: int) -> str:
        """
        Calculates a score based on a skill or attribute and a random modifier (which can be overriden).
        The score is compared to a difficulty to generate and return an outcome.
        Parameters:
            skill_or_attribute_name: the skill or attribute of a character that influences the score
            difficulty: the value of the difficulty to compare the final score to
            override_random: an optional variable that overrides the random element - for testing purposes only
        Returns:
            A string representing the level of success (++, +, -, --).
        """

        # if override_random is provided and it is an integer, it is used in place of the random element
        if type(override_random) == int:
            random_element = override_random

        # if override_random is not provided, random element is calculated
        else:
            
            random_element = sum([random.randint(-1,1),random.randint(-1,1),random.randint(-1,1)])
            #The random element is determined by randomly selecting one of (-1,0,1) threee times

        # calculates final score based on the character's attribute score, random element, and the proficiency bonus
        score =  random_element + self.calculate_score(skill_or_attribute_name,difficulty)

        # returns:
            # "--" denoting overwhelming failure if the score is (difficulty - 4) or less
            # "-" denoting failure if the score is (difficulty - 1) or less
            # "+" denoting success if the score is (difficulty + 2) or less 
            # "++" denoting overwhelming success otherwise, as it is greater than (difficulty + 2)

        if score <= difficulty - 4:
            return "--"
        elif score <= difficulty - 1:
            return "-"
        elif score <= difficulty + 2:
            return "+"
        else:
            return "++"
            

    def calculate_score(self, skill_or_attribute_name: str, difficulty: int = 0) -> int:
        """
        Calculates and returns a score based on a character's attributes and a given skill or attribute.
        Parameters:
            skill_or_attribute_name: the skill or attribute of a character that influences the score
            difficulty: the value of the difficulty to compare the final score to
        Returns:
            An integer score calculated based on the provided skill or attribute
        """

        # initialises score as 0
        score = 0

        # if a skill is provided, match it with the associated attribute name
        if skill_or_attribute_name in self.SkillDict:
            attribute_name = self.SkillDict[skill_or_attribute_name]
            
            # if the character is proficient in that skill, 2 will be added to the final score
            if skill_or_attribute_name == self.proficiency:
                score += 2
                
        # if an attribute is provided, use its name to get that character's attribute
        elif skill_or_attribute_name in Character.AttributeList:
            attribute_name = skill_or_attribute_name 

        # if no skill or attribute is provided, a value that would result in overwhelming failure is returned
        # source: https://edstem.org/au/courses/7542/discussion/865983?answer=1944613 
        elif skill_or_attribute_name == None:
            return difficulty - 4
            
        # otherwise, raises an error
        else:
            raise ValueError("not an attribute or a skill")

        # adds the acumen, body, or charm score to score depending on the attribute_name
        if attribute_name == "acumen":
            score += self.acumen
        elif attribute_name == "body":
            score += self.body
        elif attribute_name == "charm":
            score += self.charm

        return score

    ##
    ##
    
    def __str__(self) -> str:
        """
        Returns the class formatted as a string.
        """
        str_char = f"{self.name} [A{self.acumen} B{self.body} C{self.charm}] is proficient in {self.proficiency}"
        return str_char


##
##


class Story: 
    """ 
    The Story class is used to represent stories.
    The class also tracks the current scene and lets the user move on to the next one by choosing an option.

    Attributes:
        characters (list): A list of character objects that are part of the story.
        scenes (dict): A dictionary of scene objects that are part of the story with the keys as scene ids.
        current_scene (str): The ID of the currently active scene.
    """
    
    def __init__(self,scene_string_data: list, characters_in_story: list) -> None:
        """
        This function instantiates the instance variables for the Story class.
        Parameters:
            scene_string_data: A list of strings separated by a delimiter which represent scene ID, description, and options.
            characters_in_story: A list of characters' data separated by a delimiter representing name, attribute scores, and skill proficiency. 
        """
        # initialize list of character objects
        self.characters = [Character(character) for character in list(self.file_processor(characters_in_story, '----'))]

        # initializes dictionary containing all scenes
        self.scenes = self.scene_processor(scene_string_data)
        
        # initialize current scene to starting scene
        self.current_scene = self.scenes['S']

    ##
    ##

    def file_processor(self, iterable: list, delimiter: str) -> list:
        """
        Processes a list into smaller sublists, separated by the delimiter.
        Parameters:
            iterable: The list of strings to be processed.
            delimiter: The string separating each sublist.
        Yields:
            yield_list: The sublists of strings separated by the delimiter.
        """
        # initializes an empty list to be yielded
        yield_list = []

        # appends elements until the delimiter or an empty space is found
        # once it is found, yield the current list and create a new one
        for val in iterable: 
            if val != delimiter and val != "":
                yield_list.append(val)
            else:
                yield yield_list
                yield_list = [] 

        # yields the final list
        
        yield yield_list

    ##
    ##

    def scene_processor(self, scene_string_data: str) -> dict:
        """
        This function processes a list of strings representing scenes.
        Parameters:
            scene_string_data: A string which is the name of the file containing scene information.
        Returns:
            scene_dict: A dictionary where the keys are scene ids and the values are the corresponding Scene instances.
        """
        # initializes scene_dict as an empty dictionary
        scene_dict = dict()
        
        # for every scene from the file processor, separated by "----"
        for scene in list(self.file_processor(scene_string_data, "----")):
            
            # checks that the scene is not null, an empty string, or a new line
            if scene not in [[""],[],["\n"]]:

                # splits the scene by "====" (list 1 has ID and description, list 2 has options)
                scene_split = list(self.file_processor(scene, "===="))


                # print(scene_split)
                # the id and description of the scene are found and assigned to variables
                scene_id = scene_split[0][0]
                description = "\n".join(scene_split[0][1:]) # join each element of the list on a new line
                
                # initializes options_dict as an empty dictionary
                options_dict = dict()

                # checks that length is greater than 0
                if len(scene_split[1]) > 0:
                    
                    # takes in the 2nd element of the scene_split list as the options
                    options_data = scene_split[1]
                    
                    # for each option
                    for choice in options_data:
                        
                        # if the data type of choice is not a string, a value error is raised
                        if type(choice) != str:
                            raise ValueError(f"{choice} is not a string")

                        # the first character is the option number
                        number = choice.split()
                        # print("number:",number)
                        number = number[0]

                        # check if the first item in that option is a number, if not raise an error
                        if list(number)[0].isdigit() == False:
                            raise ValueError(f"{number} is not a number")

                        # checks if the option has a requirement by checking "]"
                        # separates the requirement and the text/next scenes
                        if "]" in choice:
                            split_choice = choice.split("]")

                            requirement = split_choice[0][3:] + "]"
                            
                            text_and_next_scenes = split_choice[1].split()
                            
                        # otherwise, requirement is none and only extracts the text/next scenes
                        else:
                            requirement = None
                            text_and_next_scenes = choice[3:].split()

                        # creates two empty lists for next_scenes and option_description
                        # this is to separate text_and_next_scenes as defined above
                        next_scenes = []
                        option_description = []

                        # every item with "+" or "-" is added to next_scenes
                        # all other items are added to option_description
                        
                        for item in text_and_next_scenes:
                            if "+" in item or "-" in item:
                                next_scenes.append(item)
                            else:
                                option_description.append(item)

                        # adds spaces to convert the list of words in option_description into a string 
                        option_description = ' '.join(option_description)


                        # sorts the next scenes list (as ++, +, --, -)
                        next_scenes.sort()
                       
                        # moves the "--" to the last position, if not already there
                        if len(next_scenes) > 1:
                            if "--" in next_scenes[-2]:
                                temp_swap = next_scenes[-2]
                                next_scenes[-2] = next_scenes[-1]
                                next_scenes[-1] = temp_swap

                        # if there is no length, next_scenes is none
                        elif len(next_scenes) == 0:
                            next_scenes = None

                        # creates a new options objects with the extracted information
                        formatted_option = Option([number,requirement,option_description,next_scenes])
                        
                        # also adds it to the options dictionary
                        options_dict[int(number[:-1])] = formatted_option 

                # creates a new scene with the ID, description, and a dictionary of options
                scene_dict[scene_id] = Scene(scene_id, description, options_dict)

        # returns final scene dictionary
        return scene_dict

    ##
    ##

    def get_scene_id(self) -> str:
        """
        Returns the ID of the currently active scene.
        """
        return self.current_scene.get_ID()

    ##
    ##

    def show_current_scene(self) -> str:
        """
        Returns a string representation of the currently active scene.
        """
        scene_str = str(self.current_scene)
        return scene_str

    ##
    ##

    def select_option(self, option_number: int, override: int, character: Character = None) -> None:
        """
        Allows the user to select an option to progress the story, and updates current_scene based on the outcome.
        Parameters:
            option_number: An integer representing the option chosen, shown at the end of the scene.
            override: An optional variable used to override the random element in make_check of the character objects.
            character: An optional instance of Character, which is None by default.
                       This is used for the StoryBest class which inherits from Story.
        """

        # if no character is specified, character is set to the first character in self.characters
        if character == None:
            character = self.characters[0]

        
        # if current scene is the ending scene, stop and print the game over message
        if "E" in self.current_scene.ID:
            raise StopIteration("the game is over")

        # checks that the chosen option is in the list
        if option_number in self.current_scene.options:
            
            # obtains the chosen option using the list with the option number as the index
            chosen_option = self.current_scene.options[option_number]
            

            # if the option exists, obtain the option object's attribute and difficulty
            if chosen_option.attribute != None:
                skill_or_attribute_name = chosen_option.attribute
                difficulty = chosen_option.difficulty
            
            # if the option does not exist, the attribute is None and difficulty is 0
            else:
                skill_or_attribute_name = None
                difficulty = 0

            # if override provided is not an integer, set it to None
            if type(override) != int:
                override = None

            # obtains the outcome using the first character, as well as the attribute and difficulty obtained from options
            outcome = character.make_check(skill_or_attribute_name,difficulty,override)
            
            # declares scene ID
            scene_id = None

            # if there is only one next scene, get the scene ID by removing "+" and "-" characters
            if len(chosen_option.next_scenes) == 1:
                # ['+5'] >> 5
                scene_id = chosen_option.next_scenes[0].translate({43:None,45:None})
                
            # if there are multiple next scenes, get the sceneID 
            else:
                # for every scene, checks if the outcome is (+, -) or (++, --)
                for outcome_scene in chosen_option.next_scenes:
                    
                    # checks that the outcome is the same as the first character in outcome_scene
                    # if it is, value of scene_id is outcome_scene (excluding "+" and "-")
                    if outcome == outcome_scene[0] and outcome != outcome_scene[1]:
                        scene_id = outcome_scene.translate({43:None,45:None})

                    # checks that the outcome is the same as the first two characters in outcome_scene
                    # if it is, value of scene_id is outcome_scene (excluding "+" ahnd "-")
                    if outcome == outcome_scene[:2]:
                        scene_id = outcome_scene.translate({43:None,45:None})

                # if no scene id is assigned yet
                if scene_id == None and len(outcome) == 2:
                    # for every scene, checks if outcome[0] (+ or -) is in outcome_scene
                    # if it is, value of scene_id is outcome_scene (excluding "+" and "-")
                    # this is for when the outcome is ++ or -- but it is not found
                    # so the code looks for just + or -
                    for outcome_scene in chosen_option.next_scenes:
                       if outcome[0] in outcome_scene:
                           scene_id = outcome_scene.translate({43:None,45:None})
                           break

                # if no scene ID is assigned yet
                if scene_id == None:
                    
                    # if "+" is in the outcome, value of scene_id is the first character (excluding "+" and "-")
                    if "+" in outcome:
                        scene_id = chosen_option.next_scenes[0].translate({43:None,45:None})
                    # otherwise, value of scene_id is the final character (excluding "+" and "-")
                    else:
                        scene_id = chosen_option.next_scenes[-1].translate({43:None,45:None})

            # updates the current scene of story object with the scene ID obtained
            self.current_scene = self.scenes[scene_id]

    ##
    ##

    def __str__(self) -> str:
        """
        Returns a summary of the characters and scenes in the object as a string.
        """
        # story_str is initialised as ""
        story_str = ""

        # concatenates story_str with a header
        # and string representations of all Character objects in self.characters
        story_str += "CHARACTERS"
        for chara in self.characters:
            story_str += "\n" + str(chara)

        # concatenates story_str with a header
        # and string representations of all Scene objects in self.scenes
        story_str += "\nSCENES"
        for sceneid in self.scenes:
            scn = self.scenes[sceneid]
            story_str += "\n" + scn.get_scene_info()

        # string is returned
        return story_str


####
#### SCENE CLASS
####

class Scene:
    """ 
    A class used to represent each scene in a story.
    Attributes:
        ID: A single alphanumeric character representing the scene ID.
        description: A multiple-line description of the scenes.
        options: A dictionary of options where the scene ID is used as the key.
    """
    def __init__(self,scene_ID: str, scene_description: str, scene_options: dict) -> None:
        """
        This function instantiates the instance variables for the Scene class.
        Parameters:
            scene_ID: An alphanumeric character to be used as the scene ID.
            scene_description: A multiple-line description of the scenes.
            scene_options: A dictionary of scene options where scene ID is used as the key.
        """
        # checks if scene id is a string
        assert type(scene_ID) is str, 'scene ID must be a string' # check if the scene_ID paramater is a string
        self.ID = scene_ID

        # checks that scene_description is a string
        assert type(scene_description) is str, 'scene description must be a string' # check if the description is  string
        self.description = scene_description

        # check that scene_options is a dictionary
        assert type(scene_options) is dict, 'scene description must be a dictionary' # check if the option parameter is an dictionary
        self.options = scene_options

    ##
    ##

    def get_scene_info(self) -> str:
        """
        Returns the scene ID and options formatted as a string.
        """

        # adds ID to the string
        scene_info_str = self.ID + " >" 
        # adds each option to the string
        if self.options != None or len(self.options) != 0:
            for key in self.options:
                scene_info_str += " "
                scene_info_str += self.options[key].get_option_info()

        # returns the string
        return scene_info_str

    ##
    ##
    
    def get_ID(self) -> str:
        """
        Returns the ID of the current scene.
        """
        return self.ID
    
    ##
    ##
    
    def get_description(self) -> str:
        """
        Returns the description of the current scene.
        """
        return self.description
    
    ##
    ##
    
    def get_options(self) -> list:
        """
        Returns a list of options for the current scene.
        """
        return self.options
    
    ##
    ##
    
    def __str__(self) -> str:
        """
        Returns the scene class formatted as a string.
        """

        # declares the string to add options
        option_str = ""

        # if options are in the scene, formats the scene information with the ID, description, and options
        if self.options != None:
            for key in self.options:
                option_str += str(self.options[key]) + "\n"
            str_scene = "Scene " + self.ID + "\n" + self.description + "\n====\n" + option_str + "----"

        # otherwise, formats scene information with only ID and description
        else:
            str_scene = "Scene " + self.ID + "\n" + self.description + "\n====\n----"

        # returns the scene information
        return str_scene


####
#### OPTION CLASS
####

class Option:
    """
    The Option class represents a set of options for a given scene.

    Attributes:
        number (int): The option number.
        description (str): A short description of the option.
        next_scenes (list) : A list of the scenes following the option, depending on the outcome.
        attribute (str): The name of the attribute required to perform that option.
        difficulty (int): The value of the attribute required to perform that option.
    """

    def __init__(self, option_data: list) -> None:
        """
        This function instantiates the instance variables for the Option class.
        Parameters:
            option_data: A list of option information in the following format: 
            [number, [attribute difficulty], description, [next scenes]]
        """

        # initializes option number, excluding the "."
        self.number = int(option_data[0][:-1])

        # initializes description
        self.description = option_data[2]

        # initializes next scenes
        self.next_scenes = option_data[3]

        # checks if there is an attribute and difficulty
        if option_data[1] != None:
            
            # splits the difficulty and attribute into 2 strings
            difficulty_attribute = option_data[1][1:-1].split()
            
            # initializes attribute
            self.attribute = difficulty_attribute[0]
            
            # initializes difficulty
            self.difficulty = int(difficulty_attribute[1])

        # otherwise, sets default values for attribute and difficulty
        else:
            self.attribute = None
            self.difficulty = 0


    ##
    ##

    def get_option_info(self) -> str:
        """
        Returns the option information in the following format: [1. diplomacy10 +2 -1 --10]
        """
        
        # adds the opening bracket and the number, followed by a "."
        option_str = "[" + str(self.number) + "."
        
        # adds attribute and difficulty, if it exists
        if self.attribute != None:
            option_str +=  " " + self.attribute + str(self.difficulty)
        
        # adds the next scenes
        for scene in self.next_scenes:
            option_str += " " + scene

        # adds the closing bracket
        option_str += "]"
        
        # returns the string
        return option_str    
    
    ##
    ##

    def __str__(self) -> str:
        """
        Returns the option's number and description as a formatted string.
        """

        # format: "[number]. [description]"
        return str(self.number) + ". " + self.description
        
        
##
## 


if __name__ == "__main__":

    # imports the read_file function
    from choose_your_own_adventure import read_file 

    # creates a story using the sample files for the scenes and characters
    storyyy = Story(read_file("sample_chars.txt"),read_file("1053story.txt"))

    # prints the story
    print(storyyy)
    
