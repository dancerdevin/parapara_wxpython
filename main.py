# Press Shift+F10 to execute code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# The basic components of Paradigms & Parameters are Arcs, Paradigms, Parameters, and Log Entries.
# An Arc is a set that contains all other sets. A new Arc can have different Paradigms, Parameters, etc.
# A Paradigm has a name, a description, associated default parameters, associated quests, level, and XP/progress.
# A Parameter has a name, a description, a level, and XP/progress.
# A Log Entry has a name, tagged paradigms, a significance modifier (routine/notable/major/miraculous), parameter values
# (which default to the tagged paradigms' values multiplied by the significance modifier), and entry text.
# The core functions will be: 1) create/edit arc, 2) c/e paradigm, 3) c/e parameter, 4) c/e log entry.
# Optional functions could be: 1) daily decay on/off, 2) repeatable tasks as stock Log Entries.
# I may also want to distinguish between General and Specific Quests, or define completion criteria for the former type.
# Once I get the core functions down, I'll try to learn about GUI for displaying meters, buttons, and pop up explainers.
import csv
import os.path
from datetime import datetime


class Arc:
    def __init__(self):
        self.name = ""
        self.paradigms = []
        self.parameters = []
        self.log_entries = []


class Paradigm:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.default_parameters = []
        self.quests = []
        self.level = 1
        self.xp = 0
        self.total_xp = 0
        self.xp_limit = self.level * 25


class Parameter:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.level = 10
        self.xp = 0
        self.total_xp = 0
        self.xp_limit = self.level * 5


class LogEntry:
    def __init__(self):
        id = 0
        name = ""
        date = None
        tagged_paradigms = []
        significance_modifier = 0
        parameter_values = {}
        entry_text = ""


# def initial_startup:
#     print("Welcome to Paradigms & Parameters. Now preparing the chronicle of your adventures...")
#     # Instantiate the first arc.
#     new_arc = Arc()
#     new_arc.name = input("What will this arc of your journeys be called?")
#     # Instantiate paradigms.
#     creating_paradigms = True
#     while creating_paradigms:
#         print("")

# Skipping to defining my current arc.
weekend_fairy = Arc()
# Defining my paradigms.
adventurer = Paradigm()
knight = Paradigm()
sage = Paradigm()
dancer = Paradigm()
homemaker = Paradigm()
logician = Paradigm()
storyteller = Paradigm()
fairy = Paradigm()
# Defining my parameters.
condition = Parameter()
community = Parameter()
diligence = Parameter()
memory = Parameter()
vivacity = Parameter()
transcendence = Parameter()
# Defining the specifics of each parameter first (since paradigms have default parameters).
condition.name = "Condition"
condition.description = "Physical strength, flexibility, and resilience; pain management."
community.name = "Community"
community.description = "Old friendships and new acquaintances nurtured and fostered."
diligence.name = "Diligence"
diligence.description = "Conscientiousness, consistency, and composure."
memory.name = "Memory"
memory.description = "Retention, narrative, and the distinctness of days."
vivacity.name = "Vivacity"
vivacity.description = "Presence, passion, charisma and confidence."
transcendence.name = "Transcendence"
transcendence.description = "Otherness and acceptance thereof."
# Defining the specifics of each paradigm.
adventurer.name = "Adventurer"
adventurer.description = "STORGE: Habits and virtues, one step further."
adventurer.default_parameters = {condition: 1, community: 1, transcendence: 1}
adventurer.quests = ["Maintain and renew dormant friendships", "Strengthen hips and knees", "Donate blood alone"]
knight.name = "Knight"
knight.description = "PHILIA: Passion and duty, loyalty and persistence."
knight.default_parameters = {diligence: 1, memory: 1}
knight.quests = ["Learn Django and create ParaPara", "Learn JavaScript and create a RPGMaker Script",
                 "Begin Russian with flashcards and basics"]
dancer.name = "Dancer"
dancer.description = "EROS: Liberation through opacity. Meaning without knowing."
dancer.default_parameters = {vivacity: 1, condition: 1}
dancer.quests = ["Return to masked dancing with different fabulous outfits", "10 Insta mutuals from dancing",
                 "Attend new afterhours"]
sage.name = "Sage"
sage.description = "AGAPE: Liberation through clarity. From knowing, meaning."
sage.default_parameters = {vivacity: 1, memory: 1}
sage.quests = ["Create first Ethics for the Depressed video essay",
               "Set up regular philosophy virtual discussion", "Read 5 histories of philosophy"]
homemaker.name = "Homemaker"
homemaker.description = "LUDUS: Knight/Dancer. Loving husband."
homemaker.default_parameters = {vivacity: 1, diligence: 1}
homemaker.quests = ["Incorporate cat care into cleaning routine", "Learn to cook channa masala",
                    "Rototiller the backyard or some equivalent"]
logician.name = "Logician"
logician.description = "PRAGMA: Knight/Sage. Academic philosopher."
logician.default_parameters = {community: 1, diligence: 1}
logician.quests = ["Break through and submit Crit Phen of Value paper",
                   "Finish and submit Existential Feelings and Quasi-Beliefs papers", "Book proposal in 2023"]
storyteller.name = "Storyteller"
storyteller.description = "PHILAUTIA: Sage/Dancer. Creative writer."
storyteller.default_parameters = {memory: 1, community: 1}
storyteller.quests = ["Arrange Cosmos Cup for SCSMUSH",
                      "Read 10 new novels",
                      "Watch 10 new movies on the Criterion Channel"]
fairy.name = "Fairy"
fairy.description = "MANIA: Sublime oblivion, beyond direction."
fairy.default_parameters = {transcendence: 2, condition: 1}
fairy.quests = ["Fabulous queer moment on the dance floor", "Fabulous queer moment at Conduit Coffee",
                "Fabulous queer moment at home"]

weekend_fairy.paradigms = [adventurer, knight, sage, dancer, homemaker, logician, storyteller, fairy]
weekend_fairy.parameters = [condition, community, diligence, memory, vivacity, transcendence]


def create_my_arc(parameters, paradigms):
    with open('weekend_fairy_stats.csv', 'w', newline='') as csvfile:
        fairy_writer = csv.writer(csvfile, delimiter='|')
        # First, give them column names, so maybe reading the file is easier.
        # fairy_writer.writerow(["Name"] + ["Description"] + ["Level"] + ["XP"] + ["Next Level"] + ["Total XP"] +
        #                       ["Default Parameters"] + ["Quests"])
        print("PARAMETERS")
        for parameter in parameters:
            parameter_text = parameter.name + ": " + str(parameter.level) + " (" + str(parameter.xp) + "/" + str(
                parameter.xp_limit) + ")"
            print(parameter_text)
            fairy_writer.writerow(
                [parameter.name] + [parameter.description] + [str(parameter.level)] + [str(parameter.xp)] +
                [str(parameter.xp_limit)] + [str(parameter.total_xp)])
        print("PARADIGMS")
        for paradigm in paradigms:
            paradigm_text = paradigm.name + ": " + str(paradigm.level) + " (" + str(paradigm.xp) + "/" + str(
                paradigm.xp_limit) + ")"
            print(paradigm_text)
            # Unpack the dictionary of default parameters: try turning each into a string like everything else
            default_parameters_list = []
            for key, value in paradigm.default_parameters.items():
                default_parameter_string = str(key.name) + " +" + str(value)
                default_parameters_list.append(default_parameter_string)
            fairy_writer.writerow(
                [paradigm.name] + [paradigm.description] + [str(paradigm.level)] + [str(paradigm.xp)] +
                [str(paradigm.xp_limit)] + [str(paradigm.total_xp)] + [default_parameters_list] +
                [paradigm.quests])


# This generates the CSV file for my specific arc at its starting point if the CSV stats file does not already exist.
just_created = False
if not os.path.exists('weekend_fairy_stats.csv'):
    print("The Weekend Fairy is born!")
    create_my_arc(weekend_fairy.parameters, weekend_fairy.paradigms)
    just_created = True
# Now that I have the basics down, I'll make logentry.py to modify main.py. For my purposes, I won't run this twice.
# But if I expand on the program to make it usable by others, or to make multiple arcs, this structure may help.
