"""
This program has been written to automatize the generation of a qualtrics survey.

Library : pandas

For this, you need :

- a csv with your questions (my columns : ID, item)

Name : questions_formatted.csv

- a .txt file with a generic template for your question to be filled

Name : txt_squeletton.txt

It will generate a .txt file with all your questions in the same template that you want to import in Qualtrics

Name of the output : completed_template.txt

The code has to be changed a little bit depending on the two files that you import, but it doesn't take a lot of time !

"""

# we load the required libraries
import pandas as pd

# we create a pandas df from our list of questions and responses
# with question ID, question, and responses
questions_formatted = pd.read_csv("questions_formatted.csv", sep=";", encoding = 'cp1252')

# we upload our template
# this is a .txt file containing format for a single question

with open("txt_squeletton.txt", encoding='utf-8') as g:
    qualtrics_structure = g.readlines()

# this info is only repeated once so we create a single object
advanced_format = qualtrics_structure[0]

# we select the template in itself, excluding advanced_format
question_template = qualtrics_structure[1:]

# we create the list in which we will put all of the questions
list_of_question = []

# these lines allow to see each element of our template with its index
# so that we know what we want to change !
# so this is not fixed : depends on your survey architecture (txt_squeletton.txt)
for elt in range(len(question_template)) :
         print(elt)
         print(question_template[elt])

# we upload the matrixes
# a csv with the matrix nb and the url in qualtrics to upload it
matrices_url = pd.read_csv("url_saved_new.csv", index_col = None, sep=",")



# we loop through our questions df
for elt in range(len(questions_formatted)) :
    
    print(elt)
    ID = questions_formatted.loc[elt, 'ID']
    
    # the template in itself, renewed at each iteration
    question_template = qualtrics_structure[1:]

    # the block ID
    question_template[0] = "[[Block:" + ID + "_trial]]"
    
    # the cross ID
    question_template[3] = "[[ID:" + ID + "_cross]]"
    
    # rt cross ID
    question_template[13] = "[[ID:" + ID + "_cross_rt]]"
    
    # matrix to recall
    target_url = matrices_url.iloc[elt, 0]
    filler_1_url = matrices_url.iloc[elt, 1] 
    filler_2_url = matrices_url.iloc[elt, 2]
    filler_3_url = matrices_url.iloc[elt, 3]
    
    
    #load ID
    question_template[18] = "[[ID:" + ID + "_load]]"
    
    #load
    question_template[19] = '<div style="text-align: center;"><img src=\"' + target_url + '\" height=200 width=200 /></div>'
    #load RT ID
    question_template[27] = "[[ID:" + ID + "_load_rt]]"
    
        
    #question ID a
    question_template[31] = "[[ID:" + ID + "_question_a]]"
    
    #the 3 CRAT cues a
    txt = questions_formatted.loc[elt, 'item']
    list_CRAT = txt.split("/")
    question_template[32] = '<div class=\"deadline\"><div style="text-align: center;"><span style="color:#008000;"><strong>' + list_CRAT[0].upper() + " <br>"
    question_template[33] = list_CRAT[1].upper() + " <br>" 
    question_template[34] = list_CRAT[2].upper() + "</strong><br />" 
    question_template[35] = """
    <br />\n\
    Please give your very first, intuitive answer.</span></div>\n\
<span style="color:#008000;"><strong>\n    
    <style>\n\
        .ChoiceStructure {\n\
    text-align: center;\n\
}\n\
<div id="tempHead" style="height:1500px"></div>\n
</style>
    <style type="text/css">\n
     * {\n
   cursor: none;\n
     }\n
</style>"""
    
    #rt question a
    question_template[37] = "[[ID:" + ID + "_question_rt_a]]"
    
    #conf a
    question_template[41] = "[[ID:" + ID + "_conf_a]]"
    
    #conf rt a
    question_template[44] = "[[ID:" + ID + "_conf_rt_a]]"
    
    #Aha a
    question_template[48] = "[[ID:" + ID + "_Aha_a]]"
    
    #Aha rt a
    question_template[55] = "[[ID:" + ID + "_Aha_rt_a]]"
    
    # slow
    
    question_template[59] = "[[ID:" + ID + "_slow]]"
        
    #load recall ID
    question_template[65] = "[[ID:" + ID + "_load_recall]]"
    
    #load recall
    question_template[66] = "From the following pictures, which one was the presented pattern ?\n" + "[[AdvancedChoices]]\n" + "[[Choice:1]]\n" + "<img src=\"" + target_url + "\" height=200 width=200 />\n" + "[[Choice:2]]\n" + "<img src=\"" + filler_1_url + "\" height=200 width=200 />\n" + "[[Choice:3]]\n" + "<img src=\"" + filler_2_url + "\" height=200 width=200 />\n" + "[[Choice:4]]\n" + "<img src=\"" + filler_3_url + "\" height=200 width=200 />\n"
    
    #load recall rt
    question_template[70] = "[[ID:" + ID + "_load_recall_rt]]"
    
    #load correct
    question_template[74] = "[[ID:" + ID + "_load_correct]]"
    
    #load incorrect
    question_template[79] = "[[ID:" + ID + "_load_incorrect]]" 
    
    #question ID b
    question_template[84] = "[[ID:" + ID + "_question_b]]"
     
    #the 3 CRAT cues
    txt = questions_formatted.loc[elt, 'item']
    list_CRAT = txt.split("/")
    question_template[85] = '<div style="text-align: center;"><span style="color:#0000CD;"><strong>' + list_CRAT[0].upper() + " <br>"
    question_template[86] = list_CRAT[1].upper() + " <br>" 
    question_template[87] = list_CRAT[2].upper() + "</strong><br />" 
    question_template[88] = """
    <br />\n\
    Please give your final answer.</span></div>\n\
<span style="color:#0000CD;"><strong>\n    
    <style>\n\
        .ChoiceStructure {\n\
    text-align: center;\n\
}\n\
<div id="tempHead" style="height:1500px"></div>\n
</style>
    <style type="text/css">\n
     * {\n
   cursor: none;\n
     }\n
</style>"""
    
    #rt question b
    question_template[90] = "[[ID:" + questions_formatted.loc[elt, 'ID'] + "_question_rt_b]]"
    
    #conf b
    question_template[94] = "[[ID:" + questions_formatted.loc[elt, 'ID'] + "_conf_b]]"
    
    #conf rt b
    question_template[97] = "[[ID:" + questions_formatted.loc[elt, 'ID'] + "_conf_rt_b]]"
    
    #Aha b
    question_template[101] = "[[ID:" + questions_formatted.loc[elt, 'ID'] + "_Aha_b]]"
    
    #Aha rt b
    question_template[108] = "[[ID:" + questions_formatted.loc[elt, 'ID'] + "_Aha_rt_b]]"
    # we append the completed template to the final list
    list_of_question.append(question_template)


# practice trials: we suppress elt accordingly (some practice trials do not have load, etc.)
# we had to inspect visually the index of the elements of the trials we wanted to suppress
# here we want to identify the load part and the second stage part
cross_part = list(range(0, 16))
 
load_part = list(range(16, 30))
temp = list(range(63, 82))
load_part = load_part + temp

second_part = list(range(83, 109))

one_response = cross_part + second_part


no_load = [i for i in range(109) if i not in load_part]


load_only = cross_part + load_part

# one response (0-2)
# remove load and remove second part
for trial in range(len(list_of_question)):
    if trial in range(0, 3):
        # Iterate over the indices in second_part and keep only the corresponding elements in list_of_question[trial]
        list_of_question[trial] = [list_of_question[trial][i] for i in one_response]
            
# no load (3-4)

    if trial == 3 or trial == 4:
        list_of_question[trial] = [list_of_question[trial][i] for i in no_load]
        
# load only
    if trial == 5 or trial == 6:
        list_of_question[trial] = [list_of_question[trial][i] for i in load_only]




# we write the results in a new .txt file
with open('completed_template.txt', 'w') as h:
    # first element
    h.write(advanced_format)
    for item in list_of_question:
        for elt in item:
            h.write("%s\n" % elt)



# we close the files we opened with python
g.close()
h.close()






