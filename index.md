# How to automate experiments in Qualtrics
*Jérémie Beucler* *- October, 2021*


This Github page explains how to partially automate experiments generation on Qualtrics using `Python`. Note that you may do the same thing using `R` or a similar programmation language.

*Notes :*
- *This page would not have been created without Matthieu Raoelison, who came up with this process in the first place;*
- *This page was created in October, 2021. Because of Qualtrics updates, some informations about the `.qsf` file may become outdated. However, it should not be a major issue once you have understood the logic behind this process.*

## Introduction

Qualtrics is an online software that allows to generate online surveys. However, some people use it to design scientific psychology experiments, for several reasons. For instance, it is [very easy](https://researcher-help.prolific.co/hc/en-gb/articles/360009224113-Qualtrics-Integration-Guide#heading-1) to run an online experiment using Qualtrics and the participants recruitment platform [Prolific](https://www.prolific.com/).

This (mis)use of Qualtrics can be quite problematic. Although you can insert some [Javascript code](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/add-javascript/) in your questions and add some logic to your experiment using the [Survey flow](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/survey-flow-overview/), Qualtrics still remains a "point and click" software.

Suppose you want to generate a psychology experiment in Qualtrics. In one trial, you may want to display a fixation cross for a given time, show a stimulus  and then record participants answers to this stimulus. In Qualtrics, generating this trial once is quite easy.

However, your experiment may contain different conditions, each one containing several trials ... If you try to implement this on Qualtrics by hand, it will take a lot of time and may lead to errors. Even worse, suppose you painfully managed to build your experiment, and you realize you wanted the fixation cross to be displayed not for two seconds, but only for one. You now have to modify each trial individually. Uh oh ...  This is the kind of task where you may want to use programming !

## General overview

Here is a brief summary of the different steps for automating experiments in Qualtrics:

1. Prepare a list of your different items (e.g., in a `.csv` file);
2. Write a program generating a `.txt` file with the complete structure of the experiment and import it on Qualtrics;
3. Fully customize one item on Qualtrics by hand and export your survey in a `.qsf` file
4. Open this file with Python, copy the configuration of the manually customized item onto the other items and import the new `.qsf` file on Qualtrics;
5. If you want to change something in your items configuration : go back to step 2 or 3.

You may have noticed that this is not a fully automated process. You indeed have to manually customize one item on Qualtrics, or to import and export the survey at its different stages. However, these operations are very easy to perform and do not take a lot of time on the whole.

## STEP 1 : Prepare a list of your different items

![](/docs/assets/images/csv_image.png)

Create a `.csv` file (or any format you find suitable, as long as you can read it on Python afterwards) containing what is gonna change from trial to trial : questions, possible answers ...

**Important : you should also have a column containing the trial/item ID, in a structured way. This will be necessary to find your item in the `.qsf` file (step 4).**

*Example : if you have two conditions - Conflict and No-Conflict - with 20 items in each, you can name your items : C_1, NC_1, C_2 ...*

## STEP 2 : Write a program generating a `.txt` file with the complete structure of the experiment and import it on Qualtrics;

![](/docs/assets/images/struct_image.png)

Fortunately, Qualtrics allows you to import a simple survey structure in a `.txt` file, using a specific syntax. However, the features you can implement through this file are very limited. For instance, you cannot set up a response time in it. This file will only allow you to create the "squeletton" of your survey.

Before proceeding, read the *Preparing a Simple Format TXT or DOC File* and the *Preparing an Advanced Format TXT or DOC File* sections of the following page, which explain the rules you have to follow in your `.txt` file : [How to import a survey on Qualtrics](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/).

Once you have understood how the `.txt` file works, you can generate a basic trial structure. Then, you  only have to use a `for` loop to fill this structure with your different items. I advise you to create one block per trial, as one trial contains several elements in Qualtrics format. Hence, for trial n°1, you will create block n°1 containing fixation cross n°1, question n°1 ...

Here is an example of what this part of your code may look like. This generates simple trials, with a fixation cross and a MCQ. The "rt" elements correspond to "timers" in Qualtrics, that allow to record RT or to display an element for a givent duration.

Note :

- *`questions_formated` is the data frame (`.csv` file) with all our items, ID, possible answers;*
- *`question_template` is a list of strings containing the structure of a typical trial;*
- *`list_of_question` is the list where we put all the trials;*

```python
# we loop through our questions df
for elt in range(len(questions_formated)) :
    # the template in itself, renewed at each iteration
    question_template = qualtrics_structure[1:]
    # the block ID; one block = a complete trial
    question_template[1] = "[[Block:" + questions_formated.loc[elt, 'ID_long'] + "]]"
    # the fixation cross ID
    question_template[4] = "[[ID:" + questions_formated.loc[elt, 'ID'] + "_cross]]"
    # rt fixation cross ID
    question_template[7] = "[[ID:" + questions_formated.loc[elt, 'ID'] + "_cross_rt]]"
    # question ID
    question_template[12] = "[[ID:" + questions_formated.loc[elt, 'ID'] + "_MCQ]]"
    # text of question
    question_template[13] = questions_formated.loc[elt, 'sentence']
    # first response option
    question_template[15] = questions_formated.loc[elt, 'Rep_1']
    # second response option
    question_template[16] = questions_formated.loc[elt, 'Rep_2']
    # third and four are always the same
    question_template[17] = "This question can't be answered in this form"
    question_template[18] = "Don't know"
    # rt MCQ ID
    question_template[20] = "[[ID:" + questions_formated.loc[elt, 'ID'] + "_MCQ_rt]]"

    # we append the completed template to the final list
    list_of_question.append(question_template)
```

**Important : you must add an ID to each element of your trial (e.g., block, fixation cross, question, timer ...). This will be necessary to find each part of your trial in the `.qsf` file (step 4). The block ID should be present in each sub-element ID.**

You have to write the final list in a `.txt` file. It should looks like this:

![](/docs/assets/images/final_txt_file_image.png)

After that, you have to import this `.txt` file on Qualtrics. This is how to do it: [How to import a TXT Survey on Qualtrics](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/#ImportTXTDoc).

*Note : During the importation process, Qualtrics automatically adds the date after your block's name (e.g., "No_conflict_1_0" will become "No_conflict_1_0 - Oct 20, 2021").*

## STEP 3 : Fully customize one item on Qualtrics by hand and export your survey in a `.qsf` file

![](/docs/assets/images/qualtrics_manual_image.png)

Once your survey has been imported on Qualtrics, choose one of your trials (in Qualtrics, a "block"), and customize it manually. This is where you can set up the trial options using the Qualtrics interface. For even more advanced customization, you may want to add some JavaScript code to the question. After you have customized one trial, note its block ID (e.g., "C_01). 

Then, export your survey as a `.qsf` file: [How to export a Survey as a QSF](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/#ExportingaSurveyasaQSF).

## STEP 4 : Open this file with Python, copy the configuration of the manually customized item onto the other items and import the new `.qsf` file on Qualtrics;

### Understand the structure of the `.qsf` file

For this last stage, it is crucial that you understand what a `.qsf` file is and how it is organized.

Before proceeding, here are two ressources you should read that will explain it to you:
- [Quickstart Guide to understand the Qualtrics Survey File](https://gist.github.com/ctesta01/d4255959dace01431fb90618d1e8c241)
- [How to generate qualtrics questions](https://blog.askesis.pl/post/2019/04/qualtrics-generate.html)

### Open the `.qsf` file

As you read, the file contains `JSON` code. Fortunately, you can read it using a `JSON` encoder/decoder. I used the [json library](https://docs.python.org/3/library/json.html) to do it. To read the qsf file, I just had to use the `json.load` function:

```python
# open the qsf file
with open('my_project.qsf', encoding = 'utf-8') as f:
  data = json.load(f)
```
At this point, you should be able to manually explore the file. I found the *variable explorer* of the [`Spyder` environment](https://www.spyder-ide.org/) to be very useful to explore the object. As you read, the object contains several elements. In Python, it is a dictionary containing a series of nested dictionaries. You can think of it as a drawer, with drawers in it, which themselves contain other drawers.

Here is an example of this Russian doll type of structure:

![](/docs/assets/images/spyder_manual_image.png)

If you look at each window's title bar, you can see that I first opened the object `Data`, then `SurveyElements`, then the item n° `223`, then its `Payload`, and finally its `Randomization` settings.

### Copy-paste the customized item configuration onto the other items

Remember, you know the name of the item you customized manually. You now have to loop through your survey's elements to find it.

*Note : as you read, you should only look at Survey Questions (SQ) : hence the `if data['SurveyElements'][index]['Element'] == "SQ":` line.* 

```python
# looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is the question already formatted manually (NC_1_0 ...)
        if data['SurveyElements'][index]['Payload']['DataExportTag'] == 'NC_1_0_MCQ' :
            # printing index to look at it manually !
            print(index)
 ```

This code displays the index of the question you formatted manually. You can now find it by hand in the explorer, to see which elements of the `Payload` (which is the part of the question containing its configuration) you may want to copy-paste onto the other questions. This should not be too difficult, as you know what you customized manually on Qualtrics and as the `Payload` elements are named transparently (e.g., `QuestionJS` for the JavaScript elements of the question).

Once you have done that, you just have to do the copy-paste operation. Here is an example for multiple-choice questions (MCQs) settings:

 ```python
# MCQ PARAMETERS

# looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is the question already formatted manually (NC_1_0 ...)
        if data['SurveyElements'][index]['Payload']['DataExportTag'] == 'NC_1_0_MCQ' :
            # saving the configuration to paste it in other items !
            # choice randomization
            ref_MCQ_rando = data['SurveyElements'][index]['Payload']['Randomization']
            # validation (e.g., forced answer)
            ref_MCQ_vali = data['SurveyElements'][index]['Payload']['Validation']
            # JS for not displaying next button, going to next question when clicking
            ref_MCQ_JS = data['SurveyElements'][index]['Payload']['QuestionJS']
            
# now, applying those parameters to other MCQ questions !

# looping through the questions
for index in range(0, len(data['SurveyElements'])):
    # checking if question (SQ = survey questions)
    if data['SurveyElements'][index]['Element'] == "SQ":
        # checking if this is a MCQ question
        if re.search("MCQ$", data['SurveyElements'][index]['Payload']['DataExportTag']):
            # copy pasting the formatted configuration in the other items
            data['SurveyElements'][index]['Payload']['Randomization'] = ref_MCQ_rando
            data['SurveyElements'][index]['Payload']['Validation'] = ref_MCQ_vali
            data['SurveyElements'][index]['Payload']['QuestionJS'] = ref_MCQ_JS

 ```
 
You can see that we use [regular expressions](https://docs.python.org/3/library/re.html) to navigate through the question IDs : `if re.search("MCQ$", data['SurveyElements'][index]['Payload']['DataExportTag']):`. This allows us to only modify MCQ question in this example. 
 
You have to repeat this copy-pasting operation for each element of your trial (e.g., the fixation cross parameters, the MCQ timer parameters, etc.).

Once you are finished, you only have to write the result in a new `.qsf` file thanks to the `json.dump` function :

 ```python
 # new version of the qsf file
with open('my_project_modified.qsf.qsf', 'w') as h:
    json.dump(data, fp=h)
 ```

### Import the new `.qsf` file on Qualtrics

Finally, you have to import the new .qsf file: [Importing a QSF Survey](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/#ImportingASurvey).

You should find all the different trials in the same, customized format. Congratulations, you've done it!

You can now modify the [Survey flow](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/survey-flow-overview/), change the general appearance of the survey...

### STEP 5 : If you want to change something in your items configuration, go back to step 2 or 3.

If you realize that you have some modifications to make to your trial configuration, you can go back to step 2 or 3 (depending on the modification). Note that exporting and importing the survey in the `.qsf` format will not affect the Survey Flow, or other settings you may have fixed manually.



