from participant import TrialParticipant
from filereader import FlankerFileReader

flanker_instructions = """
Welcome to the Flanker Task

In this task, you will be a string of 5 letters on the screen.
The aim is to respond to the MIDDLE letter only.

- If the middle letter is X or C -> Press the 'A' key
- If the middle letter is B or V -> Press the 'L' key

Scores will be tallied.
Once all rounds are completed, the task will end.

Press ENTER to continue
"""

flanker_consent = """
Consent Required

You are invited to take part in a short experiment.
In this task, you will respond to visual stimuli on the screen.
Your responses will be recorded but no personally identifying information will be stored.

Your participation is voluntary. You may withdraw from the experiment at any time.
By continuing, you confirm that you understand the instructions and agree to take part in the study.

Press ENTER to continue / Press n to quit
"""

response = input(flanker_consent)       # informs participants of their rights, in line with ethical considerations

if response.strip().lower() == 'n':
    print("\n"*3)
    print("Flanker Task terminated.")
    run_expr = False
    quit()                                  # if the response to the consent request is no, quit the program
else:
    print("Thank you for agreeing to take part in the study. The experiment will begin shortly....")
    print('\n'*5)
    char_in = input(flanker_instructions)     # if the participant agrees to consent, they are then shown the instructions for the game
    run_expr = True


flanker_participant = TrialParticipant()        # creates an instance of the Trial Participant object
flanker_participant.firstname = input("Enter your first name: ")
flanker_participant.lastname = input("Enter your last name: ")
print("\n"*50)          # clears the console for the game to run

run_expr = True
rounds_completed = 0

    # this outer loop continues until all rounds have been completed
while run_expr:

    words_remaining = True

        # this inner loop continues until all words in the current round have been presented
    while words_remaining: 
        flanker_participant.choose_key()        # selects a random key for this trial
        print('\n'*4)
        word = flanker_participant.get_word()       # retrieves the word for each specific round
        print(word)
        selection = input("Press 'a' or 'l': ").strip().lower()

        correct = flanker_participant.check_selection(selection)        # calls the check_selection method, taking the participant's answer as an argument
        print("Correct!" if correct else "Incorrect :(")

        words_remaining = flanker_participant.increment_wordpos()       # move to the next word
    
    rounds_completed = rounds_completed + 1

    # feature 1:
    if rounds_completed % 2 == 0 and rounds_completed < flanker_participant.get_round_count():
        change_words = input("\nWould you like to change the set of words? (y/n): ").strip().lower()

        if change_words == "y":
            print("Ok. Generating new word set...")

            # TrialParticipant uses FlankerFileReader - objects interaction
            new_stimuli = flanker_participant.file_reader.get_alternate_rounds()
            flanker_participant.change_stimuli(new_stimuli)
            print("Word set has been changed! Starting from round 1... \n")
            rounds_completed = 0
    
    # for my final project I aimed to tackle a problem I created in Assignment 1, hard-coding the number of rounds to 4
    # my idea was let TrialParticipant manage the internal state of the program and let main.py control the experiment flow.
    if rounds_completed >= flanker_participant.get_round_count():
        run_expr = False
        break

    # more rounds exist, safe to increment the round
    flanker_participant.increment_and_shuffle_round()


print("\n"*5)
print("Thank you for participating in the experiment!")
print("Task has completed.")
print("Flanker Task terminated.")
print(flanker_participant)