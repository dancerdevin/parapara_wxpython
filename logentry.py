import main
import csv
from datetime import datetime

# I've successfully defined my classes and written to CSV in main.py. Now I'll edit a preexisting CSV file.
# I'll open the CSV file, add a log entry, modify the parameter/paradigm values based on position, and print.
# Then I can think about how to read log entries (I'll probably want a GUI for that, even just for me).

# First, instantiate a reader object to print current stats (if you haven't just seen them thanks to main.py).
def stat_reader(all_stats):
    # I've set up the reader object as part of a function that prepares the object to be read by log_entry.
    # Set the stat with a name that matches the first column to the level, XP, etc., read off of the CSV file.
    with open('weekend_fairy_stats.csv', newline='') as stats_csv:
        fairy_reader = csv.reader(stats_csv, delimiter='|')
        for row in fairy_reader:
            for stat in all_stats:
                if row[0] == stat.name:
                    stat.level = int(row[2])
                    stat.xp = int(row[3])
                    stat.xp_limit = int(row[4])
                    stat.total_xp = int(row[5])
        return all_stats


def gui_log_reader(counter):
    # This is a function to display all log entries on Panel Three, assuming an ever-increasing amount of entries.
    # Display 10 rows in static text. Use "Next Page" and "Previous Page" buttons to cycle through those 10 rows.
    # Let's try to display the most recent ones. I'll add every entry to a big list.
    all_log_entries = []
    with open('weekend_fairy_logs.csv', newline='') as logs_csv:
        fairy_reader = csv.reader(logs_csv, delimiter='|')
        for row in fairy_reader:
            all_log_entries.append(row)
    # Determine the number of elements in the list.
    num_log_entries = len(all_log_entries)
    # Create a list of the 10 most recent entries.
    entries_to_display = []
    max_counter = counter + 9
    min_counter = 1
    # Let's make sure that max_counter can't go higher than the total number of log entries.
    # Otherwise, the while loop will try to access an index that doesn't exist.
    if max_counter > num_log_entries:
        max_counter = num_log_entries
        counter = max_counter - 10
    if counter < min_counter:
        counter = min_counter
    while counter <= max_counter:
        entries_to_display.append(all_log_entries[num_log_entries-counter])
        counter += 1
    # It works! In wxpython: populate StaticText box by iterating through entries_to_display.
    # I'll want to return the counter as well, so we don't lose our place when flipping through "pages."
    return entries_to_display, counter, num_log_entries


def log_printer(all_stats, print_bool, log_entry_bool, gui_bool):
    # I've adapted part of create_my_arc()'s log-writing function to just print the log without writing to it.
    # Use this function after stat_reader updates the values in all_stats to be current.
    updated_weekend_fairy = main.Arc()
    for stat in all_stats:
        if isinstance(stat, main.Parameter):
            updated_weekend_fairy.parameters.append(stat)
        elif isinstance(stat, main.Paradigm):
            updated_weekend_fairy.paradigms.append(stat)
    if print_bool:
        print("PARAMETERS")
        for parameter in updated_weekend_fairy.parameters:
            parameter_text = parameter.name + ": " + str(parameter.level) + " (" + str(parameter.xp) + "/" + str(
                parameter.xp_limit) + ")"
            print(parameter_text)
        print("PARADIGMS")
        for paradigm in updated_weekend_fairy.paradigms:
            paradigm_text = paradigm.name + ": " + str(paradigm.level) + " (" + str(paradigm.xp) + "/" + str(
                paradigm.xp_limit) + ")"
            print(paradigm_text)
    # If you want to write to the log, too, set log_entry_bool to True, and this function will return the Arc object.
    if log_entry_bool:
        return updated_weekend_fairy
    # If I want the GUI to print this information instead, I'll pass it one big string without printing anything.
    if gui_bool:
        stats_string = ""
        stats_string += "PARAMETERS\n"
        for parameter in updated_weekend_fairy.parameters:
            parameter_text = parameter.name + ": " + str(parameter.level) + " (" + str(parameter.xp) + "/" + str(
                parameter.xp_limit) + ")\n"
            stats_string += parameter_text
        stats_string += "\nPARADIGMS\n"
        for paradigm in updated_weekend_fairy.paradigms:
            paradigm_text = paradigm.name + ": " + str(paradigm.level) + " (" + str(paradigm.xp) + "/" + str(
                paradigm.xp_limit) + ")\n"
            stats_string += paradigm_text
        return stats_string


def log_entry():
    # Begin by scraping all data from stats.CSV with the stat_reader function.
    all_stats = main.weekend_fairy.parameters + main.weekend_fairy.paradigms
    stat_reader(all_stats)
    # If you just created the Arc, you'll already have printed the stats. If not, print them. (Avoids redundancy.)
    if not main.just_created:
        print("Welcome back, Weekend Fairy. Here is your progress so far.")
        log_printer(all_stats, print_bool=True, log_entry_bool=False, gui_bool=False)
    # Now, create a log entry object.
    log_entry = main.LogEntry()
    print("Creating new log entry.")
    log_entry.name = input("Entry name: ")
    log_entry.entry_text = input("Entry text: ")
    entry_paradigms = input("Tag relevant paradigms, separated by commas: ")
    # Connect this inputted text with the paradigm objects.
    actual_paradigms = []
    split_entry_paradigms = entry_paradigms.split(",")
    for paradigm_text in split_entry_paradigms:
        stripped_paradigm = paradigm_text.strip(" ")
        for paradigm_object in main.weekend_fairy.paradigms:
            if stripped_paradigm.lower() == paradigm_object.name.lower():
                actual_paradigms.append(paradigm_object)
    # Let's ask for a significance modifier, then adjust the defaults accordingly. Overriding the defaults can come later.
    entry_sig_mod = int(
        input("Please input a significance rating (0 = Routine, 1 = Minor, 2 = Notable, 3 = Major, 4 = Miraculous): "))
    multiplier = 0
    if entry_sig_mod == 0:
        multiplier = 1
    elif entry_sig_mod == 1:
        multiplier = 3
    elif entry_sig_mod == 2:
        multiplier = 7
    elif entry_sig_mod == 3:
        multiplier = 15
    elif entry_sig_mod == 4:
        multiplier = 40
    else:
        print("Error. Not a recognized integer.")
        exit()
    # Multiply the default parameters by the significance modifier's multiplier.
    xp_gain = {}
    for paradigm in actual_paradigms:
        for key, value in paradigm.default_parameters.items():
            # If multiple paradigms modify the same parameter, increment the XP gain accordingly.
            try:
                xp_gain[key.name] += int(value) * multiplier
            except KeyError:
                xp_gain[key.name] = int(value) * multiplier
        # Now we have the parameter that's gaining XP and XP gained. Let's do the same for the paradigms themselves.
        # There shouldn't be multiple instances of the same Paradigm, though, right? Well, this can't hurt, for now.
        try:
            xp_gain[paradigm.name] += multiplier
        except KeyError:
            xp_gain[paradigm.name] = multiplier
    print(xp_gain)
    # Append the log entry object components to the log CSV file.
    with open('weekend_fairy_logs.csv', 'a', newline='') as logs_csv:
        fairy_logger = csv.writer(logs_csv, delimiter='|')
        fairy_logger.writerow([log_entry.name] + [xp_gain] + [log_entry.entry_text])
    # Modify the stats in the stats CSV file according to XP gain. Increment total XP, etc., and check for level ups.
    # Recall that I'm currently separating variables by "|" to avoid splitting on commas in, e.g., descriptions.
    # Let's try this: see if the name (text before first split) matches any key in xp_gain.
    # EUGENE'S ADVICE: Just read the stats file, change the values, and overwrite with all the same information,
    # rather than trying to fish for specific indices in a fucking CSV file (that I probably shouldn't be using anyway).
    # Use stat_reader to connect the inputted strings with actual paradigm/parameter objects.
    all_stats = stat_reader(all_stats)
    # Now, let's check for a level up and increment the values.
    for key, value in xp_gain.items():
        for stat in all_stats:
            # Match the name in XP_Gain with the name in all_stats.
            if stat.name == key:
                # Increment total XP.
                stat.total_xp += value
                # Check for level up.
                if stat.xp + value >= stat.xp_limit:
                    # This is a level up.
                    stat.xp += value
                    # Do a "while" loop to allow for multiple level ups at once.
                    while stat.xp >= stat.xp_limit:
                        stat.level += 1
                        print("Congratulations! " + stat.name + " is now Level " + str(stat.level) + "!")
                        # Set XP progress back to 0 plus any excess over the XP needed for the level up.
                        stat.xp = 0 + (stat.xp - stat.xp_limit)
                        # Set the new XP Limit depending on if the stat is a Paradigm or a Parameter.
                        if isinstance(stat, main.Paradigm):
                            stat.xp_limit = stat.level * 25
                        elif isinstance(stat, main.Parameter):
                            stat.xp_limit = stat.level * 5
                        else:
                            # Just in case this breaks somewhere.
                            print("Error: " + stat.name + " is neither a Paradigm nor a Parameter.")
                            exit()
                # This is not a level up, so just increment the XP, too.
                else:
                    stat.xp += value
    # Now that all the stats (Paradigms and Parameters) have been modified, let's write them to a new CSV file.
    # Let's split all_stats back into paradigms and parameters, and then run my overwrite function from before!
    updated_weekend_fairy = log_printer(all_stats, print_bool=False, log_entry_bool=True, gui_bool=False)
    main.create_my_arc(updated_weekend_fairy.parameters, updated_weekend_fairy.paradigms)


def gui_log_entry(entry_name, entry_text, entry_paradigms, entry_sig_mod, entry_parameter=""):
    # For now, to get the GUI off the ground, I'm just copying and tweaking the previous function, to not break it.
    # Begin by scraping all data from stats.CSV with the stat_reader function.
    all_stats = main.weekend_fairy.parameters + main.weekend_fairy.paradigms
    stat_reader(all_stats)
    # If you just created the Arc, you'll already have printed the stats. If not, print them. (Avoids redundancy.)
    # if not main.just_created:
    #     print("Welcome back, Weekend Fairy. Here is your progress so far.")
    #     log_printer(all_stats, print_bool=True, log_entry_bool=False, gui_bool=False)
    # Now, create a log entry object.
    log_entry = main.LogEntry()
    # print("Creating new log entry.")
    # log_entry.name = input("Entry name: ")
    # log_entry.entry_text = input("Entry text: ")
    # entry_paradigms = input("Tag relevant paradigms, separated by commas: ")
    # Connect this inputted text with the paradigm objects.
    all_log_entries = []
    with open('weekend_fairy_logs.csv', newline='') as logs_csv:
        fairy_reader = csv.reader(logs_csv, delimiter='|')
        for row in fairy_reader:
            all_log_entries.append(row)
    # Determine the number of elements in the list.
    num_log_entries = len(all_log_entries)
    log_entry.id = num_log_entries+1
    log_entry.name = entry_name
    log_entry.date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    log_entry.entry_text = entry_text
    actual_paradigms = []
    split_entry_paradigms = entry_paradigms.split(",")
    for paradigm_text in split_entry_paradigms:
        stripped_paradigm = paradigm_text.strip(" ")
        for paradigm_object in main.weekend_fairy.paradigms:
            if stripped_paradigm.lower() == paradigm_object.name.lower():
                actual_paradigms.append(paradigm_object)
    # Let's ask for a significance modifier, then adjust the defaults accordingly. Overriding the defaults can come later.
    # entry_sig_mod = int(
    #     input("Please input a significance rating (0 = Routine, 1 = Minor, 2 = Notable, 3 = Major, 4 = Miraculous): "))
    # entry_sig_mod = 0
    multiplier = 0
    if entry_sig_mod == 0:
        multiplier = 1
    elif entry_sig_mod == 1:
        multiplier = 3
    elif entry_sig_mod == 2:
        multiplier = 7
    elif entry_sig_mod == 3:
        multiplier = 15
    elif entry_sig_mod == 4:
        multiplier = 40
    else:
        print("Error. Not a recognized integer.")
        exit()
    # Multiply the default parameters by the significance modifier's multiplier.
    xp_gain = {}
    # If there's a parameter override, set the parameter XP based on the override, not the paradigms.
    if entry_parameter:
        actual_parameters = []
        split_entry_parameter = entry_parameter.split(",")
        for entry in split_entry_parameter:
            stripped_entry = entry.strip(" ")
            split_on_colon = stripped_entry.split(":")
            for parameter_object in main.weekend_fairy.parameters:
                if split_on_colon[0].lower() == parameter_object.name.lower():
                    actual_parameters.append({parameter_object: int(split_on_colon[1])})
        for parameter_dict in actual_parameters:
            for key, value in parameter_dict.items():
                try:
                    xp_gain[key.name] += value
                except KeyError:
                    xp_gain[key.name] = value
        # Also, add paradigm XP (just not to parameters based on default parameters, as in the else statement).
        for paradigm in actual_paradigms:
            try:
                xp_gain[paradigm.name] += multiplier
            except KeyError:
                xp_gain[paradigm.name] = multiplier
    else:
        for paradigm in actual_paradigms:
            for key, value in paradigm.default_parameters.items():
                # If multiple paradigms modify the same parameter, increment the XP gain accordingly.
                try:
                    xp_gain[key.name] += int(value) * multiplier
                except KeyError:
                    xp_gain[key.name] = int(value) * multiplier
            # Now we have the parameter that's gaining XP and XP gained. Let's do the same for the paradigms themselves.
            # There shouldn't be multiple instances of the same Paradigm, though, right? Well, this can't hurt, for now.
            try:
                xp_gain[paradigm.name] += multiplier
            except KeyError:
                xp_gain[paradigm.name] = multiplier
    # print(xp_gain)
    # Append the log entry object components to the log CSV file.
    with open('weekend_fairy_logs.csv', 'a', newline='') as logs_csv:
        fairy_logger = csv.writer(logs_csv, delimiter='|')
        fairy_logger.writerow([log_entry.id] + [log_entry.name] + [log_entry.date] + [xp_gain] + [log_entry.entry_text])
    # Modify the stats in the stats CSV file according to XP gain. Increment total XP, etc., and check for level ups.
    # Recall that I'm currently separating variables by "|" to avoid splitting on commas in, e.g., descriptions.
    # Let's try this: see if the name (text before first split) matches any key in xp_gain.
    # EUGENE'S ADVICE: Just read the stats file, change the values, and overwrite with all the same information,
    # rather than trying to fish for specific indices in a fucking CSV file (that I probably shouldn't be using anyway).
    # Use stat_reader to connect the inputted strings with actual paradigm/parameter objects.
    all_stats = stat_reader(all_stats)
    # Now, let's check for a level up and increment the values.
    for key, value in xp_gain.items():
        for stat in all_stats:
            # Match the name in XP_Gain with the name in all_stats.
            if stat.name == key:
                # Increment total XP.
                stat.total_xp += value
                # Check for level up.
                if stat.xp + value >= stat.xp_limit:
                    # This is a level up.
                    stat.xp += value
                    # Do a "while" loop to allow for multiple level ups at once.
                    while stat.xp >= stat.xp_limit:
                        stat.level += 1
                        print("Congratulations! " + stat.name + " is now Level " + str(stat.level) + "!")
                        # Set XP progress back to 0 plus any excess over the XP needed for the level up.
                        stat.xp = 0 + (stat.xp - stat.xp_limit)
                        # Set the new XP Limit depending on if the stat is a Paradigm or a Parameter.
                        if isinstance(stat, main.Paradigm):
                            stat.xp_limit = stat.level * 25
                        elif isinstance(stat, main.Parameter):
                            stat.xp_limit = stat.level * 5
                        else:
                            # Just in case this breaks somewhere.
                            print("Error: " + stat.name + " is neither a Paradigm nor a Parameter.")
                            exit()
                # This is not a level up, so just increment the XP, too.
                else:
                    stat.xp += value
    # Now that all the stats (Paradigms and Parameters) have been modified, let's write them to a new CSV file.
    # Let's split all_stats back into paradigms and parameters, and then run my overwrite function from before!
    updated_weekend_fairy = log_printer(all_stats, print_bool=False, log_entry_bool=True, gui_bool=False)
    main.create_my_arc(updated_weekend_fairy.parameters, updated_weekend_fairy.paradigms)
    return log_entry.id

def mission_level_up(xp_gain, all_stats):
    updated_stats = all_stats
    for key, value in xp_gain.items():
        for stat in updated_stats:
            # Match the name in XP_Gain with the name in all_stats.
            if stat.name == key:
                # Increment total XP.
                print("Stat before total xp increase: " + str(stat.total_xp))
                stat.total_xp += value
                print("Stat after total xp increase: " + str(stat.total_xp))
                # Check for level up.
                if stat.xp + value >= stat.xp_limit:
                    # This is a level up.
                    stat.xp += value
                    # Do a "while" loop to allow for multiple level ups at once.
                    while stat.xp >= stat.xp_limit:
                        stat.level += 1
                        print("Congratulations! " + stat.name + " is now Level " + str(stat.level) + "!")
                        # Set XP progress back to 0 plus any excess over the XP needed for the level up.
                        stat.xp = 0 + (stat.xp - stat.xp_limit)
                        # Set the new XP Limit depending on if the stat is a Paradigm or a Parameter.
                        if isinstance(stat, main.Paradigm):
                            stat.xp_limit = stat.level * 25
                        elif isinstance(stat, main.Parameter):
                            stat.xp_limit = stat.level * 5
                        else:
                            # Just in case this breaks somewhere.
                            print("Error: " + stat.name + " is neither a Paradigm nor a Parameter.")
                            exit()
                # This is not a level up, so just increment the XP, too.
                else:
                    print("Stat before xp increase: " + str(stat.xp))
                    stat.xp += value
                    print("Stat after xp increase: " + str(stat.xp))
    print("inside mission_level_up")
    log_printer(updated_stats, print_bool=True, log_entry_bool=False, gui_bool=False)
    updated_weekend_fairy = log_printer(updated_stats, print_bool=False, log_entry_bool=True, gui_bool=False)
    main.create_my_arc(updated_weekend_fairy.parameters, updated_weekend_fairy.paradigms)