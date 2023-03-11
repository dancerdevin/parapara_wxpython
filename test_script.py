import datetime

# sublist = [1, 2, 3]
# list = [1, 2, 3, sublist]
# print(list[3][1])
string = "['Condition +1', 'Community +1', 'Transcendence +1']"
new_string = string.translate({ord(i): None for i in "[]+,'"})
print(new_string)

# DONE. 1. Store "last_checked_box_day" for daily missions and "last_checked_box_week" for weekly missions. Write to text.
# DONE. 1.5. I also need to record the state of the checkboxes themselves for after I close the program!
# 2. On switching to PanelFour (if I can get that to work), compare today's year, then week, then day.
# DONE. 2.5. Also, retrieve the last saved states of the checkboxes.
# 3. If the year is different, clear all (lol). If week, clear all. If day, clear daily.
# 3.5. Check whatever boxes should remain checked.
# 4. Before clearing, GetValue and add parameter/paradigm XP according to which ones were checked.
# 5. Update the StaticText label at the bottom with XP gained, just so you know something happened?
# with open('record_date.txt', 'r') as f:
#     # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
#     contents_string = f.readline()
#     contents_list = contents_string.split(" ")
#     recorded_day = contents_list[0]
#     recorded_week = contents_list[1]
#     recorded_year = contents_list[2]
#     if datetime.date.today().strftime("%d") != recorded_day:
#         different_day = True
#     else:
#         different_day = False
#     if datetime.date.today().strftime("%V") != recorded_week:
#         different_week = True
#     else:
#         different_week = False
#     if datetime.date.today().strftime("%y") != recorded_year:
#         different_year = True
#     else:
#         different_year = False
#     daily_missions_refreshed = False
#     if different_day:
#         refresh_daily_missions()
#         daily_missions_refreshed = True
#     if different_week:
#         self.refresh_weekly_missions()
#         weekly_missions_refreshed = True
#         # Make sure that it's not, e.g., another month but the same day numeral.
#         if not daily_missions_refreshed:
#             self.refresh_daily_missions()
#             daily_missions_refreshed = True
#     # If both daily and weekly missions have already been refreshed, there's no need for more.
#     # But if it's a new year and not still he last week of the previous year, refresh everything just in case.
#     if not daily_missions_refreshed and not weekly_missions_refreshed:
#         if different_year and recorded_week != 54:
#             self.refresh_daily_missions()
#             self.refresh_weekly_missions()
#             daily_missions_refreshed = True
#             weekly_missions_refreshed = True
#
#
# def refresh_daily_missions(self):
#     pass
#
#
# def refresh_weekly_missions(self):
#     pass
#
# # Logic: if the day is the same, check that the week is the same. If the day is different, refresh daily missions.
# # If the week is the same, check that the year is the same. If the year is different, refresh daily and weekly missions.
# # If the year is the same, refresh nothing. If the week is different, refresh daily and weekly missions.
# # This should avoid issues like closing the program for a year and opening it on the same week next year, etc.
#
#
# datetime_object = datetime.datetime.strptime('2022-1-1', '%Y-%m-%d').date()
# print(datetime_object.strftime("%d"))
# print(datetime_object.strftime("%V"))
# print(datetime_object.strftime("%y"))
# print(datetime.date.today().strftime("%V"))
# print(datetime.date.today().strftime("%y"))

# with open('record_date.txt', 'r') as f:
#     # Record day, week, and year, separated by spaces, to be split into a list for later comparison.
#     contents_string = f.readline()
#     contents_list = contents_string.split(" ")
#     recorded_day = contents_list[0]
#     recorded_week = contents_list[1]
#     recorded_year = contents_list[2]
#     condition_bool = contents_list[3]
#     community_bool = contents_list[4]
#     diligence_bool = contents_list[5]
#     memory_bool = contents_list[6]
#     vivacity_bool = contents_list[7]
#     transcendence_bool = contents_list[8]
#     adventurer_bool = contents_list[9]
#     knight_bool = contents_list[10]
#     dancer_bool = contents_list[11]
#     sage_bool = contents_list[12]
#     homemaker_bool = contents_list[13]
#     logician_bool = contents_list[14]
#     storyteller_bool = contents_list[15]
#     fairy_bool = contents_list[16]
#     list_of_bools = [condition_bool, community_bool, diligence_bool, memory_bool, vivacity_bool, transcendence_bool,
#                      adventurer_bool, knight_bool, dancer_bool, sage_bool, homemaker_bool, logician_bool,
#                      storyteller_bool, fairy_bool]
#     for item in list_of_bools:
#         counter = 0
#         if item == "1":

