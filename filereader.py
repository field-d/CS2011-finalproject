import random

class FileReader:

    # constructor for the FileReader class
    # takes filename as a parameter
    def __init__(self, filename):
        self.__filename = None
        self.set_filename(filename)
        print("instance of FileReader class created!")
    
    def read_all(self):
        try:
            file_1 = open(self.__filename)
            lines = file_1.readlines()
            file_1.close()
            return lines
        except:
            print("file not opened. Terminating method")
            return False

    def line_count(self):
        lines = self.read_all()
        line_amount = len(lines)
        return line_amount   

    def get_filename(self):
        return self.__filename

    def set_filename(self, new_filename):
        if type(new_filename) == str:
            self.__filename = new_filename 

    
class FlankerFileReader(FileReader):
    
    def __init__(self, filename):
        """
        Constructor for FlankerFileReader class.
        It initialises the object by first calling the parent class constructor using super(), ensuring that the filename is 
        properly validated and stored through FileReader's encapsulation.
        
        The design uses good OOP practice by reusing initialisation logic from the parent class rather than overwriting it, 
        maintaining consistency and reducing redudancy.
        """

        super().__init__(filename)
        self.stimuli = {}
        self.round_num_list = []

    def read_all(self):
        lines = super().read_all()

        if not lines:
            print("Warning: File is empty or could not be read.")
            return []
        
        valid_lines = []
        for line in lines:
            if line.strip() and ',' in line:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    valid_lines.append(line)
                else:
                    print(f"Warning: Skipped invalid line: {line.strip()}")

        return valid_lines    

    def __str__(self):
        """
        Returns a formateed string representation of the current FlankerFileReader object.
        Includes the filename and a short description of the subclass's purpose.

        This method supports debugging, and its design allows for __str__ to provide human-readable information about objects.
        """

        description = "This class builds upon it's Parent Class FileReader by creating a subclass called FlankerFileReader.\n" \
        "This class accesses a file designed to run a Flanker Task Experiment"
        return f"File Read: {self.get_filename()}\nDescription: {description}"
    
    def all_rounds(self):
        """
        This method reads the entire contents from the file provided. It calls the parent method read_all() which opens the file, 
        saves it's contents to a varaiable lines and then closes the file.
        The method then cleans the file, assigns keys and values based on the assumption of the structure of the file.
        """
        
        if self.line_count() == 0:
            print("The file is empty!")
            return {}
        
        lines = self.read_all()

        if not lines:
            return {}
        
        for line in lines:
            clean_lines = line.strip().split(",")
            key = int(clean_lines[0])
            inner_key = clean_lines[1]
            values = clean_lines[2:]

            if key not in self.stimuli:
                self.stimuli[key] = {}
            
            self.stimuli[key][inner_key] = values

        return self.stimuli

    def get_rounds_at(self, round_num_list : list):
        """
        This method retrieves and returns the specified rounds from the stimuli, with their keys renumbered starting at 1. 
        
        Parameters: round_num_list (list of integers) - a list of ints representing the round numbers to extract from the stimuli.
        Returns: A dictionary temp_dict that includes only these rounds, but their keys are reindexed to begin at 1 and are incremented, regardless of their round numbers originally.

        This design ensures that the returned dictionary follows the requirements to always start at round 1, even if the requested rounds are later in the experiment.
        This implementation uses a manual counter for clarity
        """
        
       # Ensures the entire stimuli has been loaded before access
        if not self.stimuli:
            self.all_rounds()

        # if the list is empty, return an empty dictionary to ensure return types are consistent
        if len(round_num_list) < 1:
            return {}
        
        # temp_dict will store only the request rounds
        temp_dict = {}
        temp_key = 1 

        # iterate through each requested round number
        for round_number in round_num_list:
            # since the stimuli dictionary keys are strings
            temp_dict[temp_key] = self.stimuli[round_number]
            temp_key = temp_key + 1 # increment the round counter for reindexing

        # return the reindexed dictionary
        return temp_dict

    def get_round_range(self, round_range : list):
        """
        This method retreives rounds within a specific, inclusive range (start and end values).
        Includes a validation system with erorr handling for incorrect types, invalid order, and out of bound rounds.

        This method validates all input before processing, improving reliability. The reindexing of rounds from 1 onwards ensures the method remainds comptaible
        with other dictionary outputs in the class.
        """
        if not self.stimuli:
            self.all_rounds()

        if not type(round_range) == list:
            print("An error occured. round_range must be a list")
            return 
        
        if len(round_range) != 2:
            print("An error occured. round_range must be of length 2")
            return

        if type(round_range[0]) != int or type(round_range[1]) != int:
            print("An error occured. Elements of round_range must be of type int")
            return
        
        if round_range[0] > round_range[1]:
            print("Invalid range. Start range must be smaller than the end")
            return
        
        if round_range[0] < 0 or round_range[1] < 0:
            print("An error occured. Range cannot be negative numbers")
            return
        
        max_round = len(self.stimuli)

        if round_range[0] > max_round or round_range[1] > max_round:
            print("An error occured. Invalid range")
            return
        
        temp_dict = {}
        temp_key = 1

        for round_num in range(round_range[0], round_range[1] + 1):
            # converting the round number to string in order to match the dictionary format
            temp_dict[temp_key] = self.stimuli[round_num]
            temp_key = temp_key + 1
            
        return temp_dict

    def random_rounds(self):
        """
        THis method selects and returns a random, inclusive range of rounds from the file as a nested dictionary. THe range boundaires are generated using Python's
        random module within valid round limits.
        
        This method builds upon the existing stimuli structure that is produced by all_rounds(), reinforcing data reuse rather than re-reading the file unnecesarrily.
        Ensures randomisation is encapsulated.
        """

        if not self.stimuli:
            self.all_rounds()

        max_round = len(self.stimuli)

        # ensuring the start value can never be the last value
        if max_round > 1:
            start = random.randint(1, max_round - 1) # changed from max_round to max_round - 1
        else:
            start = 1 # edge case: if only 1 round exists
        end = random.randint(start, max_round)

        temp_dict = {}
        temp_key = 1

        for round in range(start, end + 1):
            temp_dict[temp_key] = self.stimuli[round]
            temp_key = temp_key + 1

        return temp_dict

    def exclude_rounds_at(self, round_num_list : list):
        """
        Returns a nested dictionary excluding specific rounds provided in a list.
        
        This method encourages reuse and its design preserves dictionary structure and maintaining renumbers keys starting from 1 for consistency.
        """

        if not self.stimuli:
            self.all_rounds()

        if type(round_num_list) != list or len(round_num_list) < 1: 
            print("An error occured. List length must be greater than 1")
            return 

        for i in round_num_list:
            if type(i) != int:
                print("Elements must be ints!")
                return
            
        temp_dict = {}
        temp_key = 1

        for round_num in self.stimuli.keys():
            if round_num not in round_num_list:
                temp_dict[temp_key] = self.stimuli[round_num]
                temp_key = temp_key + 1

        return temp_dict

    def exclude_round_range(self, round_range : list):
        """
        This method returns all rounds except those within the specified inclusive range.
        
        This method includes full validation for range, type and existence. 
        This method maintains renumbered keys and consistent output for predictability. 
        """
        if not self.stimuli:
            self.all_rounds()

        if type(round_range) != list or len(round_range) != 2:
            print("An error occured. List must be of length 2.")
            return
        
        if type(round_range[0]) != int or type(round_range[1]) != int:
            print("An error occured. Elements must be of type int.")
            return
        
        if round_range[0] not in self.stimuli or round_range[1] not in self.stimuli:
            print("An error occured. Rounds do not exist.")
            return

        temp_dict = {}
        temp_key = 1

        for round_num in self.stimuli.keys():
            if round_num < round_range[0] or round_num > round_range[1]:
                temp_dict[temp_key] = self.stimuli[round_num]
                temp_key = temp_key + 1

        return temp_dict
    
    def get_alternate_rounds(self):
        """
        Returns an alternate set of rounds
        This method demonstrated method overriding by crearting a variation of all_rounds()
        """

        if not self.stimuli:
            self.all_rounds()

        temp_dict = {}
        temp_key = 1

        # get rounds in the reverse order
        for round_num in sorted(self.stimuli.keys(), reverse=True):
            temp_dict[temp_key] = self.stimuli[round_num].copy()
            temp_key = temp_key + 1

        return temp_dict


if __name__ == "__main__":
    file_1 = FlankerFileReader("rounds.txt")
    file_1.all_rounds()
    print(file_1.stimuli)
