'''
This file reads the Insight_pilot_two_resp.qsf file exported from qualtrics with the 
"P1" formatted manually.

It copy pastes its configuration to the other items, and writes another qsf file :
Customized_qsf.qsf = all the items customized

Here it also changes the target matrices directly in the qsf file

'''

# library

import json
import re
import copy
import pandas as pd



# open the qsf file
with open('Two_resp_insight_exp_2.qsf', encoding = 'utf-8') as f:
  data = json.load(f)

# view it as a tree, easier to understand the structure
# import pyjsonviewer
# pyjsonviewer.view_data(json_file="One_resp_insight.qsf")



# a question to find the infos
def get_question_info(data, source_tag):
    """
    Get the payload elements and index of a survey question with the given source_tag.
    """
    for index in range(len(data['SurveyElements'])):
        if data['SurveyElements'][index]['Element'] == "SQ" and data['SurveyElements'][index]['Payload']['DataExportTag'] == source_tag:
            question_info = data['SurveyElements'][index]['Payload']
            return question_info, index
    return None, None


# we write a function to copy paste the confiduration
def copy_question_payload(data, source_tag, dest_regex, payload_elements):
    """
    Copies specific elements of a question payload with a specified DataExportTag, 
    and applies them to all other questions whose DataExportTag matches the provided regex.
    
    Parameters:
    data (dict): The survey data as a dictionary
    source_tag (str): The DataExportTag of the question whose payload elements will be copied
    dest_regex (str): A regex pattern to match the DataExportTag of the destination questions
    payload_elements (list): A list of payload elements to be copied.
    
    Returns:
    None
    """
    # Loop through the survey questions
    for index in range(0, len(data['SurveyElements'])):
        # Check if this is the source question whose payload elements will be copied
        if data['SurveyElements'][index]['Element'] == "SQ" and data['SurveyElements'][index]['Payload']['DataExportTag'] == source_tag:
            # Save the payload elements to be applied to other questions
            ref_payload = {}
            for element in payload_elements:
                ref_payload[element] = data['SurveyElements'][index]['Payload'][element]
            break
    
    # Loop through the survey questions again
    for index in range(0, len(data['SurveyElements'])):
        # Check if this is a destination question whose payload elements will be updated
        if data['SurveyElements'][index]['Element'] == "SQ" and re.search(dest_regex, data['SurveyElements'][index]['Payload']['DataExportTag']):
            # Copy the payload elements from the source question
            for element in payload_elements:
                data['SurveyElements'][index]['Payload'][element] = ref_payload[element]


# uncomment to search target matrices that are similar between items
# list_url = []
# list_export_tag = []
# for index in range(len(data['SurveyElements'])):
#         if data['SurveyElements'][index]['Element'] == "SQ" and re.search("load_recall$", data['SurveyElements'][index]['Payload']['DataExportTag']):
#             infos = data['SurveyElements'][index]['Payload']
#             url = re.search(r'http[^"]*"', infos['Choices']['1']['Display']).group()[:-1]
#             export_tag = infos['DataExportTag']
#             list_url.append(url)
#             list_export_tag.append(export_tag)

# similar_elements = []
# for i in range(len(list_url)):
#     for j in range(i+1, len(list_url)):
#         if list_url[i] == list_url[j]:
#             similar_elements.append(list_export_tag[i])
#             similar_elements.append(list_export_tag[j])

# print(similar_elements)



infos, index = get_question_info(data, "Cust_slow")


# CROSS
# look at infos
infos, index = get_question_info(data, "Cust_cross")
# apply them
copy_question_payload(data, "Cust_cross", "cross$", ['QuestionJS'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_cross")


#CROSS RT
# look at infos
infos, index = get_question_info(data, "Cust_cross_rt")
# apply them
copy_question_payload(data, "Cust_cross_rt", "cross_rt$", ['Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_cross_rt")

#load RT
# look at infos
infos, index = get_question_info(data, "Cust_load_rt")
# apply them
copy_question_payload(data, "Cust_load_rt", "load_rt$", ['Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_load_rt")

# question_a
# look at infos
infos, index = get_question_info(data, "Cust_question_a")
# apply them
copy_question_payload(data, "Cust_question_a", "question_a$", ['QuestionJS', 'Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_question_a")

#question_a_rt
# look at infos
infos, index = get_question_info(data, "Cust_question_rt_a")
# apply them
copy_question_payload(data, "Cust_question_rt_a", "question_rt_a$", ['Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_question_rt_a")

# CONFIDENCE
# a little bit trickier car more things to change
# so copy of the whole payload and change the ID

# conf a

# # looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is the question already formatted manually (Custom ...)
        if data['SurveyElements'][index]['Payload']['DataExportTag'] == 'Cust_conf_a':
            # saving the configuration to paste it in other items !          
            ref_Payload = data['SurveyElements'][index]['Payload']
            Secondary = data['SurveyElements'][index]['SecondaryAttribute']


# # now, applying those parameters to other questions !

# # looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is a conf question
        if re.search("conf_a$", data['SurveyElements'][index]['Payload']['DataExportTag']):
            # copy pasting the formatted configuration in the other items
            template = copy.deepcopy(ref_Payload)
            ID_to_replace = data['SurveyElements'][index]['Payload']['QuestionID']
            Export_tag_to_replace = data['SurveyElements'][index]['Payload']['DataExportTag']
            template['DataExportTag'] = Export_tag_to_replace
            template['QuestionID'] = ID_to_replace
            data['SurveyElements'][index]['Payload'] = template
            data['SurveyElements'][index]['SecondaryAttribute'] = Secondary

# conf b

# # looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is the question already formatted manually (Custom ...)
        if data['SurveyElements'][index]['Payload']['DataExportTag'] == 'Cust_conf_b':
            # saving the configuration to paste it in other items !          
            ref_Payload = data['SurveyElements'][index]['Payload']
            Secondary = data['SurveyElements'][index]['SecondaryAttribute']


# # now, applying those parameters to other questions !

# # looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is a conf b question
        if re.search("conf_b$", data['SurveyElements'][index]['Payload']['DataExportTag']):
            # copy pasting the formatted configuration in the other items
            template = copy.deepcopy(ref_Payload)
            ID_to_replace = data['SurveyElements'][index]['Payload']['QuestionID']
            Export_tag_to_replace = data['SurveyElements'][index]['Payload']['DataExportTag']
            template['DataExportTag'] = Export_tag_to_replace
            template['QuestionID'] = ID_to_replace
            data['SurveyElements'][index]['Payload'] = template
            data['SurveyElements'][index]['SecondaryAttribute'] = Secondary

infos, index = get_question_info(data, "Load_1_conf_b")



# Aha_a / b
# look at infos
infos, index = get_question_info(data, "Cust_Aha_a")
# apply them
copy_question_payload(data, "Cust_Aha_a", "Aha_(a|b)$", ['QuestionJS', 'Configuration', 'Validation', 'QuestionType', 'Selector'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_Aha_b")

#Aha_rt_a / b
# look at infos
infos, index = get_question_info(data, "Cust_Aha_rt_a")
# apply them
copy_question_payload(data, "Cust_Aha_rt_a", "Aha_rt_(a|b)$", ['Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_Aha_rt_b")

# slow
# apply them
copy_question_payload(data, "Cust_slow", "slow$", ['DisplayLogic'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_slow")

# load recall
# look at infos
infos, index = get_question_info(data, "Cust_load_recall")
# apply them
copy_question_payload(data, "Cust_load_recall", "^(?!.*_rt).*load_recall.*", 
      ['QuestionJS', 'Validation', 'Configuration', 'DataVisibility', 'Randomization', 'RecodeValues'])
# check that change made by looking at random item
infos2, index = get_question_info(data, "Q3_load_recall")

#load recall rt
# look at infos
infos, index = get_question_info(data, "Cust_load_recall_rt")
# apply them
copy_question_payload(data, "Cust_load_recall_rt", "load_recall_rt$", ['Configuration'])
# check that change made by looking at random item
infos2, index = get_question_info(data, "Q3_load_recall_rt")

# question_b
# look at infos
infos, index = get_question_info(data, "Cust_question_b")
# apply them
copy_question_payload(data, "Cust_question_b", "question_b$", ['QuestionJS', 'Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "Q3_question_b")

# verbal fluency
# look at infos
infos, index = get_question_info(data, "fluency_1")
# apply them
copy_question_payload(data, "fluency_1", "^fluency_\d+", ['QuestionJS', 'Configuration', 'DisplayLogic', 'QuestionDescription', 'QuestionText'])
# check that change made by looking at random item
infos, index = get_question_info(data, "fluency_34")


# verbal fluency
# look at infos
infos, index = get_question_info(data, "fluency_rt_1")
# apply them
copy_question_payload(data, "fluency_rt_1", "^fluency_rt_\d+", ['Configuration'])
# check that change made by looking at random item
infos, index = get_question_info(data, "fluency_1")

'''
"DISP LOGIC" PARTS (cf below)

Here, we do not want to copy-paste the configuration of the customized item to the other
items, because the "Display logic" explicitly refers to a specific question by definition
(e.g., if response to question 248 is correct, then do that, etc.)

So this is a little bit trickier; we have to:

1) For the Custom trial: 
- get the reference ID to be replaced
- get the Disp logic template (that we will have to modify by replacing the ref question ID)

2) For each item:
- get the ID of the question this item refers to (e.g., the MCQ ID if it's the Disp logic of the MCQ conf item)
- modify the Disp logic template by replacing the ref question ID by the specific ID we found
- add this template to the question

'''

# get the ID and the description of the target custom question
def get_question_info_disp(data, question_tag):
    # Loop through all the survey elements
    for index in range(len(data['SurveyElements'])):
        # Check if the element is a survey question (SQ)
        if data['SurveyElements'][index]['Element'] == "SQ":
            # Check if this is the custom question we're looking for, identified by its DataExportTag
            if data['SurveyElements'][index]['Payload']['DataExportTag'] == question_tag:
                # Save the ID reference and question description
                question_id = data['SurveyElements'][index]['PrimaryAttribute']
                question_description = data['SurveyElements'][index]['Payload']['QuestionDescription']
                # Return the question ID and description as separate objects
                return question_id, question_description
    # If the question is not found, return None
    return None, None

def get_display_logic(data, display_logic_tag):
    # Loop through all the survey elements
    for index in range(len(data['SurveyElements'])):
        # Check if the element is a survey question (SQ)
        if data['SurveyElements'][index]['Element'] == "SQ":
            # Check if this is the custom question we're looking for, identified by its DataExportTag
            if data['SurveyElements'][index]['Payload']['DataExportTag'] == display_logic_tag:
                # Save the display logic template for future use
                display_logic = data['SurveyElements'][index]['Payload']['DisplayLogic']
                # Return the display logic template
                return display_logic
    # If the question is not found, return None
    return None

def replace_display_logic(data, string_ID, first_part_ID, second_part_ID):
    """
    Replaces the display logic of a survey question with the display logic of another question
    that has the same name except for a different ID

    Arguments:
    - data: the data object containing the survey questions
    - string_ID: a string that should be used to identify the survey questions targeted by the modified display logic
    - first_part_ID: a string that should be used to identify the first part of the survey question ID
    - second_part_ID: a string that should be used to identify the second part of the survey question ID

    Returns:
    - None
    """

    # Loop through every question
    for index_question in range(0, len(data['SurveyElements'])):
        # Checking if this is a survey question
        if data['SurveyElements'][index_question]['Element'] == "SQ":
            # Checking if this is the good type of question (usually contains "question")
            if re.search(string_ID, data['SurveyElements'][index_question]['Payload']['DataExportTag']):
            
                # Create a deepcopy of the reference display logic dictionary to create a new one
                new_disp = copy.deepcopy(display_logic)

                # Get the ID and description of the question we will have to use to replace the reference ID and description
                ID_to_replace = data['SurveyElements'][index_question]['PrimaryAttribute']
                Desc_to_replace = data['SurveyElements'][index_question]['Payload']['QuestionDescription']
            
                # Replace the reference ID and description in the reference display logic
                # we take each dictionnary in the disp logic part except the last one
                keys_to_change = []
                keys_to_change.extend(new_disp['0'].keys())
                keys_to_change.pop(-1)
            
                for nb in keys_to_change:
                    for elt in new_disp['0'][nb]:
                        # Replace the reference ID and description by the actual ones
                        new_disp['0'][nb][elt] = display_logic['0'][nb][elt].replace(question_id, ID_to_replace).replace(question_description, Desc_to_replace)

            
                # Find the corresponding question (which contains the display logic part)
                # Here we want to go from "...question" to "...conf" for instance
                name_question = data['SurveyElements'][index_question]['Payload']['DataExportTag']

                name_contains = re.search(first_part_ID, name_question).group(1)
                name_contains = name_contains + second_part_ID
                print(name_contains)
            
                # Search for the question now that we have its name
                for index_conf in range(0, len(data['SurveyElements'])):
                    # Checking if this is a survey question
                    if data['SurveyElements'][index_conf]['Element'] == "SQ":
                        if data['SurveyElements'][index_conf]['Payload']['DataExportTag'] == name_contains:
                            # Copy and paste the display logic we created to the question
                            data['SurveyElements'][index_conf]['Payload']['DisplayLogic'] = new_disp
                            print("done")


# Conf a
question_id, question_description = get_question_info_disp(data, "Cust_question_a")
display_logic = get_display_logic(data, "Cust_conf_a")
replace_display_logic(data, "question_a$", "(.*)_question_a", "_conf_a")
# check it worked
infos, index = get_question_info(data, "Q6_question_a")
infos, index = get_question_info(data, "Q6_conf_a")

# Conf b
question_id, question_description = get_question_info_disp(data, "Cust_question_b")
display_logic = get_display_logic(data, "Cust_conf_b")
replace_display_logic(data, "question_b$", "(.*)_question_b", "_conf_b")
# check it worked
infos, index = get_question_info(data, "Q6_question_b")
infos, index = get_question_info(data, "Q6_conf_b")

# Aha a
question_id, question_description = get_question_info_disp(data, "Cust_question_a")
display_logic = get_display_logic(data, "Cust_Aha_a")
replace_display_logic(data, "question_a$", "(.*)_question_a", "_Aha_a")
# check it worked
infos, index = get_question_info(data, "Q6_question_a")
infos, index = get_question_info(data, "Q6_Aha_a")

# Aha b
question_id, question_description = get_question_info_disp(data, "Cust_question_b")
display_logic = get_display_logic(data, "Cust_Aha_b")
replace_display_logic(data, "question_b$", "(.*)_question_b", "_Aha_b")
# check it worked
infos, index = get_question_info(data, "Q6_question_b")
infos, index = get_question_info(data, "Q6_Aha_b")


# see function and qualtrics and apply the functions!

# correct
question_id, question_description = get_question_info_disp(data, "Cust_load_recall")
display_logic = get_display_logic(data, "Cust_load_correct")
replace_display_logic(data, "load_recall$", "(.*)_load_recall", "_load_correct")
# check it worked
infos, index = get_question_info(data, "Q3_load_correct")
infos_2, index = get_question_info(data, "Q3_load_recall")

# incorrect
question_id, question_description = get_question_info_disp(data, "Cust_load_recall")
display_logic = get_display_logic(data, "Cust_load_incorrect")
replace_display_logic(data, "load_recall$", "(.*)_load_recall", "_load_incorrect")
# check it worked
infos, index = get_question_info(data, "Q3_load_incorrect")
infos_2, index = get_question_info(data, "Q3_load_recall_")


# we create a new version of the qsf file
with open('customized_qsf.qsf', 'w') as h:
    json.dump(data, fp=h)
    
# we close the files we opened with python
f.close()
h.close()

