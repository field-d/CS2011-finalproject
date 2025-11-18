import random
from filereader import FlankerFileReader, FileReader

class TrialParticipant:

    instances_of_participants = 0

    def __init__(self):
        self.__first_name = ""
        self.__last_name = ""
        TrialParticipant.instances_of_participants += 1
        self.participant_num = TrialParticipant.instances_of_participants
        self.round = 1
        self.current_key = "a"
        self.word_pos = 0
        self.correct = 0
        self.incorrect = 0
        
        # for my final project, I decided to switch stimuli from a class variable to an instance variable
        # the reason for doing so is that it allows me to adjust the stimuli being shown for each instance of the flanker task, meaning different participants receive different stimuli
        # it also allows me to implement feature 1 of the final project
        self.file_reader = FlankerFileReader("rounds.txt")
        self.stimuli = self.file_reader.all_rounds()


        # feature 2: penalty system private instance variables to track answer streaks
        # these variables are private in order to encapsulate the penalty logic and prevent external modification
        self.__correct_streak = 0
        self.__incorrect_streak = 0
        self.__penalty_threshold = 3 # penalty is triggered after three incorrect answers in a row

    def __str__(self):
        """
        This is a string method for the Trial Participant class.

        The string method prints details about the participant including participant number, name (using properties) and their scores.
        """
        full_name = f"{self.firstname} {self.lastname}".strip()
        return (f"Participant: {self.participant_num} - {full_name}, Correct: {self.correct}, Incorrect: {self.incorrect}")  # string method for the Trial participant class includes name +
                                                                                                                                # results of the participant's round

    def increment_round(self):
        """
        ***The increment_ round method moves the game onto the next round once 6 words have been shown.*** REMOVED

        ***Each round it resets the word position, and once it reaches 4 rounds, it terminates the game.*** REMOVED

        Now, the number of rounds is determined by how many rounds there are in the file being read.

        For this Flanker Task, the stimuli are shuffeled once the round has been incremented. To achieve this I imported the random library and found the method shuffle in the documentation.

        Shuffle randomly reorders the elements of a list. It does not return a new list, it directly modifies the existing list by rearraging it's items into a new, random order. 
        
        This prevents learning effects from repeated sequences.
        """
        self.round = self.round + 1             # increment the round by 1 upon completion
        self.reset_wordpos()
        
        if self.round in self.stimuli:
            for key in self.stimuli[self.round]:
                random.shuffle(self.stimuli[self.round][key])
    
    def increment_wordpos(self):
        """
        The increment_wordpos method moves from word to word each trial.

        Returns True while there are words remaining in the round.
        Once it reaches 6 words per round, it resets to 0 and returns False.
        """
        self.word_pos += 1
        if self.word_pos >= 6:
            self.word_pos = 0
            return False
        return True

    def choose_key(self):
        """
        This method randomly selects the current key for the trial.

        Assumes the keys are always 'a' and 'l' (as per assginment). This ensures randomness in the presentation of stimuli.
        """
        self.current_key = random.choice(["a", "l"])            
        
    def get_key(self):
        """
        This method returns the current key ('a' or 'l') for the current round.
        """
        return self.current_key
    
    def check_selection(self, selection): 
        """
        This method checks if the answer the participant has given is correct or not.
        It does this by retrieving the word for the trial, getting the middle letter by indexing, and then comparing this letter to the correct letter for said word.

        Parameters: 
            selection - a string

        Returns:    
            True - if the answer was correct
            False - if the answer was inocrrect
        """
        word = self.get_word()
        middle_letter = word[len(word)//2]
        correct_key = "a" if middle_letter.lower() in ["x","c"] else "l"

        if selection.lower() == correct_key:
            self.increment_correct()
            # feature 2: tracking streaks
            self.__correct_streak += 1 
            self.__incorrect_streak = 0 # reset current streak on correct answer
            return True
        else:
            self.increment_incorrect()
            # feature 2: tracking streak and check for penalty
            self.__incorrect_streak += 1
            self.__correct_streak = 0 # reset current streak on incorrect answer
            
            if self.__incorrect_streak >= self.__penalty_threshold:
                self.apply_penalty()

            return False

    def increment_correct(self): 
        """
        This method increments a participant correct score by 1.
        """
        self.correct = self.correct +1      

    def increment_incorrect(self):
        """
        This method incrmements a participant's incorrect score by 1.
        """
        self.incorrect = self.incorrect +1  

    def reset_wordpos(self):
        """
        This method resets the position of the word to 0.
        """
        self.word_pos = 0
    
    def get_round(self):
        """
        This method returns dictionary of the stimuli for the current round.
        The dictionary contains two keys: 'a' and 'l', each containing a list of words for each round.
        """
        return self.stimuli[self.round]
    
    def get_word(self):
        """
        This method returns the current word for the current round and key.

        It uses self.current_key and self.word_pos to index into the stimuli tdictionary for the current round.
        """
        return self.stimuli[self.round][self.current_key][self.word_pos]
    
    def get_correct(self):
        """
        Returns the total number of correct responses the participant has achieved.
        """
        return self.correct
     
    def get_incorrect(self):
        """
        Returns the total number of incorrect responses the participant has "achieved".
        """
        return self.incorrect
    
    def get_round_count(self):
        """
        Returns the total number of rounds in the Flanker Task.
        """
        return len(self.stimuli)
    
    def set_first_name(self, first_name):
        """
        This method sets the participant's first name.

        Parameters:
            first_name (str) - The participant's first name.
        
        """
        self.__first_name = first_name

    def get_first_name(self):
        """
        This method returns the participant's first name.
        """
        return self.__first_name
    
    def set_last_name(self, last_name):
        """
        This method sets the participant's last name.

        Parameters:
            last_name (str) - The participant's last name.
        """
        self.__last_name = last_name
        
    def get_last_name(self):
        """
        This method returns the participant's last name
        """
        return self.__last_name
    
    
    def reset(self):
        """
        This method resets the participant's round and word position to the beginning.
        """
        self.round = 1
        self.word_pos = 0

        # properties with private name attributes
    firstname = property(get_first_name, set_first_name)
    lastname = property(get_last_name, set_last_name)

    def change_stimuli(self, new_stimuli: dict): 
        """
        This method is required by Feature 1 of the Final Project
        It changes the stimuli dictionary for each participant, resetting round and word positions to start fresh

        Parameters: 
            new_stimuli (dict) - new nested dictionary of stimuli
        """

        self.stimuli = new_stimuli
        self.reset()

        # feature 2: Reset streaks when stimuli is changed
        self.__incorrect_streak = 0
        self.__correct_streak = 0

    def apply_penalty(self):
        """
        Feature 2: Penalty system as a consequence of consecutive incorrect answers
        
        If a participant gets 3 incorrect answers in a row, they are penalised by:
        - Moving back one round (if not on round 1)
        - or restarting current round if on round 1

        This method demonstrates:
        - Code reuse: uses existing methods (reset_wordpos, shfuffle logic) and instance variables (self.round, self.stimuli) rather than duplicating code
        - Methods: encapsulates penalty logic in a separate method 
        - Private Variables: uses __incorect_streak and __penalty_threshold to prevent external modification
        
        The penalty system encourages focus and attention during the experiment
        """

        if self.round > 1:
            print(f"\nPENALTY TRIGGERED: {self.__penalty_threshold} incorrect answers in a row!")
            print(f"Moving back from round {self.round} to round {self.round - 1}\n")
            self.round = self.round - 1
            self.reset_wordpos()
            self.__incorrect_streak = 0

            for key in self.stimuli[self.round]:
                random.shuffle(self.stimuli[self.round][key])

        else:

            print(f"\nPENALTY TRIGGERED: {self.__penalty_threshold} incorrect answers in a row!")
            print("Restarting Round 1")
            self.reset_wordpos()
            self.__incorrect_streak = 0

            for key in self.stimuli[self.round]:
                random.shuffle(self.stimuli[self.round][key])
