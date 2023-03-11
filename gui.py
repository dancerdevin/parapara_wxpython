# Here, I will attempt to learn how the WX package works and create a rudimentary GUI for logentry.py.
# If I can succeed in that, I'll build in a log entry reader, as well. (Since my hacky data storage is illegible as-is.)
# If I took the program any further, I would follow Eugene's advice and just not use CSV and write to text instead.
import datetime

import wx
import main
import logentry
import csv
from pubsub import pub


class PanelOne(wx.Panel):
    """The View Status screen."""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.all_stats = main.weekend_fairy.parameters + main.weekend_fairy.paradigms
        current_stats = logentry.stat_reader(self.all_stats)
        stats_string = logentry.log_printer(current_stats, print_bool=False, log_entry_bool=False, gui_bool=True)
        self.st = wx.StaticText(self, label=stats_string)
        font = self.st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.st.SetFont(font)

        pub.subscribe(self.refresh_display, "REFRESH_DISPLAY")

    def refresh_display(self):
        current_stats = logentry.stat_reader(self.all_stats)
        stats_string = logentry.log_printer(current_stats, print_bool=False, log_entry_bool=False, gui_bool=True)
        self.st.SetLabel(stats_string)


class PanelTwo(wx.Panel):
    """The Create Log Entry screen."""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.name_txt = wx.TextCtrl(self)
        name_label = wx.StaticText(self, label="Entry Name: ")
        self.entry_txt = wx.TextCtrl(self)
        entry_label = wx.StaticText(self, label="Entry Text: ")
        self.paradigm_txt = wx.TextCtrl(self)
        paradigm_label = wx.StaticText(self, label="Tag relevant paradigms, separated by commas: ")
        self.significance_txt = wx.TextCtrl(self)
        significance_label = wx.StaticText(self,
                                           label="Please input a significance rating (0 = Routine, 1 = Minor, 2 = Notable, 3 = Major, 4 = Miraculous): ")
        # Create a submit button and text that it can write an entry to the CSV file.
        self.parameter_txt = wx.TextCtrl(self)
        parameter_label = wx.StaticText(self, label="Parameter Override (Optional): Manually set Parameter XP gain. "
                                                    "Syntax is Parameter:Value, separated by commas.")
        button = wx.Button(parent=self, label='Create Log Entry', pos=(20, 120))
        button.Bind(wx.EVT_BUTTON, self.on_submit)  # bind action to button
        self.info_txt = wx.StaticText(self, label="")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(name_label, 0, wx.EXPAND)
        sizer.Add(self.name_txt, 0, wx.EXPAND)
        sizer.Add(entry_label, 0, wx.EXPAND)
        sizer.Add(self.entry_txt, 0, wx.EXPAND)
        sizer.Add(paradigm_label, 0, wx.EXPAND)
        sizer.Add(self.paradigm_txt, 0, wx.EXPAND)
        sizer.Add(significance_label, 0, wx.EXPAND)
        sizer.Add(self.significance_txt, 0, wx.EXPAND)
        sizer.Add(parameter_label, 0, wx.EXPAND)
        sizer.Add(self.parameter_txt, 0, wx.EXPAND)
        sizer.Add(button, 0, wx.EXPAND)
        sizer.Add(self.info_txt, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def on_submit(self, event):
        name_txt_contents = self.name_txt.GetValue()
        entry_txt_contents = self.entry_txt.GetValue()
        paradigm_txt_contents = self.paradigm_txt.GetValue()
        significance_txt_contents = self.significance_txt.GetValue()
        parameter_txt_contents = self.parameter_txt.GetValue()
        log_id = logentry.gui_log_entry(name_txt_contents, entry_txt_contents, paradigm_txt_contents, int(significance_txt_contents), parameter_txt_contents)
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")


class PanelThree(wx.Panel):
    """The View Log Entries screen."""

    # ----------------------------------------------------------------------
    # OK. In the constructor, create one StaticText field and two buttons to access earlier and later entries.
    # Use gui_log_reader to pull ten entries from weekend_fairy_logs, starting with the most recent.
    # Display those entries in the StaticText field. (Would a grid be better? Let's just get it working first.)
    # It would make sense to hide the button for earlier or later entries, respectively, if there are none to see.
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        # Get the content of the text box from gui_log_reader.
        self.current_counter = 0
        self.log_status = logentry.gui_log_reader(self.current_counter)
        current_entries = self.log_status[0]
        self.current_counter = self.log_status[1]
        self.total_entries = self.log_status[2]
        # In order to properly show the "next 10," I have to track how many entries are already displayed, too.
        self.entries_displayed = 0
        current_entries_string = "Log Entries\n"
        for entry in current_entries:
            entry_string = entry[0] + ". " + entry[1] + " (" + entry[2] + "): " + "\n" + entry[3] + "\n" + entry[4] + "\n"
            current_entries_string += entry_string
            self.entries_displayed += 1
        self.st = wx.StaticText(self, label=current_entries_string)
        # It was hiding an entry before, but I manually specified the wrap width below, and that seems to fix it.
        self.st.Wrap(950)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.st, 0, wx.EXPAND)
        sizer.AddStretchSpacer()

        # Counter display code for debugging.
        self.counter_st = wx.StaticText(self, label="Current Counter: " + str(self.current_counter))
        sizer.Add(self.counter_st, 0, wx.EXPAND)
        self.num_logs_st = wx.StaticText(self, label="Number of Log Entries: " + str(self.total_entries))
        sizer.Add(self.num_logs_st, 0, wx.EXPAND)
        self.earlier_button = wx.Button(parent=self, label='See Earlier Entries', pos=(20, 120))
        self.earlier_button.Bind(wx.EVT_BUTTON, self.on_submit_earlier)  # bind action to button
        sizer.Add(self.earlier_button, 0, wx.EXPAND)
        self.later_button = wx.Button(parent=self, label='See Later Entries', pos=(20, 120))
        self.later_button.Bind(wx.EVT_BUTTON, self.on_submit_later)  # bind action to button
        sizer.Add(self.later_button, 0, wx.EXPAND)
        self.SetSizer(sizer)

        pub.subscribe(self.refresh_display, "REFRESH_DISPLAY")
        # pub.subscribe(self.show_and_hide_buttons, "REFRESH_BUTTONS")
        # I wanted to activate show_and_hide_buttons on move to PanelThree to start by hiding later_button, but, bugged.

    def show_and_hide_buttons(self):
        # OK. If counter + 10 would be higher than total log entries, hide earlier_button. Else, show it.
        if self.current_counter >= self.total_entries:
            self.earlier_button.Hide()
        else:
            self.earlier_button.Show()
        # If counter - 10 would be lower than 0, hide later_button. Else, show it.
        # if self.current_counter - 11 < 0:
        #     self.later_button.Hide()
        # else:
        #
        if self.current_counter <= 10:
            self.later_button.Hide()
        else:
            self.later_button.Show()

    def refresh_display(self):
        # Copying and pasting the code from above just to make sure this stuff works.
        self.current_counter -= 1
        self.total_entries += 1
        # Updating debug code
        self.counter_st.SetLabel("Current Counter: " + str(self.current_counter))
        self.num_logs_st.SetLabel("Number of Log Entries: " + str(self.total_entries))
        self.log_status = logentry.gui_log_reader(self.current_counter)
        current_entries = self.log_status[0]
        self.current_counter = self.log_status[1]
        self.total_entries = self.log_status[2]
        # In order to properly show the "next 10," I have to track how many entries are already displayed, too.
        self.entries_displayed = 0
        current_entries_string = "Log Entries\n"
        for entry in current_entries:
            entry_string = entry[0] + ". " + entry[1] + " (" + entry[2] + "): " + "\n" + entry[3] + "\n" + entry[
                4] + "\n"
            current_entries_string += entry_string
            self.entries_displayed += 1
        self.st.SetLabel(current_entries_string)

    def on_submit_earlier(self, event):
        # Check if there ARE any earlier entries.
        self.log_status = logentry.gui_log_reader(self.current_counter)
        current_entries = self.log_status[0]
        self.current_counter = self.log_status[1]
        self.entries_displayed = 0
        current_entries_string = "Log Entries\n"
        for entry in current_entries:
            entry_string = entry[0] + ". " + entry[1] + " (" + entry[2] + "): " + "\n" + entry[3] + "\n" + entry[
                4] + "\n"
            current_entries_string += entry_string
            self.entries_displayed += 1
        self.st.SetLabel(current_entries_string)
        # Pasting button show/hide code.
        self.show_and_hide_buttons()
        self.counter_st.SetLabel("Current Counter: " + str(self.current_counter))

    def on_submit_later(self, event):
        # Check if there ARE any later entries.
        self.current_counter -= (10 + self.entries_displayed)
        self.log_status = logentry.gui_log_reader(self.current_counter)
        current_entries = self.log_status[0]
        self.current_counter = self.log_status[1]
        self.entries_displayed = 0
        current_entries_string = "Log Entries\n"
        for entry in current_entries:
            entry_string = entry[0] + ". " + entry[1] + " (" + entry[2] + "): " + "\n" + entry[3] + "\n" + entry[
                4] + "\n"
            current_entries_string += entry_string
            self.entries_displayed += 1
        self.st.SetLabel(current_entries_string)
        # Pasting button show/hide code.
        # Try this: if counter is at num_log_entries, hide earlier_button; if it's 10 or less, hide later_button.
        self.show_and_hide_buttons()
        self.counter_st.SetLabel("Current Counter: " + str(self.current_counter))


class PanelFour(wx.Panel):
    """The Tasks and Missions screen."""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        """Constructor"""
        dailies_label = wx.StaticText(self, label="Daily Missions")
        weeklies_label = wx.StaticText(self, label="Weekly Missions")
        tasks_label = wx.StaticText(self, label="Regular Tasks")
        # Daily and Weekly Missions will be checkboxes.
        self.daily_condition = wx.CheckBox(self, label="Periomaintenance")
        self.daily_condition.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.daily_community = wx.CheckBox(self, label="Review correspondence")
        self.daily_community.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.daily_diligence = wx.CheckBox(self, label="Clean something")
        self.daily_diligence.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.daily_memory = wx.CheckBox(self, label="Make log entry")
        self.daily_memory.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.daily_vivacity = wx.CheckBox(self, label="Go outside")
        self.daily_vivacity.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.daily_transcendence = wx.CheckBox(self, label="Ignore Twitter")
        self.daily_transcendence.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_adventurer = wx.CheckBox(self, label="A full workout")
        self.weekly_adventurer.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_knight = wx.CheckBox(self, label="One coding and one language practice")
        self.weekly_knight.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_sage = wx.CheckBox(self, label="Read a book")
        self.weekly_sage.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_dancer = wx.CheckBox(self, label="Go or plan dancing")
        self.weekly_dancer.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_homemaker = wx.CheckBox(self, label="Plan the week's meals")
        self.weekly_homemaker.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_logician = wx.CheckBox(self, label="Contact with my academic writing")
        self.weekly_logician.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_storyteller = wx.CheckBox(self, label="Weekly SCSMUSH hype")
        self.weekly_storyteller.Bind(wx.EVT_CHECKBOX, self.record_date)
        self.weekly_fairy = wx.CheckBox(self, label="Frolic")
        self.weekly_fairy.Bind(wx.EVT_CHECKBOX, self.record_date)
        task_condition = wx.Button(parent=self, label="Workout")
        task_condition.Bind(wx.EVT_BUTTON, self.on_workout)
        task_community = wx.Button(parent=self, label="Correspond")
        task_community.Bind(wx.EVT_BUTTON, self.on_correspond)
        task_diligence = wx.Button(parent=self, label="Coding/language practice")
        task_diligence.Bind(wx.EVT_BUTTON, self.on_practice)
        task_memory = wx.Button(parent=self, label="Study and take notes")
        task_memory.Bind(wx.EVT_BUTTON, self.on_study)
        task_vivacity = wx.Button(parent=self, label="Brighten a day")
        task_vivacity.Bind(wx.EVT_BUTTON, self.on_brighten)
        task_transcendence = wx.Button(parent=self, label="Mindfulness")
        task_transcendence.Bind(wx.EVT_BUTTON, self.on_mindful)
        self.task_content = wx.TextCtrl(self)
        task_field_label = wx.StaticText(self, label="Optional entry text for task:")
        self.info_txt = wx.StaticText(self, label="")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(dailies_label, 0, wx.EXPAND)
        sizer.Add(self.daily_condition, 0, wx.EXPAND)
        sizer.Add(self.daily_community, 0, wx.EXPAND)
        sizer.Add(self.daily_diligence, 0, wx.EXPAND)
        sizer.Add(self.daily_memory, 0, wx.EXPAND)
        sizer.Add(self.daily_vivacity, 0, wx.EXPAND)
        sizer.Add(self.daily_transcendence, 0, wx.EXPAND)
        sizer.Add(weeklies_label, 0, wx.EXPAND)
        sizer.Add(self.weekly_adventurer, 0, wx.EXPAND)
        sizer.Add(self.weekly_knight, 0, wx.EXPAND)
        sizer.Add(self.weekly_dancer, 0, wx.EXPAND)
        sizer.Add(self.weekly_sage, 0, wx.EXPAND)
        sizer.Add(self.weekly_homemaker, 0, wx.EXPAND)
        sizer.Add(self.weekly_logician, 0, wx.EXPAND)
        sizer.Add(self.weekly_storyteller, 0, wx.EXPAND)
        sizer.Add(self.weekly_fairy, 0, wx.EXPAND)
        sizer.Add(tasks_label, 0, wx.EXPAND)
        sizer.Add(task_condition, 0, wx.EXPAND)
        sizer.Add(task_community, 0, wx.EXPAND)
        sizer.Add(task_diligence, 0, wx.EXPAND)
        sizer.Add(task_memory, 0, wx.EXPAND)
        sizer.Add(task_vivacity, 0, wx.EXPAND)
        sizer.Add(task_transcendence, 0, wx.EXPAND)
        sizer.Add(task_field_label, 0, wx.EXPAND)
        sizer.Add(self.task_content, 0, wx.EXPAND)
        sizer.Add(self.info_txt, 0, wx.EXPAND)
        self.SetSizer(sizer)

        pub.subscribe(self.check_boxes, "CHECK_BOXES")
        self.all_checkboxes = [self.daily_condition, self.daily_community, self.daily_diligence, self.daily_memory,
                              self.daily_vivacity, self.daily_transcendence, self.weekly_adventurer,
                              self.weekly_knight, self.weekly_sage, self.weekly_dancer, self.weekly_homemaker,
                              self.weekly_logician, self.weekly_storyteller, self.weekly_fairy]
        self.dailies = [self.daily_condition, self.daily_community, self.daily_diligence, self.daily_memory,
                              self.daily_vivacity, self.daily_transcendence]
        self.weeklies = [self.weekly_adventurer, self.weekly_knight, self.weekly_sage, self.weekly_dancer,
                         self.weekly_homemaker, self.weekly_logician, self.weekly_storyteller, self.weekly_fairy]
        self.daily_missions_refreshed = False
        self.weekly_missions_refreshed = False
        self.all_stats = main.weekend_fairy.parameters + main.weekend_fairy.paradigms

    def record_date(self, event):
        with open('record_date.txt', 'w') as f:
            # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
            date_string = datetime.date.today().strftime("%d %V %y ")
            # Record the checked/unchecked state of all the boxes. Preserve them if unchanged.
            for box in self.all_checkboxes:
                if box.GetValue():
                    date_string += "1 "
                else:
                    date_string += "0 "
            f.write(date_string)

    def on_workout(self, event):
        this_entry_text = "Regular workout recorded."
        if self.task_content.GetValue() != "":
            this_entry_text = self.task_content.GetValue()
        log_id = logentry.gui_log_entry("Regular Workout", this_entry_text, "", 0, "Condition:1")
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded as a Workout.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")

    def on_correspond(self, event):
        this_entry_text = "Regular correspondence recorded."
        if self.task_content.GetValue() != "":
            this_entry_text = self.task_content.GetValue()
        log_id = logentry.gui_log_entry("Regular Correspondence", this_entry_text, "", 0, "Community:1")
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded as Correspondence.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")

    def on_practice(self, event):
        this_entry_text = "Regular coding/language practice recorded."
        if self.task_content.GetValue() != "":
            this_entry_text = self.task_content.GetValue()
        log_id = logentry.gui_log_entry("Regular Practice", this_entry_text, "", 0, "Diligence:1")
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded as Practice.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")

    def on_study(self, event):
        this_entry_text = "Regular study and notetaking recorded."
        if self.task_content.GetValue() != "":
            this_entry_text = self.task_content.GetValue()
        log_id = logentry.gui_log_entry("Regular Study", this_entry_text, "", 0, "Memory:1")
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded as Study.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")

    def on_brighten(self, event):
        this_entry_text = "Regular brightening recorded."
        if self.task_content.GetValue() != "":
            this_entry_text = self.task_content.GetValue()
        log_id = logentry.gui_log_entry("Regular Brightening", this_entry_text, "", 0, "Vivacity:1")
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded as a Brightening.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")

    def on_mindful(self, event):
        this_entry_text = "Regular creative stimulus recorded."
        if self.task_content.GetValue() != "":
            this_entry_text = self.task_content.GetValue()
        log_id = logentry.gui_log_entry("Regular Meditation", this_entry_text, "", 0, "Vivacity:1")
        # Update infotxt with log ID number.
        self.info_txt.SetLabel("Log entry " + str(log_id) + " has been recorded as Mindfulness.")
        # Update PanelOne with new stats and PanelThree with new log.
        pub.sendMessage("REFRESH_DISPLAY")

    def check_boxes(self):
        # Let's test the code by restoring checked boxes.
        with open('record_date.txt', 'r') as f:
            # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
            contents_string = f.readline()
            contents_list = contents_string.split(" ")
            recorded_day = contents_list[0]
            recorded_week = contents_list[1]
            recorded_year = contents_list[2]
            condition_bool = contents_list[3]
            community_bool = contents_list[4]
            diligence_bool = contents_list[5]
            memory_bool = contents_list[6]
            vivacity_bool = contents_list[7]
            transcendence_bool = contents_list[8]
            adventurer_bool = contents_list[9]
            knight_bool = contents_list[10]
            dancer_bool = contents_list[11]
            sage_bool = contents_list[12]
            homemaker_bool = contents_list[13]
            logician_bool = contents_list[14]
            storyteller_bool = contents_list[15]
            fairy_bool = contents_list[16]
            list_of_bools = [condition_bool, community_bool, diligence_bool, memory_bool, vivacity_bool,
                             transcendence_bool, adventurer_bool, knight_bool, dancer_bool, sage_bool, homemaker_bool,
                             logician_bool, storyteller_bool, fairy_bool]
            counter = 0
            for item in list_of_bools:
                if item == "1":
                    self.all_checkboxes[counter].SetValue(True)
                    counter += 1
                else:
                    counter += 1
            # OK. Now, compare dates.
            with open('record_date.txt', 'r') as f:
                # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
                if datetime.date.today().strftime("%d") != recorded_day:
                    different_day = True
                else:
                    different_day = False
                if datetime.date.today().strftime("%V") != recorded_week:
                    different_week = True
                else:
                    different_week = False
                if datetime.date.today().strftime("%y") != recorded_year:
                    different_year = True
                else:
                    different_year = False
                if different_day:
                    self.refresh_daily_missions()
                    self.daily_missions_refreshed = True
                if different_week:
                    self.refresh_weekly_missions()
                    self.weekly_missions_refreshed = True
                    # Make sure that it's not, e.g., another month but the same day numeral.
                    if not self.daily_missions_refreshed:
                        self.refresh_daily_missions()
                        self.daily_missions_refreshed = True
                # If both daily and weekly missions have already been refreshed, there's no need for more.
                # But if it's a new year and not still the last week of the previous year, refresh everything.
                if not self.daily_missions_refreshed and not self.weekly_missions_refreshed:
                    if different_year and recorded_week != 54:
                        self.refresh_daily_missions()
                        self.refresh_weekly_missions()
                        self.daily_missions_refreshed = True
                        self.weekly_missions_refreshed = True
                # Now let's change info_txt depending on what refreshed.
                if self.daily_missions_refreshed:
                    self.info_txt.SetLabel("Daily missions refreshed.")
                if self.weekly_missions_refreshed:
                    self.info_txt.SetLabel("Weekly missions refreshed.")

    def refresh_daily_missions(self):
        # Record the values of the daily mission checkboxes, which have been loaded from the text file already.
        # By "record," I don't mean make a log entry, but just modify the stat XP accordingly.
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {}
        for daily in self.dailies:
            if daily.GetValue():
                if daily == self.daily_condition:
                    xp_gain["Condition"] = 1
                if daily == self.daily_community:
                    xp_gain["Community"] = 1
                if daily == self.daily_diligence:
                    xp_gain["Diligence"] = 1
                if daily == self.daily_memory:
                    xp_gain["Memory"] = 1
                if daily == self.daily_vivacity:
                    xp_gain["Vivacity"] = 1
                if daily == self.daily_transcendence:
                    xp_gain["Transcendence"] = 1
        # Now, if there's any xp_gain, run the logger and refresh displays.
        if len(xp_gain) != 0:
            logentry.mission_level_up(xp_gain, current_stats)
            pub.sendMessage("REFRESH_DISPLAY")
            # Now clear all the dailies, as it's a new day.
            for daily in self.dailies:
                daily.SetValue(False)
            # Might as well record the current state now in case I don't check any boxes, right?
            # self.record_date()

    def refresh_weekly_missions(self):
        # Let's try the same thing for weeklies.
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {}
        for weekly in self.weeklies:
            if weekly.GetValue():
                if weekly == self.weekly_adventurer:
                    xp_gain["Adventurer"] = 5
                if weekly == self.weekly_knight:
                    xp_gain["Knight"] = 5
                if weekly == self.weekly_dancer:
                    xp_gain["Dancer"] = 5
                if weekly == self.weekly_sage:
                    xp_gain["Sage"] = 5
                if weekly == self.weekly_homemaker:
                    xp_gain["Homemaker"] = 5
                if weekly == self.weekly_logician:
                    xp_gain["Logician"] = 5
                if weekly == self.weekly_storyteller:
                    xp_gain["Storyteller"] = 5
                if weekly == self.weekly_fairy:
                    xp_gain["Fairy"] = 5
        # Now, if there's any xp_gain, run the logger and refresh displays.
        if len(xp_gain) != 0:
            logentry.mission_level_up(xp_gain, current_stats)
            pub.sendMessage("REFRESH_DISPLAY")
            # And clear all the weeklies.
            for weekly in self.weeklies:
                weekly.SetValue(False)
            # And record the current state. I guess this is redundant if dailies already ran, but whatever.
            # self.record_date()


class PanelFive(wx.Panel):
    """The Descs and Quests"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        """Constructor"""
        # OK. StaticText blocks for each paradigm, followed by checkboxes for each quest.
        # Save the checkboxes in another text file and run stat_reader/mission_level_up when checking off quests.
        # Let's begin by iterating through paradigm names, descs, and quests and saving them to string variables
        # name i0, desc i1, quests i7
        self.all_stats = main.weekend_fairy.paradigms + main.weekend_fairy.parameters

        # Now create texts and checkboxes and fill in labels with strings
        self.st_adventurer = wx.StaticText(self, label="")
        self.st_knight = wx.StaticText(self, label="")
        self.st_sage = wx.StaticText(self, label="")
        self.st_dancer = wx.StaticText(self, label="")
        self.st_homemaker = wx.StaticText(self, label="")
        self.st_logician = wx.StaticText(self, label="")
        self.st_storyteller = wx.StaticText(self, label="")
        self.st_fairy = wx.StaticText(self, label="")
        self.adventurer_quest1 = wx.CheckBox(self, label="")
        self.adventurer_quest1.Bind(wx.EVT_CHECKBOX, self.record_adv_quest)
        self.adventurer_quest2 = wx.CheckBox(self, label="")
        self.adventurer_quest2.Bind(wx.EVT_CHECKBOX, self.record_adv_quest)
        self.adventurer_quest3 = wx.CheckBox(self, label="")
        self.adventurer_quest3.Bind(wx.EVT_CHECKBOX, self.record_adv_quest)
        self.knight_quest1 = wx.CheckBox(self, label="")
        self.knight_quest1.Bind(wx.EVT_CHECKBOX, self.record_kni_quest)
        self.knight_quest2 = wx.CheckBox(self, label="")
        self.knight_quest2.Bind(wx.EVT_CHECKBOX, self.record_kni_quest)
        self.knight_quest3 = wx.CheckBox(self, label="")
        self.knight_quest3.Bind(wx.EVT_CHECKBOX, self.record_kni_quest)
        self.sage_quest1 = wx.CheckBox(self, label="")
        self.sage_quest1.Bind(wx.EVT_CHECKBOX, self.record_sage_quest)
        self.sage_quest2 = wx.CheckBox(self, label="")
        self.sage_quest2.Bind(wx.EVT_CHECKBOX, self.record_sage_quest)
        self.sage_quest3 = wx.CheckBox(self, label="")
        self.sage_quest3.Bind(wx.EVT_CHECKBOX, self.record_sage_quest)
        self.dancer_quest1 = wx.CheckBox(self, label="")
        self.dancer_quest1.Bind(wx.EVT_CHECKBOX, self.record_dan_quest)
        self.dancer_quest2 = wx.CheckBox(self, label="")
        self.dancer_quest2.Bind(wx.EVT_CHECKBOX, self.record_dan_quest)
        self.dancer_quest3 = wx.CheckBox(self, label="")
        self.dancer_quest3.Bind(wx.EVT_CHECKBOX, self.record_dan_quest)
        self.homemaker_quest1 = wx.CheckBox(self, label="")
        self.homemaker_quest1.Bind(wx.EVT_CHECKBOX, self.record_hom_quest)
        self.homemaker_quest2 = wx.CheckBox(self, label="")
        self.homemaker_quest2.Bind(wx.EVT_CHECKBOX, self.record_hom_quest)
        self.homemaker_quest3 = wx.CheckBox(self, label="")
        self.homemaker_quest3.Bind(wx.EVT_CHECKBOX, self.record_hom_quest)
        self.logician_quest1 = wx.CheckBox(self, label="")
        self.logician_quest1.Bind(wx.EVT_CHECKBOX, self.record_log_quest)
        self.logician_quest2 = wx.CheckBox(self, label="")
        self.logician_quest2.Bind(wx.EVT_CHECKBOX, self.record_log_quest)
        self.logician_quest3 = wx.CheckBox(self, label="")
        self.logician_quest3.Bind(wx.EVT_CHECKBOX, self.record_log_quest)
        self.storyteller_quest1 = wx.CheckBox(self, label="")
        self.storyteller_quest1.Bind(wx.EVT_CHECKBOX, self.record_sto_quest)
        self.storyteller_quest2 = wx.CheckBox(self, label="")
        self.storyteller_quest2.Bind(wx.EVT_CHECKBOX, self.record_sto_quest)
        self.storyteller_quest3 = wx.CheckBox(self, label="")
        self.storyteller_quest3.Bind(wx.EVT_CHECKBOX, self.record_sto_quest)
        self.fairy_quest1 = wx.CheckBox(self, label="")
        self.fairy_quest1.Bind(wx.EVT_CHECKBOX, self.record_fai_quest)
        self.fairy_quest2 = wx.CheckBox(self, label="")
        self.fairy_quest2.Bind(wx.EVT_CHECKBOX, self.record_fai_quest)
        self.fairy_quest3 = wx.CheckBox(self, label="")
        self.fairy_quest3.Bind(wx.EVT_CHECKBOX, self.record_fai_quest)
        # self.adventurer_parameters = {}
        # self.knight_parameters = {}
        # self.sage_parameters = {}
        # self.dancer_parameters = {}
        # self.homemaker_parameters = {}
        # self.logician_parameters = {}
        # self.storyteller_parameters = {}
        # self.fairy_parameters = {}

        with open('weekend_fairy_stats.csv', newline='') as stats_csv:
            fairy_reader = csv.reader(stats_csv, delimiter='|')
            for row in fairy_reader:
                for paradigm in self.all_stats:
                    if row[0] == paradigm.name:
                        if paradigm.name == "Adventurer":
                            self.st_adventurer.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.adventurer_quest1.SetLabel(quest_list[0])
                            self.adventurer_quest2.SetLabel(quest_list[1])
                            self.adventurer_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Knight":
                            self.st_knight.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.knight_quest1.SetLabel(quest_list[0])
                            self.knight_quest2.SetLabel(quest_list[1])
                            self.knight_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Sage":
                            self.st_sage.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.sage_quest1.SetLabel(quest_list[0])
                            self.sage_quest2.SetLabel(quest_list[1])
                            self.sage_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Dancer":
                            self.st_dancer.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.dancer_quest1.SetLabel(quest_list[0])
                            self.dancer_quest2.SetLabel(quest_list[1])
                            self.dancer_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Homemaker":
                            self.st_homemaker.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.homemaker_quest1.SetLabel(quest_list[0])
                            self.homemaker_quest2.SetLabel(quest_list[1])
                            self.homemaker_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Logician":
                            self.st_logician.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.logician_quest1.SetLabel(quest_list[0])
                            self.logician_quest2.SetLabel(quest_list[1])
                            self.logician_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Storyteller":
                            self.st_storyteller.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.storyteller_quest1.SetLabel(quest_list[0])
                            self.storyteller_quest2.SetLabel(quest_list[1])
                            self.storyteller_quest3.SetLabel(quest_list[2])
                        if paradigm.name == "Fairy":
                            self.st_fairy.SetLabel(row[0] + " -- " + row[1])
                            quest_list = row[7].split(",")
                            self.fairy_quest1.SetLabel(quest_list[0])
                            self.fairy_quest2.SetLabel(quest_list[1])
                            self.fairy_quest3.SetLabel(quest_list[2])

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.st_adventurer, 0, wx.EXPAND)
        sizer.Add(self.adventurer_quest1, 0, wx.EXPAND)
        sizer.Add(self.adventurer_quest2, 0, wx.EXPAND)
        sizer.Add(self.adventurer_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_knight, 0, wx.EXPAND)
        sizer.Add(self.knight_quest1, 0, wx.EXPAND)
        sizer.Add(self.knight_quest2, 0, wx.EXPAND)
        sizer.Add(self.knight_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_sage, 0, wx.EXPAND)
        sizer.Add(self.sage_quest1, 0, wx.EXPAND)
        sizer.Add(self.sage_quest2, 0, wx.EXPAND)
        sizer.Add(self.sage_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_dancer, 0, wx.EXPAND)
        sizer.Add(self.dancer_quest1, 0, wx.EXPAND)
        sizer.Add(self.dancer_quest2, 0, wx.EXPAND)
        sizer.Add(self.dancer_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_homemaker, 0, wx.EXPAND)
        sizer.Add(self.homemaker_quest1, 0, wx.EXPAND)
        sizer.Add(self.homemaker_quest2, 0, wx.EXPAND)
        sizer.Add(self.homemaker_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_logician, 0, wx.EXPAND)
        sizer.Add(self.logician_quest1, 0, wx.EXPAND)
        sizer.Add(self.logician_quest2, 0, wx.EXPAND)
        sizer.Add(self.logician_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_storyteller, 0, wx.EXPAND)
        sizer.Add(self.storyteller_quest1, 0, wx.EXPAND)
        sizer.Add(self.storyteller_quest2, 0, wx.EXPAND)
        sizer.Add(self.storyteller_quest3, 0, wx.EXPAND)
        sizer.Add(self.st_fairy, 0, wx.EXPAND)
        sizer.Add(self.fairy_quest1, 0, wx.EXPAND)
        sizer.Add(self.fairy_quest2, 0, wx.EXPAND)
        sizer.Add(self.fairy_quest3, 0, wx.EXPAND)
        self.SetSizer(sizer)

        pub.subscribe(self.check_boxes, "CHECK_BOXES")

        self.all_checkboxes = [self.adventurer_quest1, self.adventurer_quest2, self.adventurer_quest3,
                          self.knight_quest1, self.knight_quest2, self.knight_quest3, self.sage_quest1,
                          self.sage_quest2, self.sage_quest3, self.dancer_quest1, self.dancer_quest2,
                          self.dancer_quest3, self.homemaker_quest1, self.homemaker_quest2,
                          self.homemaker_quest3, self.logician_quest1, self.logician_quest2,
                          self.logician_quest3, self.storyteller_quest1, self.storyteller_quest2,
                          self.storyteller_quest3, self.fairy_quest1, self.fairy_quest2, self.fairy_quest3]

    # def make_parameter_dict(self, parameters):
    #     # Feed in a string that was a list and turn it into a dictionary.
    #     stripped_parameters = parameters.translate({ord(i): None for i in "[]+,'"})
    #     stripped_parameters_list = stripped_parameters.split("")
    #     # Some paradigms have three parameters and others have two. Don't go over the index when iterating.
    #     max_counter = len(stripped_parameters_list)
    #     counter = 0

    def record_quests(self):
        with open('quest_log.txt', 'w') as f:
            # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
            quest_string = ""
            # Record the checked/unchecked state of all the boxes. Preserve them if unchanged.
            for box in self.all_checkboxes:
                if box.GetValue():
                    quest_string += "1 "
                else:
                    quest_string += "0 "
            f.write(quest_string)

    def record_adv_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Adventurer": 25, "Condition": 50, "Community": 50, "Transcendence": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_kni_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Knight": 25, "Diligence": 50, "Memory": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_sage_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Sage": 25, "Vivacity": 50, "Memory": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_dan_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Dancer": 25, "Vivacity": 50, "Condition": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_hom_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Homemaker": 25, "Vivacity": 50, "Diligence": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_log_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Logician": 25, "Community": 50, "Diligence": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_sto_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Storyteller": 25, "Memory": 50, "Community": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    def record_fai_quest(self, event):
        current_stats = logentry.stat_reader(self.all_stats)
        xp_gain = {"Fairy": 25, "Transcendence": 100, "Condition": 50}
        logentry.mission_level_up(xp_gain, current_stats)
        pub.sendMessage("REFRESH_DISPLAY")
        self.record_quests()

    # Need new check_boxes code to pull previously completed quests from disk.
    # 1) Subscribe to message when switching to panelfive. This checks a new text file, quest_log.
    # 2) 24 binary digits in quest_log, one for each quest. If 0, unchecked; if 1, SetValue checked.

    def check_boxes(self):
        with open('quest_log.txt', 'r') as f:
            # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
            contents_string = f.readline()
            contents_list = contents_string.split(" ")
            adventurer_bool1 = contents_list[0]
            adventurer_bool2 = contents_list[1]
            adventurer_bool3 = contents_list[2]
            knight_bool1 = contents_list[3]
            knight_bool2 = contents_list[4]
            knight_bool3 = contents_list[5]
            sage_bool1 = contents_list[6]
            sage_bool2 = contents_list[7]
            sage_bool3 = contents_list[8]
            dancer_bool1 = contents_list[9]
            dancer_bool2 = contents_list[10]
            dancer_bool3 = contents_list[11]
            homemaker_bool1 = contents_list[12]
            homemaker_bool2 = contents_list[13]
            homemaker_bool3 = contents_list[14]
            logician_bool1 = contents_list[15]
            logician_bool2 = contents_list[16]
            logician_bool3 = contents_list[17]
            storyteller_bool1 = contents_list[18]
            storyteller_bool2 = contents_list[19]
            storyteller_bool3 = contents_list[20]
            fairy_bool1 = contents_list[21]
            fairy_bool2 = contents_list[22]
            fairy_bool3 = contents_list[23]
            list_of_bools = [adventurer_bool1, adventurer_bool2, adventurer_bool3, knight_bool1, knight_bool2,
                             knight_bool3, sage_bool1, sage_bool2, sage_bool3, dancer_bool1, dancer_bool2,
                             dancer_bool3, homemaker_bool1, homemaker_bool2, homemaker_bool3, logician_bool1,
                             logician_bool2, logician_bool3, storyteller_bool1, storyteller_bool2,
                             storyteller_bool3, fairy_bool1, fairy_bool2, fairy_bool3]
            counter = 0
            for item in list_of_bools:
                if item == "1":
                    self.all_checkboxes[counter].SetValue(True)
                    counter += 1
                else:
                    counter += 1

    # Also, some way to check if the box is already checked before giving XP... it's complicated with so many boxes.
    # The problem is that the functions aren't actually linked to the checkboxes calling them. I'm stumped for now.


class MyForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Panel Switcher Tutorial")

        self.panel_one = PanelOne(self)
        self.panel_two = PanelTwo(self)
        self.panel_three = PanelThree(self)
        self.panel_four = PanelFour(self)
        self.panel_five = PanelFive(self)
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.sizer.Add(self.panel_three, 1, wx.EXPAND)
        self.sizer.Add(self.panel_four, 1, wx.EXPAND)
        self.sizer.Add(self.panel_five, 1, wx.EXPAND)
        self.SetMinSize((1000, 700))
        self.SetSizer(self.sizer)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item_three = fileMenu.Append(wx.ID_ANY,
                                                        "View Status",
                                                        "Some text")
        self.Bind(wx.EVT_MENU, self.switch_to_panel_one,
                  switch_panels_menu_item_three)
        switch_panels_menu_item_one = fileMenu.Append(wx.ID_ANY,
                                                      "Create Log Entry",
                                                      "Some text")
        self.Bind(wx.EVT_MENU, self.switch_to_panel_two,
                  switch_panels_menu_item_one)
        switch_panels_menu_item_two = fileMenu.Append(wx.ID_ANY,
                                                      "View Log Entries",
                                                      "Some text")
        self.Bind(wx.EVT_MENU, self.switch_to_panel_three,
                  switch_panels_menu_item_two)
        switch_panels_menu_item_four = fileMenu.Append(wx.ID_ANY,
                                                       "View Missions and Tasks",
                                                       "Some text")
        self.Bind(wx.EVT_MENU, self.switch_to_panel_four,
                  switch_panels_menu_item_four)
        switch_panels_menu_item_five = fileMenu.Append(wx.ID_ANY,
                                                       "View Quests and Descs",
                                                       "Some text")
        self.Bind(wx.EVT_MENU, self.switch_to_panel_five,
                  switch_panels_menu_item_five)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    # ----------------------------------------------------------------------
    def switch_to_panel_one(self, event):
        """"""
        self.SetTitle("Viewing Status")
        if self.panel_two.IsShown():
            self.panel_two.Hide()
            self.panel_one.Show()
        elif self.panel_three.IsShown():
            self.panel_three.Hide()
            self.panel_one.Show()
        elif self.panel_four.IsShown():
            self.panel_four.Hide()
            self.panel_one.Show()
        elif self.panel_five.IsShown():
            self.panel_five.Hide()
            self.panel_one.Show()
        self.Layout()

    def switch_to_panel_two(self, event):
        """"""
        self.SetTitle("Creating Log Entry")
        if self.panel_one.IsShown():
            self.panel_one.Hide()
            self.panel_two.Show()
        elif self.panel_three.IsShown():
            self.panel_three.Hide()
            self.panel_two.Show()
        elif self.panel_four.IsShown():
            self.panel_four.Hide()
            self.panel_two.Show()
        elif self.panel_five.IsShown():
            self.panel_five.Hide()
            self.panel_two.Show()
        self.Layout()

    def switch_to_panel_three(self, event):
        """"""
        pub.sendMessage("REFRESH_BUTTONS")
        self.SetTitle("Viewing Log Entries")
        if self.panel_one.IsShown():
            self.panel_one.Hide()
            self.panel_three.Show()
        elif self.panel_two.IsShown():
            self.panel_two.Hide()
            self.panel_three.Show()
        elif self.panel_four.IsShown():
            self.panel_four.Hide()
            self.panel_three.Show()
        elif self.panel_five.IsShown():
            self.panel_five.Hide()
            self.panel_three.Show()
        self.Layout()

    def switch_to_panel_four(self, event):
        self.SetTitle("Viewing Missions and Tasks")
        # Trying to write a trigger for when switching to PanelFour that checks the date and boxes.
        pub.sendMessage("CHECK_BOXES")
        if self.panel_one.IsShown():
            self.panel_one.Hide()
            self.panel_four.Show()
        elif self.panel_two.IsShown():
            self.panel_two.Hide()
            self.panel_four.Show()
        elif self.panel_three.IsShown():
            self.panel_three.Hide()
            self.panel_four.Show()
        elif self.panel_five.IsShown():
            self.panel_five.Hide()
            self.panel_four.Show()
        self.Layout()

    def switch_to_panel_five(self, event):
        self.SetTitle("Viewing Quests and Descs")
        # Same trigger for PanelFive with slightly different effect.
        pub.sendMessage("CHECK_BOXES")
        if self.panel_one.IsShown():
            self.panel_one.Hide()
            self.panel_five.Show()
        elif self.panel_two.IsShown():
            self.panel_two.Hide()
            self.panel_five.Show()
        elif self.panel_three.IsShown():
            self.panel_three.Hide()
            self.panel_five.Show()
        elif self.panel_four.IsShown():
            self.panel_four.Hide()
            self.panel_five.Show()
        self.Layout()


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
